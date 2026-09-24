#!/usr/bin/env python3
"""Comprueba que el cuerpo de los capítulos no reintroduce andamiaje extraído."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDBOOK = ROOT / "handbook"
META = HANDBOOK / "_meta"
SKIP = {"CHANGELOG.md"}

FORBIDDEN = [
    re.compile(r"^\|\s*\*\*Versión\*\*\s*\|", re.MULTILINE),
    re.compile(r"^\*\*En esta p.gina:\*\*", re.MULTILINE),
    re.compile(r"^## Relacionado\s*$", re.MULTILINE),
    re.compile(r"^## (?:\d+\.\s+)?Historial\s*$", re.MULTILINE),
]


def main() -> int:
    failed = 0
    bodies = 0
    meta_lines = 0
    body_lines = 0
    files = sorted(p for p in HANDBOOK.glob("*.md") if p.name not in SKIP)
    for path in files:
        side = META / f"{path.stem}.yaml"
        if not side.is_file():
            print(f"FAIL falta sidecar {side.relative_to(ROOT).as_posix()}")
            failed += 1
            continue
        text = path.read_text(encoding="utf-8")
        bodies += 1
        body_lines += len(text.splitlines())
        meta_lines += len(side.read_text(encoding="utf-8").splitlines())
        for pat in FORBIDDEN:
            if pat.search(text):
                print(f"FAIL {path.name}: el cuerpo aún contiene andamiaje ({pat.pattern})")
                failed += 1
                break
        if f"_meta/{path.stem}.yaml" not in text:
            print(f"FAIL {path.name}: falta puntero al sidecar")
            failed += 1
    index = HANDBOOK / "index.yaml"
    if not index.is_file():
        print("FAIL falta handbook/index.yaml")
        failed += 1
    if failed:
        return 1
    print(
        f"OK andamiaje extraído ({bodies} capítulos; "
        f"{body_lines} líneas de cuerpo, {meta_lines} líneas en _meta)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
