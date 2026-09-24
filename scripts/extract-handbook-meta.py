#!/usr/bin/env python3
"""Extrae cabecera, TOC, Relacionado e Historial de capítulos del handbook a _meta/."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
HANDBOOK = ROOT / "handbook"
META = HANDBOOK / "_meta"

SKIP = {"CHANGELOG.md"}


def parse_related(block: str) -> list[dict]:
    rows: list[dict] = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|") or re.match(r"^\|\s*-+", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or cells[0] in {"Destino", "", "|"}:
            continue
        if cells[0].startswith("-") or "Destino" in cells[0] or cells[0] in {"|"}:
            continue
        if any(h in cells[0].lower() for h in ("destino", "por qué", "por que")):
            continue
        if len(cells) >= 3 and cells[0] in {"", "🧭", "🛠️", "📖", "📝", "⛔", "📦", "🖼️"}:
            destino, por_que = cells[1], cells[2]
        elif len(cells) >= 2:
            destino, por_que = cells[0], cells[1]
        else:
            continue
        if destino.lower() in {"destino"}:
            continue
        rows.append({"destino": destino, "por_que": por_que})
    return rows


def parse_historial(block: str) -> list[dict]:
    rows: list[dict] = []
    for line in block.splitlines():
        line = line.strip()
        m = re.match(
            r"^\|\s*([0-9]+(?:\.[0-9]+){1,2})\s*\|\s*([^\|]+)\|\s*(.+?)\s*\|$",
            line,
        )
        if not m:
            continue
        rows.append(
            {
                "version": m.group(1),
                "fecha": m.group(2).strip(),
                "cambio": m.group(3).strip(),
            }
        )
    return rows


def parse_cabecera(block: str) -> dict:
    data: dict[str, str] = {}
    for line in block.splitlines():
        m = re.match(r"^\|\s*\*{0,2}([^|*]+)\*{0,2}\s*\|\s*(.*?)\s*\|$", line.strip())
        if not m:
            continue
        key = m.group(1).strip()
        val = m.group(2).strip()
        if key.lower() in {"campo", "---"} or set(key) <= {"-"}:
            continue
        data[key] = val
    return data


def split_body(text: str) -> dict:
    lines = text.splitlines()
    title = lines[0] if lines else ""
    i = 1
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    cab_lines: list[str] = []
    if i < len(lines) and lines[i].startswith("|"):
        while i < len(lines) and (lines[i].startswith("|") or lines[i].strip() == ""):
            if lines[i].strip():
                cab_lines.append(lines[i])
            i += 1
    while i < len(lines) and lines[i].strip() in {"", "---"}:
        i += 1
    toc = ""
    if i < len(lines) and re.match(r"^\*\*En esta p.gina:\*\*", lines[i]):
        toc = lines[i]
        i += 1
        while i < len(lines) and lines[i].strip() == "":
            i += 1
    rest = "\n".join(lines[i:])
    rel_m = re.search(r"^## Relacionado\s*$", rest, re.MULTILINE)
    hist_m = re.search(r"^## (?:\d+\.\s+)?Historial\s*$", rest, re.MULTILINE)
    cuts = []
    if rel_m:
        cuts.append(rel_m.start())
    if hist_m:
        cuts.append(hist_m.start())
    body = rest[: min(cuts)].rstrip() if cuts else rest.rstrip()
    relacionado = ""
    historial = ""
    if rel_m and hist_m:
        if rel_m.start() < hist_m.start():
            relacionado = rest[rel_m.end() : hist_m.start()]
            historial = rest[hist_m.end() :]
        else:
            historial = rest[hist_m.end() : rel_m.start()]
            relacionado = rest[rel_m.end() :]
    elif rel_m:
        relacionado = rest[rel_m.end() :]
    elif hist_m:
        historial = rest[hist_m.end() :]
    return {
        "title": title,
        "cabecera": parse_cabecera("\n".join(cab_lines)),
        "toc": toc,
        "body": body,
        "relacionado": parse_related(relacionado),
        "historial": parse_historial(historial),
    }


def cab_get(cab: dict, *names: str) -> str:
    lower = {k.lower().strip("*"): v for k, v in cab.items()}
    for name in names:
        if name.lower() in lower:
            return lower[name.lower()]
    return ""


def extract_file(path: Path) -> None:
    parsed = split_body(path.read_text(encoding="utf-8"))
    cab = parsed["cabecera"]
    meta = {
        "archivo": path.name,
        "titulo": parsed["title"].lstrip("# ").strip(),
        "version": cab_get(cab, "Versión", "Version"),
        "estado": cab_get(cab, "Estado"),
        "fecha": cab_get(cab, "Fecha", "Última actualización"),
        "parte": cab_get(cab, "Parte"),
        "norma_superior": cab_get(cab, "Norma superior", "Norma"),
        "deriva_hacia": cab_get(cab, "Deriva hacia"),
        "toc": parsed["toc"],
        "relacionado": parsed["relacionado"],
        "historial": parsed["historial"],
        "cabecera": cab,
    }
    META.mkdir(parents=True, exist_ok=True)
    side = META / f"{path.stem}.yaml"
    side.write_text(
        yaml.safe_dump(meta, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    pointer = (
        f"{parsed['title']}\n\n"
        f"> Andamiaje (cabecera, TOC, Relacionado, Historial): "
        f"`_meta/{path.stem}.yaml`.\n\n"
        f"{parsed['body']}\n"
    )
    path.write_text(pointer, encoding="utf-8")


def write_index(files: list[Path]) -> None:
    items = []
    for path in files:
        side = META / f"{path.stem}.yaml"
        data = yaml.safe_load(side.read_text(encoding="utf-8"))
        items.append(
            {
                "id": path.stem,
                "archivo": path.name,
                "meta": f"_meta/{path.stem}.yaml",
                "version": data.get("version"),
                "estado": data.get("estado"),
                "titulo": data.get("titulo"),
            }
        )
    payload = {
        "linea": "0.4.0",
        "nota": "Andamiaje de capítulos en handbook/_meta. El cuerpo es norma.",
        "capitulos": items,
    }
    (HANDBOOK / "index.yaml").write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def main() -> int:
    files = sorted(
        p
        for p in HANDBOOK.glob("*.md")
        if p.name not in SKIP
    )
    for path in files:
        extract_file(path)
        print(f"OK {path.name}")
    write_index(files)
    print("OK handbook/index.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
