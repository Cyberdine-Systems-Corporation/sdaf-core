#!/usr/bin/env python3
"""Comprobación MECÁNICA de la coherencia arquitectónica de un repositorio con línea base.

No decide ni aprueba nada: comprueba que la línea base (`architecture/description.md`),
los ADRs, las unidades de `stack.units` y las specs no se contradicen. Solo con la
línea base en estado Approved hace las tres comprobaciones siguientes:

1. ADRs frente a la sección «Decisiones vigentes» de la línea base. «Vigente» es
   ADR-006 §4: estado Aceptado (o su equivalente heredado) y sin «Sustituido por»,
   leído de los ficheros ADR, no del índice. FAIL: un ADR listado que no existe,
   uno listado que está sustituido o un ADR que no es UTF-8. AVISO: un ADR vigente
   que no figura en la sección, un ADR listado que no es vigente ni sustituido
   (Propuesto, Rechazado, Deprecado…), la sección ausente o `N/A` habiendo ADRs vigentes.
2. Unidades de `stack.units`: cada `name` debe figurar, con el mismo texto, entre las
   unidades de la línea base; si no, FAIL (añadir una unidad exige un ADR Aceptado y
   una versión nueva de la línea base, H14 §6). El atajo `src_path`/`tests_path` no
   tiene nombres: no hay nada que cotejar. Una config ilegible es FAIL.
3. Unidades de las specs (`specs/**`): cada unidad citada en `Unidades` debe figurar en
   la línea base, si no, FAIL. Se ignoran las specs con ID de plantilla y los
   placeholders del campo. Una spec sin campo `Unidades` es AVISO; un `.md` que no es
   UTF-8 es FAIL.

Cuando no se puede comprobar, avisa y sale 0 sin más (no duplica G0.6): línea base
ausente o en un estado distinto de Approved, o `sdaf.version` anterior a 0.5.0. Una
`sdaf.config.yaml` o una `sdaf.version` ilegibles, o una línea base que no es UTF-8,
son FAIL.

Códigos de salida: 0 sin FAIL (aunque haya AVISO), 1 con algún FAIL, 2 si el uso es
erróneo (`--root` no es un directorio). Nunca escribe ficheros ni cambia estados.

NO se ejecuta sobre el propio core: el core no tiene línea base ni specs. Solo lo
ejercita su autocomprobación, `scripts/test-architecture.py`.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sdaf_adrs import ADR_FOLDER, adr_label, adr_vigencia  # noqa: E402
from sdaf_diff import ConfigUnreadable, load_units  # noqa: E402
from sdaf_docs import baseline, baseline_adrs, is_placeholder, spec_units  # noqa: E402

CONFIG = "sdaf.config.yaml"
BASELINE = "architecture/description.md"
MIN_LINE = (0, 5, 0)  # la línea base y su coherencia son de la línea 0.5.0 (opt-in)
APPROVED = "Approved"
SECTION = "«Decisiones vigentes»"
VERSION_RE = re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?")
CONFIG_ERRORS = (yaml.YAMLError, OSError, UnicodeDecodeError, AttributeError, TypeError, ValueError)


class Report:
    """Imprime las líneas OK / FAIL / AVISO y cuenta los FAIL y los AVISO."""

    def __init__(self) -> None:
        self.fails = 0
        self.warns = 0

    def ok(self, text: str) -> None:
        print(f"OK {text}")

    def fail(self, text: str) -> None:
        self.fails += 1
        print(f"FAIL {text}")

    def warn(self, text: str) -> None:
        self.warns += 1
        print(f"AVISO {text}")

    def mark(self) -> tuple[int, int]:
        return self.fails, self.warns

    def clean_since(self, mark: tuple[int, int]) -> bool:
        return (self.fails, self.warns) == mark


# --- línea del método ------------------------------------------------------------

def check_line(root: Path, rep: Report) -> bool:
    """True si hay que seguir comprobando; False si la línea es anterior a 0.5.0 o ilegible."""
    cfg = root / CONFIG
    if not cfg.is_file():
        return True
    try:
        data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    except CONFIG_ERRORS as exc:
        rep.fail(f"{CONFIG}: no se puede leer ({type(exc).__name__}); no se sabe a qué línea del método pertenece")
        return False
    sdaf = data.get("sdaf") if isinstance(data, dict) else None
    version = sdaf.get("version") if isinstance(sdaf, dict) else None
    if version is None:
        return True
    match = VERSION_RE.match(str(version).strip())
    if not match:
        rep.fail(f"{CONFIG}: la versión «{version}» de sdaf.version es ilegible (se espera MAYOR.MENOR.PARCHE)")
        return False
    if tuple(int(n or 0) for n in match.groups()) < MIN_LINE:
        rep.warn(f"línea {version}: la coherencia arquitectónica es de la línea 0.5.0 (opt-in); no se comprueba nada")
        return False
    return True


# --- línea base ------------------------------------------------------------------

def load_baseline(root: Path, rep: Report) -> list[str] | None:
    """Unidades de la línea base si está Approved y se puede comprobar; None si no (ya informado)."""
    if not (root / BASELINE).is_file():
        rep.warn(f"no se comprueba la coherencia: sin línea base; G0.6 la exige ({BASELINE} no existe)")
        return None
    state = baseline(root)
    if state is None:
        rep.fail(f"{BASELINE}: no se puede leer o no es UTF-8")
        return None
    if state[0] != APPROVED:
        rep.warn(f"la línea base está en «{state[0] or 'sin Estado'}», no Approved: no se comprueba la coherencia")
        return None
    return state[1]


# --- comprobaciones --------------------------------------------------------------

def check_adrs(root: Path, rep: Report) -> int:
    """ADRs frente a la sección «Decisiones vigentes». Devuelve cuántos ADRs vigentes hay."""
    vigencia = adr_vigencia(root)
    listed = baseline_adrs(root)
    mark = rep.mark()
    for num, adr in sorted(vigencia.items()):
        if not adr.legible:
            rep.fail(f"{ADR_FOLDER}/{adr.fichero}: no se puede leer o no es UTF-8")
    vigentes = [num for num, adr in sorted(vigencia.items()) if adr.vigente]
    names = ", ".join(adr_label(n) for n in vigentes)

    if listed is None or not listed.seccion:
        extra = f": hay {len(vigentes)} ADR(s) vigente(s) ({names})" if vigentes else ""
        rep.warn(f"sección {SECTION} ausente en la línea base{extra}")
        return len(vigentes)
    if listed.na and not listed.adrs:
        if vigentes:
            rep.warn(f"la sección {SECTION} declara N/A pero hay {len(vigentes)} ADR(s) vigente(s) ({names})")
        else:
            rep.ok(f"la sección {SECTION} declara N/A y no hay ADRs vigentes")
        return len(vigentes)

    for num in listed.adrs:
        adr = vigencia.get(num)
        if adr is None:
            rep.fail(f"{adr_label(num)} figura en {SECTION} pero no existe en {ADR_FOLDER}/")
        elif not adr.legible:
            continue  # ya informado como FAIL por fichero
        elif adr.estado == "Sustituido" or adr.sustituido_por:
            by = f" (por {', '.join(adr_label(n) for n in adr.sustituido_por)})" if adr.sustituido_por else ""
            rep.fail(f"{adr_label(num)} figura en {SECTION} pero está sustituido{by}")
        elif not adr.vigente:
            estado = f"Estado «{adr.estado}»" if adr.estado else "Estado no reconocido"
            rep.warn(f"{adr_label(num)} figura en {SECTION} pero no es vigente ({estado})")
    for num in vigentes:
        if num not in listed.adrs:
            rep.warn(f"{adr_label(num)} es vigente (Aceptado y sin «Sustituido por») y no figura en {SECTION}")
    if rep.clean_since(mark):
        rep.ok(f"ADRs: {len(vigentes)} vigente(s), todos en {SECTION} y ninguno sustituido")
    return len(vigentes)


def check_stack_units(root: Path, rep: Report, units: list[str]) -> int:
    """`stack.units` frente a las unidades de la línea base. Devuelve cuántas unidades con nombre cotejó."""
    try:
        configured = load_units(root)
    except ConfigUnreadable as exc:
        rep.fail(f"{CONFIG}: no se pueden leer las unidades de código ({exc})")
        return 0
    names = [unit.name for unit in configured if unit.name]
    if not names:
        rep.ok("sin stack.units: no hay nombres que cotejar")
        return 0
    mark = rep.mark()
    for name in names:
        if name not in units:
            rep.fail(f"stack.units: la unidad «{name}» {missing_unit(units)}")
    if rep.clean_since(mark):
        rep.ok(f"stack.units: {len(names)} unidad(es) en la línea base")
    return len(names)


def missing_unit(units: list[str]) -> str:
    return (f"no figura en la línea base ({', '.join(units) or 'sin unidades'}); si es nueva, añadirla exige "
            "un ADR Aceptado y una versión nueva de la línea base (H14 §6)")


def check_specs(root: Path, rep: Report, units: list[str]) -> int:
    """Unidades que citan las specs frente a la línea base. Devuelve cuántas specs revisó."""
    reviewed = 0
    mark = rep.mark()
    for spec in spec_units(root):
        if not spec.legible:
            rep.fail(f"{spec.path}: no se puede leer o no es UTF-8")
            continue
        if spec.id is None or is_placeholder(spec.id):
            continue
        reviewed += 1
        label = f"{spec.path} ({spec.id})"
        if spec.units is None:
            rep.warn(f"{label}: sin campo «Unidades»; no se pueden cotejar sus unidades con la línea base")
            continue
        for name in spec.units:
            if name not in units:
                rep.fail(f"{label}: la unidad «{name}» {missing_unit(units)}")
    if rep.clean_since(mark):
        rep.ok(f"specs: {reviewed} spec(s) con unidades de la línea base")
    return reviewed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Comprobación mecánica de la coherencia entre línea base, ADRs, stack.units y specs (no aprueba nada).")
    parser.add_argument("--root", default=".", help="Raíz del repositorio a comprobar.")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        parser.error(f"--root «{args.root}» no es un directorio")

    rep = Report()
    if not check_line(root, rep):
        return 1 if rep.fails else 0
    units = load_baseline(root, rep)
    if units is None:
        return 1 if rep.fails else 0
    adrs = check_adrs(root, rep)
    configured = check_stack_units(root, rep, units)
    specs = check_specs(root, rep, units)
    if rep.fails:
        print(f"{rep.fails} FAIL en la coherencia arquitectónica: resuélvelos antes de seguir")
        return 1
    rep.ok(f"coherencia arquitectónica: {adrs} ADR(s) vigente(s), {configured} unidad(es) de stack.units "
           f"cotejada(s), {specs} spec(s) revisada(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
