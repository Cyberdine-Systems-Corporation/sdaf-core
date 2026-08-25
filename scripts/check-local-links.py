#!/usr/bin/env python3
"""Comprueba que rutas relativas markdown hacia archivos del repo existan (muestreo README/docs/skills)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
SCAN = [
    ROOT / "README.md",
    ROOT / "docs",
    ROOT / "skills",
    ROOT / "handbook" / "README.md",
    ROOT / "AGENTS.md.template",
]


def iter_md(paths: list[Path]):
    for p in paths:
        if p.is_file():
            yield p
        elif p.is_dir():
            yield from p.rglob("*.md")


def main() -> int:
    missing = []
    for md in iter_md(SCAN):
        text = md.read_text(encoding="utf-8")
        for _label, href in LINK_RE.findall(text):
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = href.split("#", 1)[0]
            if not target:
                continue
            resolved = (md.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                continue
            if not resolved.exists():
                missing.append(f"{md.relative_to(ROOT)} -> {href}")
    if missing:
        print("Rutas rotas:")
        for m in missing:
            print(f"  - {m}")
        return 1
    print("OK enlaces locales (README/docs/skills/handbook README/AGENTS template)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
