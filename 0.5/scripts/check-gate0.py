#!/usr/bin/env python3
"""Comprobaciones MECÁNICAS de Gate 0 (G0.1, G0.2, G0.4, G0.5 y G0.6) del PBI en curso.

No decide ni aprueba nada: comprueba que los documentos que Gate 0 exige
existen, están completos y en el estado correcto. G0.3 (si el cambio toca
límites y exige ADR) es juicio humano: el comprobador solo avisa y verifica
que los ADRs citados existan y estén Aceptados. La excepción de adopción
(H05 §3, H13 §3) tampoco la relaja nunca: solo la informa.

Selección del PBI: `--pbi` (ID o ruta) o, sin él, el diff (`--changed` o git,
como check-worklog-presence.py): si toca código de producto, los PBIs de
backlog/ tocados y los que citan un worklog tocado. Nunca escribe ficheros ni
cambia estados. Sale 0 sin FAIL, 1 con algún FAIL o sin diff calculable en un
PR, 2 si el uso es erróneo.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sdaf_adrs import ESTADOS_HEREDADOS, adr_label, adr_num, file_re, refs  # noqa: E402
from sdaf_adrs import fields as adr_fields  # noqa: E402
from sdaf_diff import DiffUnavailable, git_changed, is_product, load_product_prefixes  # noqa: E402
from sdaf_docs import (  # noqa: E402
    baseline, find_pbis, frontmatter, header_fields, is_placeholder, read, section, spec_index, split_list,
)

CONFIG = "sdaf.config.yaml"
BASELINE = "architecture/description.md"
ADR_FOLDER = "architecture/decisions"
MIN_LINE = (0, 5, 0)  # el PBI de plantilla y la línea base son de la línea 0.5.0 (opt-in)
ADR_DIGITS = (3, 4)  # ancho admitido de ADR-N: 3 en el core, 3 o 4 en consumidores
APPROVED = "Approved"
ACCEPTED = "Aceptado"
INDEX_NAME = "readme.md"  # índice de backlog/: no es un PBI aunque el diff lo toque
PBI_FIELDS = ("ID", "Versión", "Estado", "Fecha", "Specs", "Acceptance", "Unidades", "ADRs", "Worklogs")
ACCEPTANCE_TITLE = r"Criterios de aceptaci[oó]n"
VERSION_RE = re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?")
CHARACTERIZATION_RE = re.compile(r"^`?caracterizaci[oó]n`?$", re.IGNORECASE)
NA_RE = re.compile(r"^N/A\s*:\s*(.*)$", re.IGNORECASE | re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]*\]\(\s*<?([^)\s>]+)>?[^)]*\)")
EXTERNAL_RE = re.compile(r"^[a-z][a-z0-9+.-]*://", re.IGNORECASE)
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
FETCH_DEPTH_HINT = "  Revisa que el checkout use fetch-depth: 0."
DIFF_ERRORS = (json.JSONDecodeError, OSError, UnicodeDecodeError)  # además de DiffUnavailable
CONFIG_ERRORS = (yaml.YAMLError, OSError, UnicodeDecodeError, AttributeError, TypeError, ValueError)


class Report:
    """Imprime las líneas OK / FAIL / AVISO y cuenta los FAIL."""

    def __init__(self) -> None:
        self.fails = 0

    def ok(self, text: str) -> None:
        print(f"OK {text}")

    def fail(self, text: str) -> None:
        self.fails += 1
        print(f"FAIL {text}")

    def warn(self, text: str) -> None:
        print(f"AVISO {text}")


@dataclass
class Pbi:
    path: Path
    label: str  # ID de la cabecera o, si no tiene, su ruta
    fields: dict[str, str]


@dataclass
class Context:
    root: Path
    specs: dict[str, list[Path]]
    adrs: dict[int, tuple[str, str | None]]  # número → (fichero, Estado; None si no es UTF-8)
    unreadable: dict[str, list[str]]  # carpeta → ficheros .md que no son UTF-8

    def rel(self, path: Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return str(path)


def norm(path: str) -> str:
    path = path.replace("\\", "/").strip()
    return path[2:] if path.startswith("./") else path


def gate(code: str, pbi: Pbi, text: str) -> str:
    return f"{code} {pbi.label}: {text}"


def has_content(block: str) -> bool:
    return any(ln.strip() and not ln.lstrip().startswith("#") for ln in block.splitlines())


def slug(title: str) -> str:
    return re.sub(r"[^\w\- ]", "", title.strip().lower()).replace(" ", "-")


def headings(text: str) -> tuple[list[tuple[int, str, int]], list[str]]:
    """(nivel, ancla GFM, línea) de cada encabezado fuera de bloques de código, y las líneas."""
    lines = text.splitlines()
    out: list[tuple[int, str, int]] = []
    seen: dict[str, int] = {}
    fenced = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        match = None if fenced else HEADING_RE.match(line)
        if match:
            base = slug(match.group(2))
            n = seen.get(base, 0)
            seen[base] = n + 1
            out.append((len(match.group(1)), base if n == 0 else f"{base}-{n}", i))
    return out, lines


def heading_body(text: str, anchor: str) -> str | None:
    """Cuerpo bajo el encabezado de esa ancla (hasta el siguiente de su nivel o superior); None si no existe."""
    found, lines = headings(text)
    for idx, (level, name, line) in enumerate(found):
        if name == anchor:
            end = next((ln for lv, _, ln in found[idx + 1:] if lv <= level), len(lines))
            return "\n".join(lines[line + 1:end])
    return None


def unreadable_md(root: Path, folder: str) -> list[str]:
    base = root / folder
    if not base.is_dir():
        return []
    return [p.relative_to(root).as_posix() for p in sorted(base.rglob("*.md")) if read(p) is None]


def adr_index(root: Path) -> dict[int, tuple[str, str | None]]:
    out: dict[int, tuple[str, str | None]] = {}
    folder = root / ADR_FOLDER
    if not folder.is_dir():
        return out
    for path in sorted(folder.glob("ADR-*.md")):
        match = file_re(ADR_DIGITS).match(path.name)
        if not match:
            continue
        text = read(path)
        estado = adr_fields(text).get("Estado") if text is not None else None
        out.setdefault(adr_num(match.group(1)), (path.name, estado))
    return out


def build_context(root: Path) -> Context:
    specs = {k: v for k, v in spec_index(root).items() if not is_placeholder(k)}
    return Context(root, specs, adr_index(root),
                   {f: unreadable_md(root, f) for f in ("specs", "backlog")})


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
        rep.warn(f"línea {version}: el PBI de plantilla y la línea base son de la línea 0.5.0 (opt-in); "
                 "no se comprueba nada")
        return False
    return True


# --- selección del PBI -----------------------------------------------------------

def load_pbi(ctx: Context, rep: Report, path: Path) -> Pbi | None:
    text = read(path)
    rel = ctx.rel(path)
    if text is None:
        rep.fail(f"G0.4 {rel}: no se puede leer o no es UTF-8")
        return None
    fields = header_fields(text)
    return Pbi(path, fields.get("ID") or rel, fields)


def select_explicit(ctx: Context, rep: Report, refs_: list[str]) -> list[Path]:
    raw = find_pbis(ctx.root)
    by_id = {k: v for k, v in raw.items() if not is_placeholder(k)}
    paths: list[Path] = []
    for ref in refs_:
        candidate = ctx.root / norm(ref)
        if ref in by_id:
            if len(by_id[ref]) > 1:
                rep.fail(f"G0.4: PBI {ref} duplicado ({', '.join(ctx.rel(p) for p in by_id[ref])}): el ID debe ser único")
                continue
            found = by_id[ref][0]
        elif candidate.is_file():
            found = candidate
        else:
            hint = f"; hay ficheros en backlog/ que no son UTF-8: {', '.join(ctx.unreadable['backlog'])}" \
                if ctx.unreadable["backlog"] else ""
            rep.fail(f"G0.4: PBI desconocido «{ref}»: no es un ID de backlog/ ni una ruta existente{hint}")
            continue
        if found not in paths:
            paths.append(found)
    return paths


def cited_worklogs(fields: dict[str, str]) -> set[str]:
    return {norm(w) for w in split_list(fields.get("Worklogs", ""))}


def select_by_diff(ctx: Context, rep: Report, args: argparse.Namespace) -> list[Path] | None:
    """PBIs en curso según el diff; None si no hay nada que comprobar (ya informado) o el diff falla."""
    root = ctx.root
    try:
        prefixes = load_product_prefixes(root)
    except CONFIG_ERRORS as exc:
        rep.fail(f"{CONFIG}: no se pueden leer las rutas de código ({type(exc).__name__})")
        return None
    if args.changed is not None:
        changed = [norm(p) for p in args.changed]
    else:
        try:
            changed = git_changed(args.base, root)
        except DiffUnavailable as exc:
            rep.fail(f"no se pudo calcular el diff del PR: {exc}")
            print(FETCH_DEPTH_HINT)
            return None
        except DIFF_ERRORS as exc:
            rep.fail(f"no se pudo calcular el diff del PR: {type(exc).__name__}: {exc}")
            return None
        if changed is None:
            rep.warn("sin diff de PR que comprobar: usa --pbi para comprobar un PBI concreto")
            return None
        changed = [norm(p) for p in changed]
    if not changed:
        rep.ok("diff vacío")
        return None
    if not any(is_product(p, prefixes) for p in changed):
        rep.ok("sin código de producto en el diff: no hay PBI que comprobar")
        return None

    touched = [root / p for p in changed if p.startswith("backlog/") and p.endswith(".md")
               and Path(p).name.lower() != INDEX_NAME and (root / p).is_file()]
    worklogs = [p for p in changed if p.startswith("worklogs/") and p.endswith(".md") and (root / p).is_file()]
    ids = set()
    for p in worklogs:
        text = read(root / p)
        pbi = (frontmatter(text) or {}).get("pbi") if text is not None else None
        if pbi:
            ids.add(str(pbi))
    paths = list(touched)
    for pbi_paths in find_pbis(root).values():
        for path in pbi_paths:
            text = read(path)
            fields = header_fields(text) if text is not None else {}
            if path not in paths and (fields.get("ID") in ids or cited_worklogs(fields) & set(worklogs)):
                paths.append(path)
    if not paths:
        rep.fail("G0.4: no hay PBI en curso (STOP): el diff toca código de producto y ningún PBI de backlog/ "
                 "ni worklog tocado lo identifica; añade el PBI o pasa --pbi")
        return None
    return paths


# --- comprobaciones por PBI ------------------------------------------------------

def check_g04(ctx: Context, rep: Report, pbi: Pbi, units: list[str] | None) -> bool:
    """Cabecera completa y unidades de la línea base. False si no hay cabecera (se omite el resto)."""
    before = rep.fails
    if not pbi.fields:
        rep.fail(gate("G0.4", pbi, "no tiene cabecera «Campo | Valor» tras el encabezado «# »"))
        return False
    for name in PBI_FIELDS:
        if name not in pbi.fields:
            rep.fail(gate("G0.4", pbi, f"falta el campo «{name}»"))
        elif is_placeholder(pbi.fields[name]):
            rep.fail(gate("G0.4", pbi, f"el campo «{name}» está vacío o conserva texto de plantilla"))
    value = pbi.fields.get("Unidades", "")
    if units is not None and not is_placeholder(value):
        for name in split_list(value) or [value]:
            if name not in units:
                rep.fail(gate("G0.4", pbi,
                              f"la unidad «{name}» no figura en la línea base ({', '.join(units) or 'sin unidades'}); "
                              "si es nueva, añadirla exige un ADR Aceptado y una versión nueva de la línea base (H14 §6)"))
    if rep.fails == before:
        rep.ok(gate("G0.4", pbi, "cabecera completa" + (" y unidades de la línea base" if units is not None else "")))
    return True


def lookup_spec(ctx: Context, sid: str) -> tuple[str, dict[str, str], str] | str:
    """(texto, cabecera, ruta relativa) de la spec o el motivo por el que no se resuelve."""
    paths = ctx.specs.get(sid, [])
    if not paths:
        bad = ctx.unreadable["specs"]
        return f"{sid} no existe en specs/" + (f" (hay ficheros que no son UTF-8: {', '.join(bad)})" if bad else "")
    if len(paths) > 1:
        return f"{sid} está duplicada ({', '.join(ctx.rel(p) for p in paths)}): el ID debe ser único"
    text = read(paths[0]) or ""
    return text, header_fields(text), ctx.rel(paths[0])


def check_g01(ctx: Context, rep: Report, pbi: Pbi) -> None:
    before = rep.fails
    value = pbi.fields.get("Specs", "")
    ids = [] if is_placeholder(value) else split_list(value)
    if not ids:
        rep.fail(gate("G0.1", pbi, "no cita ninguna spec (campo Specs vacío o de plantilla)"))
        return
    characterization = []
    for sid in ids:
        spec = lookup_spec(ctx, sid)
        if isinstance(spec, str):
            rep.fail(gate("G0.1", pbi, f"spec {spec}"))
            continue
        _, fields, _ = spec
        is_char = CHARACTERIZATION_RE.match(fields.get("Origen", "").strip()) is not None
        characterization.append(is_char)
        estado = fields.get("Estado", "")
        if estado != APPROVED:
            hint = "; la spec de caracterización exige revisión humana antes de Approved (H04 §4)" if is_char else ""
            rep.fail(gate("G0.1", pbi, f"spec {sid} está en «{estado or 'sin Estado'}», no Approved{hint}"))
    if rep.fails == before:
        rep.ok(gate("G0.1", pbi, f"{len(ids)} spec(s) Approved"))
    if len(characterization) == len(ids) and all(characterization):
        rep.warn(gate("G0.1", pbi, "todas las specs son de caracterización; sus tests no sustituyen el "
                                   "acceptance del PBI (H05 §3)"))


def check_acceptance_spec(ctx: Context, rep: Report, pbi: Pbi, sid: str) -> None:
    spec = lookup_spec(ctx, sid)
    if isinstance(spec, str):
        rep.fail(gate("G0.2", pbi, f"acceptance {spec}"))
        return
    text, fields, _ = spec
    if fields.get("Estado") != APPROVED:
        rep.fail(gate("G0.2", pbi, f"acceptance {sid} está en «{fields.get('Estado') or 'sin Estado'}», no Approved"))
    elif not has_content(section(text, ACCEPTANCE_TITLE)):
        rep.fail(gate("G0.2", pbi, f"acceptance {sid} no tiene contenido bajo «Criterios de aceptación»"))
    else:
        rep.ok(gate("G0.2", pbi, f"acceptance {sid} Approved con criterios"))


def check_acceptance_link(ctx: Context, rep: Report, pbi: Pbi, target: str) -> None:
    if EXTERNAL_RE.match(target):
        rep.warn(gate("G0.2", pbi, f"el enlace de acceptance «{target}» es externo: el comprobador no lo verifica"))
        return
    file_part, _, anchor = target.partition("#")
    file_part, anchor = unquote(file_part), unquote(anchor).lower()
    if file_part:
        options = [pbi.path.parent / norm(file_part), ctx.root / norm(file_part).lstrip("/")]
        dest = next((p for p in options if p.is_file()), None)
    else:
        dest = pbi.path
    if dest is None:
        rep.fail(gate("G0.2", pbi, f"el enlace de acceptance «{target}» apunta a un fichero que no existe"))
        return
    text = read(dest)
    if text is None:
        rep.fail(gate("G0.2", pbi, f"{ctx.rel(dest)} no se puede leer o no es UTF-8"))
        return
    body = heading_body(text, anchor) if anchor else section(text, ACCEPTANCE_TITLE)
    if body is None:
        rep.fail(gate("G0.2", pbi, f"el encabezado «#{anchor}» no existe en {ctx.rel(dest)}"))
    elif not has_content(body):
        rep.fail(gate("G0.2", pbi, f"{ctx.rel(dest)} no tiene contenido bajo «Criterios de aceptación»"))
    else:
        rep.ok(gate("G0.2", pbi, f"acceptance enlazado en {ctx.rel(dest)} con criterios"))


def check_g02(ctx: Context, rep: Report, pbi: Pbi) -> None:
    value = pbi.fields.get("Acceptance", "").replace("`", "").strip()
    if is_placeholder(value):
        rep.fail(gate("G0.2", pbi, "Acceptance está vacío o conserva texto de plantilla"))
        return
    link = LINK_RE.search(value)
    if link:
        check_acceptance_link(ctx, rep, pbi, link.group(1))
    elif "/" in value or "#" in value or value.lower().endswith(".md"):
        check_acceptance_link(ctx, rep, pbi, value)
    else:
        for sid in split_list(value) or [value]:
            check_acceptance_spec(ctx, rep, pbi, sid)


def check_g03(ctx: Context, rep: Report, pbi: Pbi) -> None:
    """ADRs citados: existen y están Aceptados. Si hace falta ADR es juicio (aviso global)."""
    value = pbi.fields.get("ADRs", "").replace("`", "").strip()
    if is_placeholder(value):
        rep.fail(gate("G0.3", pbi, "ADRs está vacío o conserva texto de plantilla (usa ADR-N o «N/A: motivo»)"))
        return
    not_applicable = NA_RE.match(value)
    if not_applicable:
        if not_applicable.group(1).strip():
            rep.ok(gate("G0.3", pbi, "ADRs declara N/A con motivo (el comprobador no juzga si basta)"))
        else:
            rep.fail(gate("G0.3", pbi, "ADRs declara N/A sin motivo"))
        return
    numbers = refs(value, ADR_DIGITS)
    if not numbers:
        rep.fail(gate("G0.3", pbi, "ADRs no cita ningún ADR-N ni «N/A: motivo»"))
        return
    before = rep.fails
    for num in numbers:
        entry = ctx.adrs.get(num)
        if entry is None:
            rep.fail(gate("G0.3", pbi, f"{adr_label(num)} no existe en {ADR_FOLDER}/"))
        elif entry[1] is None:
            rep.fail(gate("G0.3", pbi, f"{entry[0]} no se puede leer o no tiene Estado (¿no es UTF-8?)"))
        elif ESTADOS_HEREDADOS.get(entry[1].strip().casefold()) != ACCEPTED:
            rep.fail(gate("G0.3", pbi, f"{adr_label(num)} está «{entry[1]}», no Aceptado"))
    if rep.fails == before:
        rep.ok(gate("G0.3", pbi, f"{len(numbers)} ADR(s) citado(s) Aceptado(s)"))


def check_g05(ctx: Context, rep: Report, pbi: Pbi) -> None:
    value = pbi.fields.get("Worklogs", "")
    cited = [] if is_placeholder(value) else [norm(w) for w in split_list(value)]
    if not cited:
        rep.fail(gate("G0.5", pbi, "no cita ningún worklog (campo Worklogs vacío o de plantilla)"))
        return
    valid = 0
    for name in cited:
        path = ctx.root / name
        if not path.is_file():
            rep.warn(gate("G0.5", pbi, f"el worklog {name} no existe"))
            continue
        text = read(path)
        if text is None:
            rep.fail(gate("G0.5", pbi, f"{name} no se puede leer o no es UTF-8"))
            continue
        meta = frontmatter(text)
        if meta is None:
            rep.fail(gate("G0.5", pbi, f"{name} no tiene frontmatter parseable"))
            continue
        valid += 1
        if str(meta.get("estado", "")).strip() == "abortado":
            rep.warn(gate("G0.5", pbi, f"el worklog {name} está abortado"))
    if valid:
        rep.ok(gate("G0.5", pbi, f"{valid} worklog(s) con frontmatter parseable"))
    else:
        rep.fail(gate("G0.5", pbi, "ningún worklog citado existe con frontmatter parseable"))


def check_g06(root: Path, rep: Report, state: tuple[str | None, list[str], list[str]] | None) -> None:
    path = root / BASELINE
    if not path.is_file():
        rep.fail(f"G0.6: {BASELINE} no existe: falta la línea base arquitectónica Approved")
    elif state is None:
        rep.fail(f"G0.6: {BASELINE} no se puede leer o no es UTF-8")
    elif state[0] != APPROVED:
        rep.fail(f"G0.6: la línea base está en «{state[0] or 'sin Estado'}», no Approved")
    else:
        rep.ok(f"G0.6: línea base Approved ({len(state[1])} unidad(es))")


def check_pbis(ctx: Context, rep: Report, paths: list[Path]) -> None:
    """Comprueba cada PBI, la línea base (G0.6) y recuerda que G0.3 es juicio humano."""
    state = baseline(ctx.root)
    units = state[1] if state is not None else None  # sin línea base legible, G0.6 lo informa
    for path in paths:
        pbi = load_pbi(ctx, rep, path)
        if pbi is not None and check_g04(ctx, rep, pbi, units):
            check_g01(ctx, rep, pbi)
            check_g02(ctx, rep, pbi)
            check_g03(ctx, rep, pbi)
            check_g05(ctx, rep, pbi)
    check_g06(ctx.root, rep, state)
    rep.warn("G0.3 requiere juicio (H14 §6): el comprobador no decide si hace falta ADR")


def adoption_notice(root: Path) -> None:
    state = baseline(root)
    if state is not None and state[2]:
        print("AVISO excepción de adopción: la línea base declara unidades «heredada» "
              f"({', '.join(state[2])}). Si el cambio es correctivo en una unidad heredada y el ADR de excepción "
              "está Aceptado y vigente, la excepción podría aplicar (H05 §3, H13 §3). Lo decide una persona: "
              "el comprobador no relaja ningún FAIL.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Comprobaciones mecánicas de Gate 0 del PBI en curso (no aprueba nada).")
    parser.add_argument("--root", default=".", help="Raíz del repositorio a comprobar.")
    parser.add_argument("--pbi", nargs="+", metavar="ID|RUTA", help="PBIs a comprobar (anula la selección por diff).")
    parser.add_argument("--base", default=None, help="Ref git para el diff local.")
    parser.add_argument("--changed", nargs="*", metavar="RUTA", help="Lista de rutas cambiadas (modo prueba).")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        parser.error(f"--root «{args.root}» no es un directorio")

    rep = Report()
    if not check_line(root, rep):
        return 1 if rep.fails else 0
    ctx = build_context(root)
    paths = select_explicit(ctx, rep, args.pbi) if args.pbi else select_by_diff(ctx, rep, args)
    if paths:
        check_pbis(ctx, rep, paths)
        if not rep.fails:
            rep.ok(f"comprobaciones mecánicas de Gate 0 sin errores ({len(paths)} PBI): no sustituyen el juicio "
                   "humano de G0.3 ni la revisión de la persona responsable")
    if rep.fails:
        adoption_notice(root)
        print(f"{rep.fails} FAIL en las comprobaciones mecánicas de Gate 0: STOP hasta resolverlos")
    return 1 if rep.fails else 0


if __name__ == "__main__":
    sys.exit(main())
