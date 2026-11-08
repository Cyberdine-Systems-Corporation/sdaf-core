#!/usr/bin/env python3
"""Autocomprobación de la coherencia arquitectónica (check-architecture.py).

Ejecuta check-architecture.py sobre un fixture estático válido y sobre copias
mutadas en directorios temporales (fuera del repo): comprueba el código de
salida y el mensaje esperado en cada caso. Ningún caso depende del git del
repo ni de la red. El comprobador NO se ejecuta sobre el propio core; solo
esta autocomprobación (y el caso que lo lanza sin línea base para ver el aviso).
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check-architecture.py"
FIXTURE = ROOT / "scripts" / "testdata" / "architecture-valido"

BASELINE = "architecture/description.md"
DECISIONS = "architecture/decisions"
README = f"{DECISIONS}/README.md"
ADR_SUSTITUIDO = f"{DECISIONS}/ADR-002-sustituido.md"
SPEC = "specs/product/SPEC-PRD-001.md"
SPEC_ACC = "specs/acceptance/SPEC-ACC-001.md"
CONFIG = "sdaf.config.yaml"
FORBIDDEN = ("cumplido", "aprobado")  # el comprobador jamás se da por «cumplido» ni «aprobado»

SUMMARY = "OK coherencia arquitectónica: 2 ADR(s) vigente(s), 2 unidad(es) de stack.units cotejada(s), 2 spec(s) revisada(s)"
NOT_VALID_UNIT = "no figura en la línea base (Unidad A, Unidad B); si es nueva, añadirla exige un ADR Aceptado y una versión nueva de la línea base (H14 §6)"
SECTION = "«Decisiones vigentes»"

Mutation = Callable[[Path], None]


def clean_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    return env


def run(root: Path | None, *args: str) -> subprocess.CompletedProcess[str]:
    """Con `root` pasa --root; sin él ejecuta desde la raíz del repo (el propio core)."""
    cmd = [sys.executable, str(CHECKER), *(("--root", str(root)) if root is not None else ()), *args]
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=clean_env(),
                          cwd=None if root is not None else ROOT)


def expect(label: str, proc: subprocess.CompletedProcess[str], code: int,
           needles: tuple[str, ...] = (), absent: tuple[str, ...] = ()) -> bool:
    problems = []
    text = proc.stdout + proc.stderr
    if proc.returncode != code:
        problems.append(f"exit {proc.returncode} (se esperaba {code})")
    problems += [f"falta «{n}»" for n in needles if n not in text]
    problems += [f"sobra «{a}»" for a in absent if a in text]
    problems += [f"sobra «{w}»" for w in FORBIDDEN if w in proc.stdout.lower()]
    if "Traceback" in text:
        problems.append("traceback")
    if problems:
        print(f"FAIL {label}: " + "; ".join(problems))
        print(proc.stdout + proc.stderr)
        return False
    print(f"OK {label}")
    return True


@contextmanager
def tree(mutate: Mutation | None = None) -> Iterator[Path]:
    """Copia del fixture en un directorio temporal fuera del repo, con la mutación aplicada."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "repo"
        shutil.copytree(FIXTURE, root)
        if mutate:
            mutate(root)
        yield root


def case(label: str, mutate: Mutation | None, code: int, needles: tuple[str, ...] = (),
         args: tuple[str, ...] = (), absent: tuple[str, ...] = ()) -> bool:
    with tree(mutate) as root:
        return expect(label, run(root, *args), code, needles, absent)


# --- mutaciones -------------------------------------------------------------

def edit(rel: str, old: str, new: str) -> Mutation:
    def apply(root: Path) -> None:
        path = root / rel
        text = path.read_text(encoding="utf-8")
        assert old in text, f"«{old}» no está en {rel}"
        path.write_text(text.replace(old, new), encoding="utf-8", newline="\n")
    return apply


def put(rel: str, text: str) -> Mutation:
    def apply(root: Path) -> None:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    return apply


def put_bytes(rel: str, data: bytes) -> Mutation:
    def apply(root: Path) -> None:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return apply


def drop(rel: str) -> Mutation:
    return lambda root: (root / rel).unlink()


def both(*mutations: Mutation) -> Mutation:
    def apply(root: Path) -> None:
        for mutation in mutations:
            mutation(root)
    return apply


