#!/usr/bin/env python3
"""Falla si la cabecera de versión no coincide con la máxima del historial.

También comprueba fechas: formato ISO 8601 (día, o día con hora y zona) y que
la fecha de cabecera sea la de la fila más reciente de la versión máxima.

Parser: scripts/sdaf_meta.py (sidecar handbook/_meta o tabla en el cuerpo).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sdaf_meta import DATE_RE, fecha_key, load_dates, load_version_info  # noqa: E402

INCLUDE_GLOBS = [
    "handbook/*.md",
    "agents/*.md",
    "prompts/**/*.md",
    "skills/**/*.md",
    "templates/*.md",
    "AGENTS.md.template",
]

SKIP = {
    "handbook/CHANGELOG.md",
    "agents/README.md",
    "prompts/README.md",
    "templates/worklog.md",
}


def iter_targets() -> list[Path]:
    found: list[Path] = []
    for glob in INCLUDE_GLOBS:
        found.extend(ROOT.glob(glob))
    out: list[Path] = []
    for path in found:
        rel = path.relative_to(ROOT).as_posix()
        if rel in SKIP:
            continue
        if path.name == "CHANGELOG.md":
            continue
        out.append(path)
    return sorted(set(out))


def main() -> int:
    global ROOT
    parser = argparse.ArgumentParser(description="Versión y fechas de cabecera frente al historial.")
    parser.add_argument("--root", default=str(ROOT), help="Raíz del árbol a comprobar (fixtures).")
    ROOT = Path(parser.parse_args().root).resolve()
    failed = 0
    checked = 0
    for path in iter_targets():
        info = load_version_info(path, ROOT)
        rel = path.relative_to(ROOT).as_posix()
        if info.header is None and not info.history:
            continue
        checked += 1
        if info.header is None:
            print(f"FAIL {rel}: historial sin campo Versión de cabecera ({info.source})")
            failed += 1
            continue
        if not info.history:
            print(f"FAIL {rel}: versión {info.header} sin tabla de Historial ({info.source})")
            failed += 1
            continue
        if info.header != info.history_max:
            print(
                f"FAIL {rel}: cabecera {info.header} ≠ máxima del historial "
                f"{info.history_max} ({info.source})"
            )
            failed += 1
        header_fecha, rows, source = load_dates(path, ROOT)
        # Marcadores de plantilla (YYYY-MM-DD…, celda vacía): no son fechas.
        rows = [(v, f) for v, f in rows if f and "YYYY" not in f]
        if header_fecha and "YYYY" in header_fecha:
            header_fecha = None
        bad = [f for _, f in rows if not DATE_RE.match(f)]
        if header_fecha and not DATE_RE.match(header_fecha):
            bad.append(header_fecha)
        if bad:
            print(f"FAIL {rel}: fecha(s) fuera de ISO 8601: {', '.join(bad)} ({source})")
            failed += 1
            continue
        top = [f for v, f in rows if v == info.history_max]
        if header_fecha and top:
            latest = max(top, key=fecha_key)
            if header_fecha != latest:
                print(
                    f"FAIL {rel}: fecha de cabecera {header_fecha} ≠ fila más reciente "
                    f"de {info.history_max} ({latest}) ({source})"
                )
                failed += 1
    if failed:
        print(f"{failed} fichero(s) con metadatos incoherentes (de {checked})")
        return 1
    print(f"OK metadatos de versión ({checked} ficheros)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
