#!/usr/bin/env python3
"""Valida manifiestos de pack (sdaf-pack.yaml) contra el schema y la coherencia.

Sin argumentos: templates/sdaf-pack.yaml. Salida `OK  <ruta>` o una línea
`FAIL <ruta>: <motivo>` por cada problema; sale 0 si todo valida y 1 si hay algún
FAIL. Un YAML inválido, un fichero que no es UTF-8 o una raíz que no es un mapa
son FAIL, nunca un traceback.

Además del schema (sdaf-pack.schema.json) comprueba, en `core` y en cada
`requires[].version`, la coherencia del rango, y que un pack no se requiere a sí
mismo. Un rango son uno o dos comparadores `X.Y.Z` separados por un espacio. Los
comparadores admitidos son `>=` y `>` (límite inferior), `<=` y `<` (límite
superior) y `=` o ninguno (versión exacta). Las versiones se comparan como tuplas
de enteros (0.10.0 es mayor que 0.9.0), nunca como texto. Con dos comparadores
debe haber un límite inferior y uno superior, en cualquier orden; el rango no
puede quedar vacío: el inferior debe ser menor que el superior, salvo
`>=X.Y.Z <=X.Y.Z`, que fija una única versión. La igualdad no se combina con
otro comparador.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "sdaf-pack.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)
TEMPLATE = ROOT / "templates" / "sdaf-pack.yaml"

COMPARATOR_RE = re.compile(r"(>=|<=|>|<|=)?([0-9]+)\.([0-9]+)\.([0-9]+)")
LOWER = {">=", ">"}
UPPER = {"<=", "<"}
TYPES = {
    "object": "un mapa",
    "array": "una lista",
    "string": "un texto",
    "integer": "un número",
    "number": "un número",
    "boolean": "un booleano",
    "null": "un valor nulo",
}


def type_name(value) -> str:
    if value is None:
        return TYPES["null"]
    if isinstance(value, bool):
        return TYPES["boolean"]
    if isinstance(value, (int, float)):
        return TYPES["number"]
    if isinstance(value, str):
        return TYPES["string"]
    if isinstance(value, dict):
        return TYPES["object"]
    return TYPES["array"]


def schema_reason(error) -> str:
    """Traduce un error de jsonschema a un motivo en español."""
    kind = error.validator
    if kind == "required":
        missing = [k for k in error.validator_value if k not in error.instance]
        return "falta la propiedad obligatoria " + ", ".join(f"'{k}'" for k in missing)
    if kind == "additionalProperties":
        known = error.schema.get("properties", {})
        extra = [k for k in error.instance if k not in known]
        return "propiedad no permitida: " + ", ".join(f"'{k}'" for k in extra)
    if kind == "pattern":
        return f"el valor {error.instance!r} no cumple el patrón {error.validator_value}"
    if kind == "minProperties":
        return f"debe declarar al menos {error.validator_value} propiedad(es)"
    if kind == "uniqueItems":
        return "la lista no admite elementos repetidos"
    if kind == "type":
        expected = error.validator_value
        names = expected if isinstance(expected, list) else [expected]
        wanted = " o ".join(TYPES.get(n, n) for n in names)
        return f"se esperaba {wanted} y se encontró {type_name(error.instance)}"
    return error.message


def parse_range(text: str) -> list[tuple[str, tuple[int, int, int]]] | None:
    """Devuelve [(comparador, (X, Y, Z))] o None si la sintaxis no es válida."""
    parts = text.split(" ")
    if len(parts) > 2:
        return None
    parsed = []
    for part in parts:
        match = COMPARATOR_RE.fullmatch(part)
        if not match:
            return None
        parsed.append((match.group(1) or "=", tuple(int(g) for g in match.group(2, 3, 4))))
    return parsed


def range_issue(text: str) -> str | None:
    """Motivo si el rango es incoherente; None si es coherente o de sintaxis inválida."""
    parsed = parse_range(text)
    if parsed is None or len(parsed) < 2:
        return None
    (op_a, _), (op_b, _) = parsed
    if "=" in (op_a, op_b):
        return f"el rango {text!r} combina una igualdad con otro comparador"
    if (op_a in LOWER) == (op_b in LOWER):
        return (
            f"el rango {text!r} combina dos límites del mismo sentido; "
            "use un límite inferior (>=, >) y uno superior (<, <=)"
        )
    (low_op, low), (up_op, up) = sorted(
        parsed, key=lambda c: 0 if c[0] in LOWER else 1
    )
    if low < up or (low == up and (low_op, up_op) == (">=", "<=")):
        return None
    dotted = lambda v: ".".join(str(n) for n in v)  # noqa: E731
    return (
        f"el rango {text!r} está vacío: el límite inferior ({dotted(low)}) "
        f"debe ser menor que el superior ({dotted(up)})"
    )


def edge_issue(where: str, value) -> str | None:
    """Motivo si un texto lleva espacios o saltos de línea en los extremos.

    Los patrones del schema usan `$`, que en Python admite un salto de línea
    final (p. ej. el de un bloque literal `|` de YAML); aquí se rechaza.
    """
    if isinstance(value, str) and value != value.strip():
        return f"{where}: el valor lleva espacios o saltos de línea al inicio o al final ({value!r})"
    return None


def semantic_issues(data: dict) -> list[str]:
    issues: list[str] = []
    for key in ("id", "version", "core"):
        if reason := edge_issue(key, data.get(key)):
            issues.append(reason)
    requires_items = data.get("requires")
    if isinstance(requires_items, list):
        for i, item in enumerate(requires_items):
            if isinstance(item, dict):
                for key in ("id", "version"):
                    if reason := edge_issue(f"requires/{i}/{key}", item.get(key)):
                        issues.append(reason)
    core = data.get("core")
    if isinstance(core, str) and (reason := range_issue(core)):
        issues.append(f"core: {reason}")
    requires = data.get("requires")
    if isinstance(requires, list):
        own_id = data.get("id")
        for i, item in enumerate(requires):
            if not isinstance(item, dict):
                continue
            version = item.get("version")
            if isinstance(version, str) and (reason := range_issue(version)):
                issues.append(f"requires/{i}/version: {reason}")
            if isinstance(own_id, str) and item.get("id") == own_id:
                issues.append(f"requires/{i}/id: un pack no puede requerirse a sí mismo ({own_id!r})")
    return issues


def load(path: Path) -> tuple[object, str | None]:
    """Lee el YAML; devuelve (datos, motivo de error o None)."""
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as exc:
        return None, f"el fichero no es UTF-8 válido (byte inválido en la posición {exc.start})"
    except OSError as exc:
        return None, f"no se puede leer el fichero: {exc.strerror or exc}"
    try:
        return yaml.safe_load(text), None
    except yaml.YAMLError as exc:
        return None, "YAML inválido: " + " ".join(str(exc).split())


def validate_file(path: Path) -> list[str]:
    """Devuelve los motivos de fallo; vacío si el manifiesto es válido."""
    data, error = load(path)
    if error:
        return [error]
    if not isinstance(data, dict):
        return [f"la raíz no es un mapa (se encontró {type_name(data)})"]
    reasons = []
    for err in sorted(VALIDATOR.iter_errors(data), key=lambda e: [str(p) for p in e.absolute_path]):
        where = "/".join(str(p) for p in err.absolute_path) or "(raíz)"
        reasons.append(f"{where}: {schema_reason(err)}")
    return reasons + semantic_issues(data)


def label_of(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Valida manifiestos de pack (sdaf-pack.yaml) contra schema y coherencia."
    )
    parser.add_argument(
        "paths", nargs="*", help="Rutas YAML. Sin argumentos: templates/sdaf-pack.yaml"
    )
    args = parser.parse_args(argv)

    failed = False
    for raw in args.paths or [str(TEMPLATE)]:
        path = Path(raw)
        if not path.is_file():
            print(f"FAIL {raw}: ruta inexistente o no es un fichero")
            failed = True
            continue
        reasons = validate_file(path)
        label = label_of(path)
        if reasons:
            failed = True
            for reason in reasons:
                print(f"FAIL {label}: {reason}")
        else:
            print(f"OK  {label}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
