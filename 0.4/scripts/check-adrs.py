#!/usr/bin/env python3
"""Comprueba los ADRs del core en architecture/decisions/.

- Numeración: ADR-001, ADR-002… sin huecos ni repetidos; el título coincide
  con el número del fichero (ADR-001, H13 §8).
- Estado: Propuesto, Aceptado o Deprecado (templates/adr.md).
- Fecha: ISO 8601 con hora y zona (H13 §9); todos los ADRs del core son de la
  línea 0.4.0 o posteriores.
- Aceptado exige fila Aceptación que empiece por fecha con hora y zona, no
  anterior a Fecha. Propuesto no lleva Aceptación: un agente no la escribe
  (H00 §3.3).
- El README de la carpeta lista cada ADR con su mismo estado.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sdaf_meta import fecha_key, has_time  # noqa: E402

ESTADOS = {"Propuesto", "Aceptado", "Deprecado"}
FILE_RE = re.compile(r"^ADR-([0-9]{3})-[a-z0-9-]+\.md$")
TITLE_RE = re.compile(r"^# ADR-([0-9]{3}) — .+$", re.MULTILINE)
FIELD_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$", re.MULTILINE)
LEADING_DATE_RE = re.compile(r"^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]+(?:Z|[+-][0-9]{2}:[0-9]{2}))")
INDEX_ROW_RE = re.compile(r"^\|\s*\[ADR-([0-9]{3})\]\(([^)]+)\)\s*\|\s*([^|]+?)\s*\|", re.MULTILINE)


def fields(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, value in FIELD_RE.findall(text):
        key = key.strip("* ")
        if key in {"Campo", "ADR"} or set(key) <= {"-"}:
            continue
        out.setdefault(key, value.strip())
    return out


def check_adr(path: Path) -> tuple[str | None, list[str]]:
    """Devuelve (estado, errores) de un ADR."""
    errs: list[str] = []
    num = FILE_RE.match(path.name).group(1)
    text = path.read_text(encoding="utf-8")
    title = TITLE_RE.search(text)
    if not title:
        errs.append("falta el título «# ADR-NNN — …»")
    elif title.group(1) != num:
        errs.append(f"el título dice ADR-{title.group(1)} y el fichero ADR-{num}")
    data = fields(text)
    estado = data.get("Estado")
    if estado not in ESTADOS:
        errs.append(f"Estado «{estado}» no es uno de {sorted(ESTADOS)}")
    fecha = data.get("Fecha", "")
    if not has_time(fecha) or fecha_key(fecha) is None:
        errs.append(f"Fecha «{fecha}» no es ISO 8601 con hora y zona (H13 §9)")
    aceptacion = data.get("Aceptación")
    if estado == "Aceptado":
        match = LEADING_DATE_RE.match(aceptacion or "")
        if not match or fecha_key(match.group(1)) is None:
            errs.append("Aceptado sin fila Aceptación que empiece por fecha con hora y zona")
        elif fecha_key(fecha) is not None and fecha_key(match.group(1)) < fecha_key(fecha):
            errs.append(f"Aceptación {match.group(1)} anterior a Fecha {fecha}")
    elif estado == "Propuesto" and aceptacion:
        errs.append("Propuesto con fila Aceptación: aceptar es un acto humano que cambia el Estado")
    return estado, errs


def main() -> int:
    parser = argparse.ArgumentParser(description="Comprueba los ADRs del core.")
    parser.add_argument("--root", default=str(ROOT), help="Raíz del árbol a comprobar (fixtures).")
    root = Path(parser.parse_args().root).resolve()
    folder = root / "architecture" / "decisions"
    if not folder.is_dir():
        print("OK sin architecture/decisions/")
        return 0

    failed = 0
    estados: dict[str, str | None] = {}
    files: dict[str, str] = {}
    for path in sorted(folder.glob("ADR-*.md")):
        match = FILE_RE.match(path.name)
        if not match:
            print(f"FAIL {path.name}: nombre fuera de ADR-NNN-slug.md")
            failed += 1
            continue
        num = match.group(1)
        if num in files:
            print(f"FAIL ADR-{num} repetido: {files[num]} y {path.name}")
            failed += 1
            continue
        files[num] = path.name
        estado, errs = check_adr(path)
        estados[num] = estado
        for err in errs:
            print(f"FAIL {path.name}: {err}")
            failed += 1

    expected = [f"{i:03d}" for i in range(1, len(files) + 1)]
    if sorted(files) != expected:
        print(f"FAIL numeración con huecos: {sorted(files)} (se espera {expected})")
        failed += 1

    readme = folder / "README.md"
    listed: dict[str, tuple[str, str]] = {}
    if readme.is_file():
        for num, href, estado in INDEX_ROW_RE.findall(readme.read_text(encoding="utf-8")):
            listed[num] = (href, estado)
    for num, name in files.items():
        if num not in listed:
            print(f"FAIL README.md no lista ADR-{num}")
            failed += 1
            continue
        href, estado = listed[num]
        if href != name:
            print(f"FAIL README.md enlaza ADR-{num} a {href}, no a {name}")
            failed += 1
        if estado != estados.get(num):
            print(f"FAIL README.md dice {estado} para ADR-{num}; el ADR dice {estados.get(num)}")
            failed += 1
    for num in listed.keys() - files.keys():
        print(f"FAIL README.md lista ADR-{num}, que no existe")
        failed += 1

    if failed:
        print(f"{failed} problema(s) en los ADRs")
        return 1
    print(f"OK ADRs ({len(files)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