def not_utf8(rel: str) -> Mutation:
    """El fichero del fixture recodificado en cp1252 (tiene tildes, así que ya no es UTF-8)."""
    def apply(root: Path) -> None:
        text = (root / rel).read_text(encoding="utf-8")
        assert not text.isascii(), f"{rel} no tiene caracteres no ASCII"
        (root / rel).write_bytes(text.encode("cp1252"))
    return apply


def section6(body: str | None) -> Mutation:
    """Sustituye el cuerpo de «## 6. Decisiones vigentes» por `body`; con None quita la sección entera."""
    def apply(root: Path) -> None:
        path = root / BASELINE
        text = path.read_text(encoding="utf-8")
        new = "" if body is None else f"## 6. Decisiones vigentes\n\n{body}\n\n"
        text, count = re.subn(r"## 6\. Decisiones vigentes\n.*?(?=## 8\.)", new, text, flags=re.DOTALL)
        assert count == 1
        path.write_text(text, encoding="utf-8", newline="\n")
    return apply


def listing(*adrs: str) -> Mutation:
    """Sección 6 con una fila por cada texto de ADR (p. ej. «ADR-001»)."""
    rows = "\n".join(f"| {adr} | Una frase | Unidad A |" for adr in adrs)
    return section6("| ADR | Decisión | Unidades afectadas |\n|-----|----------|--------------------|\n" + rows)


def adr_text(num: int, estado: str, extra: str = "", digits: int = 3) -> str:
    return (f"# ADR-{num:0{digits}d} — Decisión de prueba\n\n| Campo | Valor |\n|--------|--------|\n"
            f"| Estado | {estado} |\n| Fecha | 2026-09-01T10:00+02:00 |\n| Decisores | Persona de prueba |\n"
            f"{extra}\n## Contexto\n\nPrueba.\n")


def adr(num: int, estado: str, extra: str = "", digits: int = 3, slug: str = "prueba") -> Mutation:
    return put(f"{DECISIONS}/ADR-{num:0{digits}d}-{slug}.md", adr_text(num, estado, extra, digits))


def units_config(*names: str) -> Mutation:
    body = "".join(f"    - name: {n}\n      src: src/{i}\n" for i, n in enumerate(names))
    return put(CONFIG, f'sdaf:\n  version: "0.5.0"\n\nstack:\n  units:\n{body}')


def spec_text(sid: str, units: str | None, estado: str = "Approved") -> str:
    row = "" if units is None else f"| Unidades | {units} |\n"
    return (f"# {sid} — Spec de prueba\n\n| Campo | Valor |\n|--------|--------|\n| ID | {sid} |\n"
            f"| Versión | 0.1.0 |\n| Estado | {estado} |\n| Fecha | 2026-09-01T10:00+02:00 |\n{row}\n"
            "## Contexto\n\nPrueba.\n")


def spec(sid: str, units: str | None, estado: str = "Approved", folder: str = "specs/product") -> Mutation:
    return put(f"{folder}/{sid}.md", spec_text(sid, units, estado))


# --- casos --------------------------------------------------------------------

def test_valid() -> bool:
    ok = True
    ok &= case("Coherencia: fixture válido", None, 0,
               ("OK ADRs: 2 vigente(s), todos en «Decisiones vigentes» y ninguno sustituido", SUMMARY,
                "OK stack.units: 2 unidad(es) en la línea base", "OK specs: 2 spec(s) con unidades de la línea base"),
               absent=("FAIL", "AVISO"))
    ok &= case("Coherencia: los ADRs se leen de los ficheros, no del índice README",
               edit(README, "| Aceptado | Aceptado vigente |", "| Sustituido | Aceptado vigente |"), 0,
               (SUMMARY,), absent=("FAIL", "AVISO"))
    ok &= case("Coherencia: sin README de ADRs", drop(README), 0, (SUMMARY,), absent=("FAIL", "AVISO"))
    return ok


