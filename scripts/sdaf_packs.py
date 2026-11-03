"""Reglas reutilizables de manifiestos de pack: rangos de versión y bordes de texto.

validate-pack.py (con guion en el nombre, no importable) valida los manifiestos
con esta API, y validate-config.py la reutilizará para validar los manifiestos
que reciba junto con la configuración.

Un rango son uno o dos comparadores `X.Y.Z` separados por un espacio. Los
comparadores admitidos son `>=` y `>` (límite inferior), `<=` y `<` (límite
superior) y `=` o ninguno (versión exacta). `parse_range` lo descompone en
tuplas de enteros, `range_issue` detecta un rango incoherente y `edge_issue`
rechaza un texto con espacios o saltos de línea en los extremos.
"""
from __future__ import annotations

import re

COMPARATOR_RE = re.compile(r"(>=|<=|>|<|=)?([0-9]+)\.([0-9]+)\.([0-9]+)")
LOWER = {">=", ">"}
UPPER = {"<=", "<"}


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
