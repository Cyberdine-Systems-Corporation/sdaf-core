#!/usr/bin/env python3
"""Comprueba worklog schema (nuevo y tabla vigente) y presencia de worklog."""
from __future__ import annotations

import os
import subprocess
import sys
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