def test_line() -> bool:
    ok = True
    ok &= case("Línea: sdaf.version 0.4.0 no se comprueba nada", both(
        edit(CONFIG, '"0.5.0"', '"0.4.0"'), listing("ADR-009")), 0,
        ("AVISO línea 0.4.0", "no se comprueba nada"), absent=("FAIL", "OK "))
    ok &= case("Línea: sdaf.version 0.5.0 se comprueba", edit(CONFIG, '"0.5.0"', '"0.5.1"'), 0, (SUMMARY,))
    ok &= case("Línea: config sin sdaf.version sigue comprobando", edit(CONFIG, 'sdaf:\n  version: "0.5.0"\n', "sdaf: {}\n"),
               0, (SUMMARY,), absent=("AVISO",))
    ok &= case("Línea: sin config sigue comprobando (sin stack.units)", drop(CONFIG), 0,
               ("OK sin stack.units: no hay nombres que cotejar", "0 unidad(es) de stack.units cotejada(s)"),
               absent=("FAIL", "AVISO"))
    ok &= case("Línea: config con YAML roto", put(CONFIG, "stack: [\n"), 1,
               (f"FAIL {CONFIG}: no se puede leer", "no se sabe a qué línea del método pertenece"), absent=("OK ",))
    ok &= case("Línea: config que no es UTF-8", put_bytes(CONFIG, "sdaf: {version: '0.5.0'}  # ñ\n".encode("cp1252")), 1,
               (f"FAIL {CONFIG}: no se puede leer",))
    ok &= case("Línea: sdaf.version ilegible", edit(CONFIG, '"0.5.0"', '"abc"'), 1,
               (f"FAIL {CONFIG}: la versión «abc» de sdaf.version es ilegible",))
    ok &= case("Línea: stack no es un mapa", put(CONFIG, 'sdaf:\n  version: "0.5.0"\nstack: [1]\n'), 1,
               (f"FAIL {CONFIG}: no se pueden leer las unidades de código", "«stack» no es un mapa"), absent=("OK coherencia",))
    return ok


def test_baseline() -> bool:
    ok = True
    ok &= case("Línea base: ausente", drop(BASELINE), 0,
               ("AVISO no se comprueba la coherencia: sin línea base; G0.6 la exige",), absent=("FAIL", "OK "))
    ok &= case("Línea base: ausente aunque haya incoherencias", both(drop(BASELINE), units_config("Unidad Z")), 0,
               ("sin línea base",), absent=("FAIL",))
    ok &= case("Línea base: Draft no se comprueba", both(
        edit(BASELINE, "| Estado | Approved |", "| Estado | Draft |"), units_config("Unidad Z"), listing("ADR-002")), 0,
        ("AVISO la línea base está en «Draft», no Approved: no se comprueba la coherencia",), absent=("FAIL", "OK "))
    ok &= case("Línea base: sin Estado no se comprueba", edit(BASELINE, "| Estado | Approved |\n", ""), 0,
               ("AVISO la línea base está en «sin Estado», no Approved",), absent=("FAIL",))
    ok &= case("Línea base: que no es UTF-8", not_utf8(BASELINE), 1,
               (f"FAIL {BASELINE}: no se puede leer o no es UTF-8",), absent=("OK ",))
    return ok


