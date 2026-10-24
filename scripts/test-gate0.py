#!/usr/bin/env python3
"""Autocomprobación de las comprobaciones mecánicas de Gate 0 (check-gate0.py).

Ejecuta check-gate0.py sobre un fixture estático válido y sobre copias
mutadas en directorios temporales (fuera del repo): comprueba el código de
salida y el mensaje esperado en cada caso. Los casos de diff por git usan un
repositorio temporal propio; ningún caso depende del git del repo ni de la red.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE0 = ROOT / "scripts" / "check-gate0.py"
FIXTURE = ROOT / "scripts" / "testdata" / "gate0-valido"

PBI = "backlog/PBI-PRD-001.md"
SPEC = "specs/product/SPEC-PRD-001.md"
ACCEPTANCE = "specs/acceptance/SPEC-ACC-001.md"
BASELINE = "architecture/description.md"
ADR = "architecture/decisions/ADR-001-prueba.md"
WORKLOG = "worklogs/unidad-a/Iteration-001.md"
CONFIG = "sdaf.config.yaml"
PBI_ARGS = ("--pbi", "PBI-PRD-001")
GIT_ENV_VARS = ("GITHUB_EVENT_NAME", "GITHUB_EVENT_PATH", "GITHUB_BASE_SHA")
FORBIDDEN = ("cumplido", "aprobado")  # el comprobador jamás se da por «Gate 0 cumplido»

Mutation = Callable[[Path], None]


def clean_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k not in GIT_ENV_VARS}
    env["PYTHONUTF8"] = "1"
    return env


def run(root: Path, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(GATE0), "--root", str(root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env or clean_env(),
    )


def expect(label: str, proc: subprocess.CompletedProcess[str], code: int,
           needles: tuple[str, ...] = (), absent: tuple[str, ...] = ()) -> bool:
    problems = []
    if proc.returncode != code:
        problems.append(f"exit {proc.returncode} (se esperaba {code})")
    problems += [f"falta «{n}»" for n in needles if n not in proc.stdout]
    problems += [f"sobra «{a}»" for a in absent if a in proc.stdout]
    problems += [f"sobra «{w}»" for w in FORBIDDEN if w in proc.stdout.lower()]
    if "Traceback" in proc.stderr or "Traceback" in proc.stdout:
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
         args: tuple[str, ...] = PBI_ARGS, absent: tuple[str, ...] = ()) -> bool:
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


def drop(rel: str) -> Mutation:
    return lambda root: (root / rel).unlink()


def both(*mutations: Mutation) -> Mutation:
    def apply(root: Path) -> None:
        for mutation in mutations:
            mutation(root)
    return apply


def acceptance_link(target: str) -> Mutation:
    return edit(PBI, "| Acceptance | SPEC-ACC-001 |", f"| Acceptance | [criterios]({target}) |")


# --- casos --------------------------------------------------------------------

def test_valid() -> bool:
    ok = True
    with tree() as root:
        proc = run(root, *PBI_ARGS)
        ok &= expect("Gate 0: fixture válido por ID", proc, 0,
                     ("OK ", "comprobaciones mecánicas", "AVISO G0.3 requiere juicio (H14 §6): "
                      "el comprobador no decide si hace falta ADR"),
                     absent=("FAIL", "excepción de adopción"))
        ok &= expect("Gate 0: selección por ruta", run(root, "--pbi", PBI), 0, ("PBI-PRD-001",), absent=("FAIL",))
        ok &= expect("Gate 0: selección por backlog tocado en el diff",
                     run(root, "--changed", "src/a.py", PBI), 0, ("PBI-PRD-001",), absent=("FAIL",))
        ok &= expect("Gate 0: selección por worklog tocado (Worklogs y pbi: del frontmatter)",
                     run(root, "--changed", "src/a.py", WORKLOG), 0, ("PBI-PRD-001",), absent=("FAIL",))
        ok &= expect("Gate 0: diff sin código de producto", run(root, "--changed", "docs/nota.md"), 0,
                     ("OK sin código de producto",), absent=("G0.",))
        ok &= expect("Gate 0: diff vacío", run(root, "--changed"), 0, ("OK diff vacío",))
        ok &= expect("Gate 0: sin diff fuera de un PR", run(root), 0, ("AVISO sin diff",), absent=("FAIL",))
    return ok


def test_git_diff() -> bool:
    ok = True
    git = ["git", "-c", "user.name=Persona de prueba", "-c", "user.email=prueba@example.invalid"]
    with tree() as root:
        def sh(*cmd: str) -> str:
            return subprocess.run([*git, *cmd], cwd=root, capture_output=True, text=True, encoding="utf-8",
                                  check=True).stdout.strip()

        sh("init", "-q")
        sh("add", "-A")
        sh("commit", "-q", "-m", "base")
        base = sh("rev-parse", "HEAD")
        (root / "src").mkdir()
        (root / "src" / "a.py").write_text("x = 1\n", encoding="utf-8")
        (root / WORKLOG).write_text((root / WORKLOG).read_text(encoding="utf-8") + "\nCambio.\n", encoding="utf-8")
        sh("add", "-A")
        sh("commit", "-q", "-m", "cambio")
        ok &= expect("Gate 0: diff por git (--base) elige el PBI del worklog tocado",
                     run(root, "--base", base), 0, ("PBI-PRD-001",), absent=("FAIL",))
        ok &= expect("Gate 0: --base que git no resuelve", run(root, "--base", "no-existe"), 1,
                     ("FAIL no se pudo calcular el diff",))
        event = Path(root).parent / "event.json"
        event.write_text("{no es json", encoding="utf-8")
        env = {**clean_env(), "GITHUB_EVENT_NAME": "pull_request", "GITHUB_EVENT_PATH": str(event)}
        ok &= expect("Gate 0: evento de PR ilegible", run(root, env=env), 1, ("FAIL no se pudo calcular el diff",))
    return ok


def test_selection() -> bool:
    ok = True
    ok &= case("Gate 0: sin PBI en curso", None, 1, ("FAIL G0.4: no hay PBI en curso",),
               args=("--changed", "src/a.py", "docs/nota.md"))
    ok &= case("Gate 0: el índice de backlog/ tocado no es un PBI", put("backlog/README.md", "# Backlog\n"), 1,
               ("FAIL G0.4: no hay PBI en curso",), args=("--changed", "src/a.py", "backlog/README.md"))
    ok &= case("Gate 0: --pbi desconocido", None, 1, ("FAIL", "PBI-NO-EXISTE"), args=("--pbi", "PBI-NO-EXISTE"))
    ok &= case("Gate 0: --pbi con ruta inexistente", None, 1, ("FAIL", "backlog/nada.md"),
               args=("--pbi", "backlog/nada.md"))
    ok &= case("Gate 0: uso erróneo de argumentos", None, 2, args=("--no-existe",))
    return ok


def test_line() -> bool:
    ok = True
    ok &= case("Gate 0: línea 0.4.x avisa y no comprueba nada", both(
        edit(CONFIG, '"0.5.0"', '"0.4.0"'), drop(BASELINE), drop(PBI)), 0, ("AVISO", "0.5.0"),
        absent=("FAIL", "G0.6"))
    ok &= case("Gate 0: versión ilegible", edit(CONFIG, '"0.5.0"', '"cinco"'), 1, ("FAIL", "versión"))
    ok &= case("Gate 0: config YAML inválido", put(CONFIG, "sdaf: [sin cerrar\n"), 1, ("FAIL", CONFIG))
    ok &= case("Gate 0: sin config se asume la línea 0.5.0", drop(CONFIG), 0, absent=("FAIL", "AVISO línea"))
    return ok


def test_g04() -> bool:
    ok = True
    ok &= case("Gate 0: campo de cabecera ausente", edit(PBI, "| Worklogs | `worklogs/unidad-a/Iteration-001.md` |\n", ""),
               1, ("FAIL G0.4", "Worklogs"))
    ok &= case("Gate 0: campo de cabecera con texto de plantilla",
               edit(PBI, "2026-09-01T10:00+02:00", "YYYY-MM-DDThh:mm±hh:mm"), 1, ("FAIL G0.4", "Fecha"))
    ok &= case("Gate 0: PBI sin cabecera (sin encabezado #)", put(PBI, "Sin cabecera.\n"), 1, ("FAIL G0.4", "cabecera"),
               args=("--pbi", PBI))
    ok &= case("Gate 0: unidad ausente de la línea base", edit(PBI, "Unidad A, Unidad B", "Unidad A, Unidad C"), 1,
               ("FAIL G0.4", "Unidad C", "H14 §6"))
    ok &= case("Gate 0: unidades en minúscula no coinciden (nombre exacto)",
               edit(PBI, "Unidad A, Unidad B", "unidad a"), 1, ("FAIL G0.4", "unidad a"))
    return ok


def test_g01() -> bool:
    ok = True
    ok &= case("Gate 0: spec en Draft", edit(SPEC, "| Estado | Approved |", "| Estado | Draft |"), 1,
               ("FAIL G0.1", "SPEC-PRD-001", "Draft"))
    ok &= case("Gate 0: spec inexistente", drop(SPEC), 1, ("FAIL G0.1", "SPEC-PRD-001", "no existe"))
    ok &= case("Gate 0: spec duplicada", put("specs/product/copia.md", (FIXTURE / SPEC).read_text(encoding="utf-8")),
               1, ("FAIL G0.1", "SPEC-PRD-001", "duplicad"))
    caracterizacion = edit(SPEC, "| Unidades | Unidad A, Unidad B |", "| Unidades | Unidad A, Unidad B |\n| Origen | `caracterización` |")
    ok &= case("Gate 0: caracterización en Draft",
               both(caracterizacion, edit(SPEC, "| Estado | Approved |", "| Estado | Draft |")), 1,
               ("FAIL G0.1", "exige revisión humana antes de Approved (H04 §4)"))
    ok &= case("Gate 0: caracterización Approved cuenta, con aviso", caracterizacion, 0,
               ("AVISO G0.1", "caracterización"), absent=("FAIL",))
    ok &= case("Gate 0: spec sin ID entre las del PBI sigue siendo inexistente",
               edit(SPEC, "| ID | SPEC-PRD-001 |", "| ID | SPEC-XXX-000 |"), 1, ("FAIL G0.1", "no existe"))
    return ok


def test_g02() -> bool:
    ok = True
    ok &= case("Gate 0: PBI sin acceptance", edit(PBI, "| Acceptance | SPEC-ACC-001 |", "| Acceptance | |"), 1,
               ("FAIL G0.2",))
    ok &= case("Gate 0: acceptance con texto de plantilla",
               edit(PBI, "| Acceptance | SPEC-ACC-001 |", "| Acceptance | SPEC-ACC-000 o enlace a la sección de acceptance |"),
               1, ("FAIL G0.2",))
    ok &= case("Gate 0: acceptance por ID en Draft",
               edit(ACCEPTANCE, "| Estado | Approved |", "| Estado | Draft |"), 1, ("FAIL G0.2", "SPEC-ACC-001", "Draft"))
    ok &= case("Gate 0: acceptance por ID inexistente", drop(ACCEPTANCE), 1, ("FAIL G0.2", "no existe"))
    ok &= case("Gate 0: acceptance sin contenido bajo «Criterios de aceptación»",
               edit(ACCEPTANCE, "Dado un estado inicial, cuando ocurre un evento, entonces se observa un resultado medible.", ""),
               1, ("FAIL G0.2", "Criterios de aceptación"))
    ok &= case("Gate 0: acceptance como enlace con ancla", acceptance_link(
        "../specs/acceptance/SPEC-ACC-001.md#criterios-de-aceptación"), 0, absent=("FAIL",))
    ok &= case("Gate 0: acceptance como enlace sin ancla", acceptance_link("../specs/acceptance/SPEC-ACC-001.md"), 0,
               absent=("FAIL",))
    ok &= case("Gate 0: enlace de acceptance con ancla inexistente",
               acceptance_link("../specs/acceptance/SPEC-ACC-001.md#no-existe"), 1, ("FAIL G0.2", "no-existe"))
    ok &= case("Gate 0: enlace de acceptance a un fichero inexistente",
               acceptance_link("../specs/acceptance/nada.md"), 1, ("FAIL G0.2", "nada.md"))
    return ok


def test_g03() -> bool:
    ok = True
    ok &= case("Gate 0: ADR en Propuesto", edit(ADR, "| Estado | Aceptado |", "| Estado | Propuesto |"), 1,
               ("FAIL G0.3", "ADR-001", "Propuesto"))
    ok &= case("Gate 0: ADR inexistente", drop(ADR), 1, ("FAIL G0.3", "ADR-001", "no existe"))
    ok &= case("Gate 0: ADR citado con 4 dígitos se normaliza", edit(PBI, "| ADRs | ADR-001 |", "| ADRs | ADR-0001 |"), 0,
               absent=("FAIL",))
    ok &= case("Gate 0: ADRs con N/A y motivo", edit(PBI, "| ADRs | ADR-001 |", "| ADRs | N/A: no toca límites |"), 0,
               ("AVISO G0.3 requiere juicio",), absent=("FAIL",))
    ok &= case("Gate 0: ADRs con N/A sin motivo", edit(PBI, "| ADRs | ADR-001 |", "| ADRs | N/A: |"), 1, ("FAIL G0.3",))
    ok &= case("Gate 0: ADRs sin ADR ni N/A", edit(PBI, "| ADRs | ADR-001 |", "| ADRs | pendiente |"), 1, ("FAIL G0.3",))
    ok &= case("Gate 0: ADRs vacío", edit(PBI, "| ADRs | ADR-001 |", "| ADRs | |"), 1, ("FAIL G0.3",))
    return ok


def test_g05() -> bool:
    ok = True
    ok &= case("Gate 0: worklog ausente", drop(WORKLOG), 1, ("FAIL G0.5",))
    ok &= case("Gate 0: worklog sin frontmatter", put(WORKLOG, "# Sin frontmatter\n"), 1, ("FAIL G0.5", "frontmatter"))
    ok &= case("Gate 0: una ruta ausente y otra presente avisa",
               edit(PBI, "| Worklogs | `worklogs/unidad-a/Iteration-001.md` |",
                    "| Worklogs | `worklogs/unidad-a/Iteration-001.md`, `worklogs/unidad-a/Iteration-002.md` |"),
               0, ("AVISO G0.5", "Iteration-002"), absent=("FAIL",))
    ok &= case("Gate 0: worklog abortado avisa", edit(WORKLOG, "estado: en_curso", "estado: abortado"), 0,
               ("AVISO G0.5", "abortado"), absent=("FAIL",))
    return ok


def test_g06() -> bool:
    ok = True
    ok &= case("Gate 0: línea base en Draft", edit(BASELINE, "| Estado | Approved |", "| Estado | Draft |"), 1,
               ("FAIL G0.6", "Draft"))
    ok &= case("Gate 0: línea base ausente", drop(BASELINE), 1, ("FAIL G0.6", "no existe"))
    ok &= case("Gate 0: línea base ausente no tapa las demás comprobaciones",
               both(drop(BASELINE), edit(PBI, "| Acceptance | SPEC-ACC-001 |", "| Acceptance | |")), 1,
               ("FAIL G0.6", "FAIL G0.2"))
    return ok


def test_adoption_exception() -> bool:
    ok = True
    ok &= case("Gate 0: excepción de adopción solo se informa, nunca relaja el FAIL",
               edit(BASELINE, "| Estado | Approved |", "| Estado | Draft |"), 1,
               ("FAIL G0.6", "AVISO excepción de adopción", "Lo decide una persona"))
    ok &= case("Gate 0: sin unidades heredadas no hay aviso de excepción",
               both(edit(BASELINE, "(heredada)", ""), edit(BASELINE, "| Estado | Approved |", "| Estado | Draft |")),
               1, ("FAIL G0.6",), absent=("excepción de adopción",))
    return ok


def test_encoding() -> bool:
    ok = True
    ok &= case("Gate 0: PBI que no es UTF-8", lambda root: (root / PBI).write_bytes(
        (FIXTURE / PBI).read_text(encoding="utf-8").replace("Prueba", "Pruebá").encode("cp1252")), 1,
        ("FAIL", "no es UTF-8"), args=("--pbi", PBI))
    ok &= case("Gate 0: PBI que no es UTF-8 elegido por ID", lambda root: (root / PBI).write_bytes(
        (FIXTURE / PBI).read_text(encoding="utf-8").replace("Prueba", "Pruebá").encode("cp1252")), 1,
        ("FAIL", "no son UTF-8"))
    ok &= case("Gate 0: línea base que no es UTF-8", lambda root: (root / BASELINE).write_bytes(
        (FIXTURE / BASELINE).read_text(encoding="utf-8").replace("Código", "Códigó").encode("cp1252")), 1,
        ("FAIL G0.6", "no es UTF-8"))
    return ok


def main() -> int:
    results = [test_valid(), test_git_diff(), test_selection(), test_line(), test_g04(), test_g01(), test_g02(),
               test_g03(), test_g05(), test_g06(), test_adoption_exception(), test_encoding()]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
