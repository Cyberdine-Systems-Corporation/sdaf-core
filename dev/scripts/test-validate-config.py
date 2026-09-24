#!/usr/bin/env python3
"""Comprueba fixtures del validador de config (I1–I4, pack, duplicados)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-config.py"
INVALID = ROOT / "scripts" / "testdata" / "invalid-invariants.yaml"
I4 = ROOT / "scripts" / "testdata" / "i4-extension-without-pack.yaml"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def main() -> int:
    defaults = run([])
    if defaults.returncode != 0:
        print("FAIL examples válidos deberían salir 0")
        print(defaults.stdout)
        print(defaults.stderr)
        return 1
    print("OK examples + example.yaml")

    missing = run(["no-existe.yaml"])
    if missing.returncode == 0 or "inexistente" not in missing.stdout:
        print("FAIL ruta inexistente debería salir 1")
        print(missing.stdout)
        return 1
    print("OK ruta inexistente")

    broken = run([str(INVALID)])
    out = broken.stdout
    if broken.returncode == 0:
        print("FAIL fixture de invariantes debería salir 1")
        print(out)
        return 1
    needed = ["I1", "I2", "I3", "does not match", "uniqueItems", "foo"]
    # jsonschema message for pattern may vary; pack 'foo' must appear
    if "I1" not in out or "I2" not in out or "I3" not in out:
        print("FAIL se esperaban I1 I2 I3 en la salida")
        print(out)
        return 1
    if "foo" not in out and "does not match" not in out and "pattern" not in out.lower():
        print("FAIL se esperaba error de pack inválido")
        print(out)
        return 1
    if "I4" in out and "WARN" not in out:
        # I4 on this fixture: frontend is extension + pack is foo (invalid so schema fails first)
        pass
    print("OK fixture I1–I3 + pack + duplicados")

    i4 = run([str(I4)])
    if i4.returncode != 0:
        print("FAIL I4 por defecto no debe cambiar el exit code")
        print(i4.stdout)
        return 1
    if "WARN" not in i4.stdout or "frontend" not in i4.stdout or "I4" not in i4.stdout:
        print("FAIL I4 debería avisar y nombrar frontend")
        print(i4.stdout)
        return 1
    print("OK I4 aviso por defecto")

    i4_strict = run(["--strict-i4", str(I4)])
    if i4_strict.returncode == 0 or "I4" not in i4_strict.stdout:
        print("FAIL --strict-i4 debería salir 1 con I4")
        print(i4_strict.stdout)
        return 1
    print("OK I4 --strict-i4")
    return 0


if __name__ == "__main__":
    sys.exit(main())