def test_adrs() -> bool:
    ok = True
    ok &= case("ADRs: vigente omitido de la sección 6 (AVISO)", listing("ADR-001"), 0,
               ("AVISO ADR-003 es vigente (Aceptado y sin «Sustituido por») y no figura en «Decisiones vigentes»",
                SUMMARY), absent=("FAIL",))
    ok &= case("ADRs: sustituido listado (FAIL)", listing("ADR-001", "ADR-002", "ADR-003"), 1,
               ("FAIL ADR-002 figura en «Decisiones vigentes» pero está sustituido",), absent=("AVISO", "OK coherencia"))
    ok &= case("ADRs: ADR Aceptado con «Sustituido por» listado (FAIL)", both(
        edit(f"{DECISIONS}/ADR-001-aceptado.md", "| Decisores |", "| Sustituido por | [ADR-003](ADR-003-sucesor.md) |\n| Decisores |")), 1,
        ("FAIL ADR-001 figura en «Decisiones vigentes» pero está sustituido",))
    ok &= case("ADRs: Aceptado con «Sustituido por» no listado no es vigente (sin ruido)", both(
        edit(f"{DECISIONS}/ADR-001-aceptado.md", "| Decisores |", "| Sustituido por | [ADR-003](ADR-003-sucesor.md) |\n| Decisores |"),
        listing("ADR-003")), 0, ("1 ADR(s) vigente(s)",), absent=("FAIL", "AVISO"))
    ok &= case("ADRs: estado heredado Superseded listado (FAIL)", both(
        edit(ADR_SUSTITUIDO, "| Estado | Sustituido |", "| Estado | Superseded |"), listing("ADR-001", "ADR-002", "ADR-003")), 1,
        ("FAIL ADR-002 figura en «Decisiones vigentes» pero está sustituido",))
    ok &= case("ADRs: inexistente listado (FAIL)", listing("ADR-001", "ADR-003", "ADR-009"), 1,
               (f"FAIL ADR-009 figura en «Decisiones vigentes» pero no existe en {DECISIONS}/",))
    ok &= case("ADRs: Rechazado listado (AVISO)", both(adr(4, "Rechazado"), listing("ADR-001", "ADR-003", "ADR-004")), 0,
               ("AVISO ADR-004 figura en «Decisiones vigentes» pero no es vigente (Estado «Rechazado»)", SUMMARY),
               absent=("FAIL",))
    ok &= case("ADRs: Propuesto listado (AVISO)", both(adr(4, "Propuesto"), listing("ADR-001", "ADR-003", "ADR-004")), 0,
               ("AVISO ADR-004 figura en «Decisiones vigentes» pero no es vigente (Estado «Propuesto»)",), absent=("FAIL",))
    ok &= case("ADRs: Deprecado listado (AVISO)", both(adr(4, "Deprecado"), listing("ADR-001", "ADR-003", "ADR-004")), 0,
               ("AVISO ADR-004 figura en «Decisiones vigentes» pero no es vigente (Estado «Deprecado»)",), absent=("FAIL",))
    ok &= case("ADRs: Estado no reconocido listado (AVISO)", both(adr(4, "Raro"), listing("ADR-001", "ADR-003", "ADR-004")), 0,
               ("AVISO ADR-004 figura en «Decisiones vigentes» pero no es vigente (Estado no reconocido)",), absent=("FAIL",))
    ok &= case("ADRs: Rechazado no listado no es vigente (sin ruido)", adr(4, "Rechazado"), 0, (SUMMARY,),
               absent=("FAIL", "AVISO"))
    ok &= case("ADRs: Deprecado no listado no es vigente (sin ruido)", adr(4, "Deprecado"), 0, (SUMMARY,),
               absent=("FAIL", "AVISO"))
    ok &= case("ADRs: la tabla de plantilla sin rellenar no lista nada", section6(
        "| ADR | Decisión | Unidades afectadas |\n|-----|----------|--------------------|\n| ADR-NNN | Una frase | Unidad A |"), 0,
        ("AVISO ADR-001 es vigente", "AVISO ADR-003 es vigente"), absent=("FAIL",))
    return ok


def test_section6() -> bool:
    ok = True
    ok &= case("Sección 6: ausente con ADRs vigentes (AVISO)", section6(None), 0,
               ("AVISO sección «Decisiones vigentes» ausente en la línea base: hay 2 ADR(s) vigente(s) (ADR-001, ADR-003)",),
               absent=("FAIL",))
    ok &= case("Sección 6: ausente sin ADRs vigentes", both(section6(None), edit(
        f"{DECISIONS}/ADR-001-aceptado.md", "| Estado | Aceptado |", "| Estado | Rechazado |"), edit(
        f"{DECISIONS}/ADR-003-sucesor.md", "| Estado | Aceptado |", "| Estado | Rechazado |")), 0,
        ("AVISO sección «Decisiones vigentes» ausente en la línea base", ), absent=("FAIL", "hay "))
    ok &= case("Sección 6: N/A con ADRs vigentes (AVISO)", section6("`N/A: sin decisiones de arquitectura`"), 0,
               ("AVISO la sección «Decisiones vigentes» declara N/A pero hay 2 ADR(s) vigente(s) (ADR-001, ADR-003)",),
               absent=("FAIL",))
    no_vigentes = both(
        edit(f"{DECISIONS}/ADR-001-aceptado.md", "| Estado | Aceptado |", "| Estado | Rechazado |"),
        edit(f"{DECISIONS}/ADR-003-sucesor.md", "| Estado | Aceptado |", "| Estado | Rechazado |"))
    ok &= case("Sección 6: N/A sin ADRs vigentes (OK)", both(no_vigentes, section6("`N/A: sin decisiones de arquitectura`")), 0,
               ("OK la sección «Decisiones vigentes» declara N/A y no hay ADRs vigentes",), absent=("FAIL", "AVISO"))
    ok &= case("Sección 6: sin ADRs en el repo y N/A (OK)", both(
        section6("`N/A: ninguna`"), drop(f"{DECISIONS}/ADR-001-aceptado.md"), drop(ADR_SUSTITUIDO),
        drop(f"{DECISIONS}/ADR-003-sucesor.md")), 0,
        ("OK la sección «Decisiones vigentes» declara N/A y no hay ADRs vigentes", "0 ADR(s) vigente(s)"),
        absent=("FAIL", "AVISO"))
    return ok


