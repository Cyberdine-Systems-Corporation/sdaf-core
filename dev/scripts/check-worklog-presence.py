#!/usr/bin/env python3
"""Falla si el diff toca código de producto y no hay cambio bajo worklogs/.

No parsea campos del worklog. Un diff solo de markdown (typo) sale 0.
Sin diff de PR y sin --changed: sale 0 (nada que comprobar).
En un PR, si no se puede calcular el diff (checkout superficial, base
ausente), sale 1: el chequeo no se da por bueno sin haber mirado.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sdaf_diff import DiffUnavailable, git_changed, is_product, load_product_prefixes  # noqa: E402

WORKLOG_PREFIX = "worklogs/"
MD_SUFFIXES = {".md", ".md.template"}


def is_worklog(path: str) -> bool:
    return path.replace("\\", "/").startswith(WORKLOG_PREFIX)


def is_markdown(path: str) -> bool:
    norm = path.replace("\\", "/").lower()
    return Path(norm).suffix.lower() in {".md"} or norm.endswith(".md.template")


def main() -> int:
    parser = argparse.ArgumentParser(description="Exige worklog si hay código de producto.")
    parser.add_argument("--changed", nargs="*", help="Lista de rutas (modo prueba).")
    parser.add_argument("--base", default=None, help="Ref git para diff local.")
    parser.add_argument("--cwd", default=".", help="Raíz del repo a inspeccionar.")
    args = parser.parse_args()
    cwd = Path(args.cwd).resolve()
    prefixes = load_product_prefixes(cwd)

    if args.changed is not None:
        changed = [p.replace("\\", "/") for p in args.changed]
    else:
        os.chdir(cwd)
        try:
            changed = git_changed(args.base, cwd)
        except DiffUnavailable as exc:
            print(f"FAIL no se pudo calcular el diff del PR: {exc}")
            print("  Revisa que el checkout use fetch-depth: 0.")
            return 1
        if changed is None:
            print("OK sin diff de PR que comprobar")
            return 0

    if not changed:
        print("OK diff vacío")
        return 0

    product = [p for p in changed if is_product(p, prefixes)]
    if not product:
        print("OK sin código de producto en el diff")
        return 0

    if any(is_worklog(p) for p in changed):
        print("OK worklog presente en el diff")
        return 0

    print("FAIL el diff toca código de producto y no modifica worklogs/:")
    for p in product:
        print(f"  - {p}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
