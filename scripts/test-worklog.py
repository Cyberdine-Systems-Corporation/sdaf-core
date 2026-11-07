#!/usr/bin/env python3
"""Comprueba worklog schema (nuevo y tabla vigente) y presencia de worklog."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VW = ROOT / "scripts" / "validate-worklog.py"
PRE = ROOT / "scripts" / "check-worklog-presence.py"


def run(
    script: Path, args: list[str], env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


UNITS_CONFIG = (
    "stack:\n  units:\n    - name: Unidad A\n      src: apps/api\n      tests: tests/api\n"
    "    - name: Unidad B\n      src: libs/core\n"
)
WORKLOG_FILE = "worklogs/PBI-001/Iteration-001.md"


def check_presence(label: str, config: str | None, changed: list[str], code: int,
                   needles: tuple[str, ...] = (), absent: tuple[str, ...] = ()) -> bool:
    """Ejecuta check-worklog-presence.py con --cwd en un consumidor temporal con la config dada."""
    with tempfile.TemporaryDirectory() as tmp:
        if config is not None:
            Path(tmp, "sdaf.config.yaml").write_text(config, encoding="utf-8", newline="\n")
        proc = run(PRE, ["--cwd", tmp, "--changed", *changed])
    problems = []
    if proc.returncode != code:
        problems.append(f"exit {proc.returncode} (se esperaba {code})")
    problems += [f"falta «{n}»" for n in needles if n not in proc.stdout]
    problems += [f"sobra «{a}»" for a in absent if a in proc.stdout + proc.stderr]
    if "Traceback" in proc.stdout or "Traceback" in proc.stderr:
        problems.append("traceback")
    if problems:
        print(f"FAIL {label}: " + "; ".join(problems))
        print(proc.stdout + proc.stderr)
        return False
    print(f"OK {label}")
    return True


def test_units() -> bool:
    """Presencia de worklog con rutas de código de stack.units y con configs ilegibles."""
    ok = True
    ok &= check_presence("presencia con units: primera unidad sin worklog", UNITS_CONFIG,
                         ["apps/api/x.py"], 1, ("FAIL", "apps/api/x.py"))
    ok &= check_presence("presencia con units: primera unidad con worklog", UNITS_CONFIG,
                         ["apps/api/x.py", WORKLOG_FILE], 0, ("OK worklog presente",))
    ok &= check_presence("presencia con units: segunda unidad sin worklog", UNITS_CONFIG,
                         ["libs/core/y.py"], 1, ("FAIL", "libs/core/y.py"))
    ok &= check_presence("presencia con units: tests de una unidad sin worklog", UNITS_CONFIG,
                         ["tests/api/t.py"], 1, ("FAIL", "tests/api/t.py"))
    ok &= check_presence("presencia con units: ruta no declarada (src/) no es producto", UNITS_CONFIG,
                         ["src/Foo.cs"], 0, ("OK sin código de producto",))
    ok &= check_presence("presencia con units: prefijo por texto no cuenta (apps/api2)", UNITS_CONFIG,
                         ["apps/api2/x.py"], 0, ("OK sin código de producto",))
    ok &= check_presence("presencia con units: solo markdown", UNITS_CONFIG,
                         ["handbook/00-preface.md"], 0, ("OK sin código de producto",))
    ok &= check_presence("presencia con atajo propio: sin worklog", "stack:\n  src_path: apps/web\n",
                         ["apps/web/a.ts"], 1, ("FAIL", "apps/web/a.ts"))
    ok &= check_presence("presencia sin config: src/ sigue siendo producto", None,
                         ["src/Foo.cs"], 1, ("FAIL", "src/Foo.cs"))
    unreadable = ("FAIL sdaf.config.yaml: no se pueden leer las rutas de código (",)
    ok &= check_presence("presencia con YAML roto: FAIL limpio", "stack: [sin cerrar\n",
                         ["apps/api/x.py"], 1, unreadable)
    ok &= check_presence("presencia con stack que es lista: FAIL limpio", "stack:\n  - src_path\n",
                         ["apps/api/x.py"], 1, unreadable)
    ok &= check_presence("presencia con units vacía: FAIL limpio", "stack:\n  units: []\n",
                         ["apps/api/x.py"], 1, unreadable)
    ok &= check_presence("presencia con config ilegible aunque el diff no toque código", "stack:\n  - a\n",
                         ["docs/nota.md"], 1, unreadable)
    return ok


def main() -> int:
    new = run(VW, ["--plantilla", str(ROOT / "templates" / "worklog.md")])
    if new.returncode != 0:
        print("FAIL plantilla frontmatter debería validar")
        print(new.stdout)
        return 1
    print("OK plantilla frontmatter")

    valid = run(VW, [str(ROOT / "scripts" / "testdata" / "worklog-valid.md")])
    if valid.returncode != 0:
        print("FAIL worklog nuevo con valores reales debería validar")
        print(valid.stdout)
        return 1
    print("OK worklog nuevo con valores reales")

    bad = run(VW, [str(ROOT / "scripts" / "testdata" / "worklog-bad-sha.md")])
    expected = ("sha", "fecha", "tiempo", "coste", "fin")
    if bad.returncode == 0 or any(k not in bad.stdout for k in expected):
        print("FAIL sha corto, fecha libre, N/D sin motivo y fin < inicio deberían salir 1")
        print(bad.stdout)
        return 1
    print("OK sha, fecha, tiempo, coste y orden inicio/fin con formato")

    incoherent = run(VW, [str(ROOT / "scripts" / "testdata" / "worklog-incoherente.md")])
    if incoherent.returncode == 0 or "fecha" not in incoherent.stdout or "tiempo" not in incoherent.stdout:
        print("FAIL fecha ≠ día de inicio y tiempo > fin − inicio deberían salir 1")
        print(incoherent.stdout)
        return 1
    print("OK coherencia fecha/inicio y tiempo ≤ fin − inicio")

    legacy = run(VW, [str(ROOT / "scripts" / "testdata" / "worklog-legacy.md")])
    if legacy.returncode != 0:
        print("FAIL tabla vigente debería validar")
        print(legacy.stdout)
        return 1
    print("OK tabla vigente")

    incomplete = run(VW, [str(ROOT / "scripts" / "testdata" / "worklog-incomplete.md")])
    if incomplete.returncode == 0:
        print("FAIL frontmatter incompleto debería salir 1")
        print(incomplete.stdout)
        return 1
    print("OK frontmatter incompleto")

    prod = run(PRE, ["--changed", "src/Foo.cs"])
    if prod.returncode == 0:
        print("FAIL código de producto sin worklog debería salir 1")
        print(prod.stdout)
        return 1
    print("OK presencia: producto sin worklog")

    ok = run(PRE, ["--changed", "src/Foo.cs", "worklogs/PBI-001/Iteration-001.md"])
    if ok.returncode != 0:
        print("FAIL producto + worklog debería salir 0")
        print(ok.stdout)
        return 1
    print("OK presencia: producto con worklog")

    md = run(PRE, ["--changed", "handbook/00-preface.md"])
    if md.returncode != 0:
        print("FAIL markdown sin producto debería salir 0")
        print(md.stdout)
        return 1
    print("OK presencia: solo markdown")

    env = {**os.environ, "GITHUB_EVENT_NAME": "pull_request", "GITHUB_EVENT_PATH": "", "GITHUB_BASE_SHA": ""}
    blind = run(PRE, [], env=env)
    if blind.returncode == 0:
        print("FAIL PR sin diff calculable debería salir 1")
        print(blind.stdout)
        return 1
    print("OK presencia: PR sin diff calculable falla")
    return 0 if test_units() else 1


if __name__ == "__main__":
    sys.exit(main())