def test_legacy_and_digits() -> bool:
    ok = True
    ok &= case("ADRs: estado heredado Accepted cuenta como vigente (omitido: AVISO)", adr(4, "Accepted"), 0,
               ("AVISO ADR-004 es vigente",), absent=("FAIL",))
    ok &= case("ADRs: estado heredado Accepted listado (OK, 3 vigentes)", both(
        adr(4, "Accepted"), listing("ADR-001", "ADR-003", "ADR-004")), 0,
        ("3 ADR(s) vigente(s)",), absent=("FAIL", "AVISO"))
    ok &= case("ADRs: estado heredado Aceptada (femenino) cuenta como vigente", adr(4, "aceptada"), 0,
               ("AVISO ADR-004 es vigente",))
    ok &= case("ADRs: ADR de 4 dígitos listado con 4 dígitos (OK)", both(
        adr(4, "Aceptado", digits=4), listing("ADR-001", "ADR-003", "ADR-0004")), 0,
        ("3 ADR(s) vigente(s)",), absent=("FAIL", "AVISO"))
    ok &= case("ADRs: ADR de 4 dígitos listado con 3 dígitos (OK)", both(
        adr(4, "Aceptado", digits=4), listing("ADR-001", "ADR-003", "ADR-004")), 0,
        ("3 ADR(s) vigente(s)",), absent=("FAIL", "AVISO"))
    ok &= case("ADRs: ADR de 4 dígitos omitido (AVISO)", adr(4, "Aceptado", digits=4), 0,
               ("AVISO ADR-004 es vigente",))
    ok &= case("ADRs: ADR de 4 dígitos sustituido listado (FAIL)", both(
        adr(4, "Sustituido", "| Sustituido por | ADR-0005 |\n", digits=4), listing("ADR-001", "ADR-003", "ADR-0004")), 1,
        ("FAIL ADR-004 figura en «Decisiones vigentes» pero está sustituido",))
    return ok


def test_adr_encoding() -> bool:
    ok = True
    ok &= case("ADRs: fichero que no es UTF-8 (FAIL por fichero)", not_utf8(ADR_SUSTITUIDO), 1,
               (f"FAIL {ADR_SUSTITUIDO}: no se puede leer o no es UTF-8",), absent=("OK coherencia",))
    ok &= case("ADRs: fichero listado que no es UTF-8 (un único FAIL)", not_utf8(f"{DECISIONS}/ADR-001-aceptado.md"), 1,
               (f"FAIL {DECISIONS}/ADR-001-aceptado.md: no se puede leer o no es UTF-8",), absent=("sustituido", "no existe"))
    return ok


def test_units() -> bool:
    ok = True
    ok &= case("Unidades: unidad de stack.units que no está en la línea base (FAIL)", units_config("Unidad A", "Unidad Z"), 1,
               (f"FAIL stack.units: la unidad «Unidad Z» {NOT_VALID_UNIT}",), absent=("OK coherencia",))
    ok &= case("Unidades: varias, una mala (un solo FAIL, cita la mala)", units_config("Unidad A", "Unidad Z", "Unidad B"), 1,
               ("«Unidad Z»",), absent=("«Unidad A» no figura", "«Unidad B» no figura"))
    ok &= case("Unidades: dos malas (dos FAIL)", units_config("Unidad Y", "Unidad Z"), 1,
               ("«Unidad Y»", "«Unidad Z»"))
    ok &= case("Unidades: comparación exacta (distinto en mayúsculas)", units_config("unidad a"), 1,
               ("FAIL stack.units: la unidad «unidad a»",))
    ok &= case("Unidades: todas existen", units_config("Unidad B", "Unidad A"), 0, (SUMMARY,))
    ok &= case("Unidades: atajo src_path/tests_path sin nombres (OK)",
               put(CONFIG, 'sdaf:\n  version: "0.5.0"\n\nstack:\n  src_path: src\n  tests_path: tests\n'), 0,
               ("OK sin stack.units: no hay nombres que cotejar",), absent=("FAIL", "AVISO"))
    ok &= case("Unidades: línea base sin tabla de unidades y unidad con nombre (FAIL)", both(
        edit(BASELINE, "| Unidad A | Tipo libre | Código anterior a la adopción (heredada) |\n"
                       "| Unidad B | Tipo libre | Unidad gobernada de prueba |\n", "")), 1,
        ("FAIL stack.units: la unidad «Unidad A» no figura en la línea base (sin unidades)",))
    return ok


