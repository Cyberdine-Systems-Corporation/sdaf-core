#!/usr/bin/env python3
"""Valida worklogs: frontmatter contra worklog.schema.json, o tabla vigente H08 §4.

--plantilla: valida la forma de templates/worklog.md, cuyos valores son
marcadores (YYYY-MM-DD…); ignora los errores de `pattern` y `enum` y la
coherencia de fechas.

Coherencia (formato nuevo): `fecha` es el día de `inicio`, `fin` no es
anterior a `inicio` y `tiempo` no supera `fin − inicio`.
"""
from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "worklog.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)

LEGACY_FIELDS = [
    "Fecha",
    "Agente",
    "Modelo",
    "Versión prompt",
    "Contexto",
    "Especificaciones utilizadas",
    "Archivos leídos",
    "Archivos modificados",
    "Resultado",
    "Tiempo",
    "Coste",
    "Observaciones",
    "Pruebas ejecutadas",
    "Estado",
    "Siguiente agente",
]


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    if not text.startswith("---"):
        return None, text
    rest = text[3:]
    end = rest.find("\n---")
    if end < 0:
        return None, text
    raw = rest[:end]
    body = rest[end + 4 :]
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError("frontmatter no es un objeto")
    # YAML lee `fecha: 2026-09-24` como date; el schema valida texto ISO.
    data = {
        k: v.isoformat() if isinstance(v, (datetime.date, datetime.datetime)) else v
        for k, v in data.items()
    }
    return data, body


DURATION_RE = re.compile(
    r"^P(?:(?P<d>[0-9]+)D)?(?:T(?:(?P<h>[0-9]+)H)?(?:(?P<m>[0-9]+)M)?(?:(?P<s>[0-9]+)S)?)?$"
)


def parse_duration(text: str) -> datetime.timedelta | None:
    match = DURATION_RE.match(text)
    if not match or text in {"P", "PT"}:
        return None
    parts = {k: int(v) if v else 0 for k, v in match.groupdict().items()}
    return datetime.timedelta(days=parts["d"], hours=parts["h"], minutes=parts["m"], seconds=parts["s"])


def parse_datetime(text) -> datetime.datetime | None:
    try:
        value = datetime.datetime.fromisoformat(str(text).replace("Z", "+00:00"))
    except ValueError:
        return None
    return value if value.tzinfo is not None else None


def coherence(data: dict) -> list[str]:
    errs: list[str] = []
    inicio = parse_datetime(data.get("inicio"))
    fin = parse_datetime(data.get("fin"))
    if inicio is None or fin is None:
        return errs
    if fin < inicio:
        errs.append(f"fin: {data['fin']} es anterior a inicio {data['inicio']}")
    if str(data.get("fecha")) != inicio.date().isoformat():
        errs.append(f"fecha: {data.get('fecha')} no es el día de inicio ({inicio.date().isoformat()})")
    tiempo = data.get("tiempo")
    if isinstance(tiempo, str):
        duration = parse_duration(tiempo)
        if duration is not None and fin >= inicio and duration > fin - inicio:
            errs.append(f"tiempo: {tiempo} supera fin − inicio ({fin - inicio})")
    return errs


PLACEHOLDER_VALIDATORS = {"pattern", "enum"}


def only_placeholder(error) -> bool:
    """El error solo se debe a un marcador de plantilla (pattern/enum), también dentro de anyOf."""
    if error.validator in PLACEHOLDER_VALIDATORS:
        return True
    if error.validator in {"anyOf", "oneOf"} and error.context:
        branches: dict = {}
        for sub in error.context:
            branches.setdefault(sub.relative_schema_path[0], []).append(sub)
        return any(all(only_placeholder(sub) for sub in subs) for subs in branches.values())
    return False


def legacy_ok(text: str) -> list[str]:
    missing: list[str] = []
    for field in LEGACY_FIELDS:
        if not re.search(rf"^\|\s*{re.escape(field)}\s*\|", text, re.MULTILINE):
            missing.append(field)
    return missing


def validate_path(path: Path, plantilla: bool = False) -> list[str]:
    text = path.read_text(encoding="utf-8")
    try:
        data, _body = split_frontmatter(text)
    except ValueError as exc:
        return [str(exc)]
    if data is None:
        missing = legacy_ok(text)
        if missing:
            return [f"formato tabla vigente: faltan campos {', '.join(missing)}"]
        return []
    errs = sorted(VALIDATOR.iter_errors(data), key=lambda e: list(e.path))
    if plantilla:
        errs = [e for e in errs if not only_placeholder(e)]
    out = [
        "/".join(str(p) for p in e.path) + ": " + e.message if e.path else e.message
        for e in errs
    ]
    if not plantilla:
        out.extend(coherence(data))
    return out


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    plantilla = "--plantilla" in args
    args = [a for a in args if a != "--plantilla"]
    if not args:
        print("Uso: validate-worklog.py [--plantilla] <rutas>")
        return 1
    failed = 0
    for raw in args:
        path = Path(raw)
        if not path.is_file():
            print(f"FAIL ruta inexistente: {raw}")
            failed += 1
            continue
        errs = validate_path(path, plantilla)
        if errs:
            failed += 1
            print(f"FAIL {path}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"OK   {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