def test_specs() -> bool:
    ok = True
    ok &= case("Specs: unidad inexistente (FAIL por spec y unidad)", spec("SPEC-PRD-001", "Unidad A, Unidad Z"), 1,
               (f"FAIL {SPEC} (SPEC-PRD-001): la unidad «Unidad Z» {NOT_VALID_UNIT}",), absent=("OK coherencia",))
    ok &= case("Specs: comparación exacta (distinto en mayúsculas)", spec("SPEC-PRD-001", "unidad a"), 1,
               (f"FAIL {SPEC} (SPEC-PRD-001): la unidad «unidad a»",))
    ok &= case("Specs: dos unidades inexistentes en dos specs", both(
        spec("SPEC-PRD-001", "Unidad Y"), spec("SPEC-ACC-001", "Unidad Z", folder="specs/acceptance")), 1,
        (f"FAIL {SPEC} (SPEC-PRD-001): la unidad «Unidad Y»", f"FAIL {SPEC_ACC} (SPEC-ACC-001): la unidad «Unidad Z»"))
    ok &= case("Specs: sin campo Unidades (AVISO)", spec("SPEC-PRD-001", None), 0,
               (f"AVISO {SPEC} (SPEC-PRD-001): sin campo «Unidades»", "2 spec(s) revisada(s)"), absent=("FAIL",))
    ok &= case("Specs: spec con ID de plantilla se ignora aunque cite una unidad mala",
               spec("SPEC-XXX-000", "Unidad Z"), 0, ("2 spec(s) revisada(s)",), absent=("FAIL", "AVISO"))
    ok &= case("Specs: spec con ID de plantilla y sin Unidades se ignora", spec("SPEC-XXX-000", None), 0,
               ("2 spec(s) revisada(s)",), absent=("FAIL", "AVISO"))
    ok &= case("Specs: campo Unidades solo con placeholders se ignora sin ruido",
               spec("SPEC-PRD-001", "<nombres exactos de la línea base>"), 0, (SUMMARY,), absent=("FAIL", "AVISO"))
    ok &= case("Specs: placeholder junto a una unidad válida", spec("SPEC-PRD-001", "<unidad>, Unidad A"), 0, (SUMMARY,),
               absent=("FAIL", "AVISO"))
    ok &= case("Specs: se comprueban también las Draft", spec("SPEC-PRD-001", "Unidad Z", estado="Draft"), 1,
               (f"FAIL {SPEC} (SPEC-PRD-001): la unidad «Unidad Z»",))
    ok &= case("Specs: se comprueban las de subcarpetas de specs/", spec("SPEC-EXT-001", "Unidad Z", folder="specs/otra/anidada"), 1,
               ("FAIL specs/otra/anidada/SPEC-EXT-001.md (SPEC-EXT-001): la unidad «Unidad Z»",))
    ok &= case("Specs: un .md de specs/ sin ID no es una spec", put("specs/NOTAS.md", "# Notas\n\nSin cabecera.\n"), 0,
               ("2 spec(s) revisada(s)",), absent=("FAIL", "AVISO"))
    ok &= case("Specs: fichero que no es UTF-8 (FAIL por fichero)", both(
        spec("SPEC-PRD-001", "Unidad A"), not_utf8(SPEC)), 1,
        (f"FAIL {SPEC}: no se puede leer o no es UTF-8",), absent=("OK coherencia",))
    ok &= case("Specs: sin carpeta specs/ (0 revisadas)", lambda root: shutil.rmtree(root / "specs"), 0,
               ("0 spec(s) revisada(s)",), absent=("FAIL", "AVISO"))
    return ok


def test_cli() -> bool:
    ok = True
    with tree() as root:
        ok &= expect("CLI: --root que no es un directorio", run(root / BASELINE), 2, ("no es un directorio",),
                     absent=("OK ",))
        ok &= expect("CLI: --root inexistente", run(root / "no-existe"), 2, ("no es un directorio",))
        ok &= expect("CLI: la salida nunca contiene Traceback ni palabras de aprobación",
                     run(root), 0, (SUMMARY,))
    ok &= expect("CLI: el propio core sin --root no tiene línea base (AVISO, salida 0)", run(None), 0,
                 ("AVISO no se comprueba la coherencia: sin línea base; G0.6 la exige",), absent=("FAIL", "OK "))
    return ok


def main() -> int:
    results = [test_valid(), test_line(), test_baseline(), test_adrs(), test_section6(), test_legacy_and_digits(),
               test_adr_encoding(), test_units(), test_specs(), test_cli()]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
