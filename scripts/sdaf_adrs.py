"""Parseo reutilizable de ADRs: tabla de campos, referencias, nombre, título e índice.

check-adrs.py (con guion en el nombre, no importable) valida con esta API y
otros comprobadores pueden reutilizarla. Un ADR se identifica por su número
normalizado a entero (ADR-001 y ADR-0001 son el mismo); `adr_num` y
`adr_label` son el único punto de paso entre texto e entero.

El ancho admitido del número es `digits = (mínimo, máximo)` de dígitos y por
defecto vale DIGITS = (3, 3). El mínimo fija además el relleno de ADR-NNN.
"""
from __future__ import annotations

import re
from functools import lru_cache

DIGITS = (3, 3)
FIELD_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$", re.MULTILINE)


def _width(digits: tuple[int, int]) -> str:
    return "{%d,%d}" % digits


def adr_num(text: str) -> int:
    """Número de ADR normalizado a entero desde sus dígitos («001» y «0001» → 1)."""
    return int(text)


def adr_label(num: int, digits: tuple[int, int] = DIGITS) -> str:
    """Forma textual «ADR-NNN» de un número, con el relleno mínimo de `digits`."""
    return f"ADR-{num:0{digits[0]}d}"


@lru_cache(maxsize=None)
def file_re(digits: tuple[int, int] = DIGITS) -> re.Pattern[str]:
    """Nombre de fichero «ADR-NNN-slug.md»; el grupo 1 son los dígitos."""
    return re.compile(r"^ADR-([0-9]%s)-[a-z0-9-]+\.md$" % _width(digits))


@lru_cache(maxsize=None)
def title_re(digits: tuple[int, int] = DIGITS) -> re.Pattern[str]:
    """Título «# ADR-NNN — …»; el grupo 1 son los dígitos."""
    return re.compile(r"^# ADR-([0-9]%s) — .+$" % _width(digits), re.MULTILINE)


@lru_cache(maxsize=None)
def ref_re(digits: tuple[int, int] = DIGITS) -> re.Pattern[str]:
    """Referencia «ADR-N» dentro de un valor; el grupo 1 son los dígitos."""
    return re.compile(r"ADR-([0-9]%s)" % _width(digits))


@lru_cache(maxsize=None)
def index_row_re(digits: tuple[int, int] = DIGITS) -> re.Pattern[str]:
    """Fila del índice. Columnas: ADR | Estado | Título | [Sustituido por].

    La 4.ª es opcional (consumidores con el índice anterior); el grupo 4 es
    None si falta. El grupo 1 son los dígitos, el 2 el enlace y el 3 el estado.
    """
    return re.compile(
        r"^\|\s*\[ADR-([0-9]%s)\]\(([^)]+)\)\s*\|\s*([^|]+?)\s*\|"
        r"(?:[ \t]*[^|\n]*?[ \t]*\|[ \t]*([^|\n]*?)[ \t]*\|)?" % _width(digits),
        re.MULTILINE,
    )


def fields(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, value in FIELD_RE.findall(text):
        key = key.strip("* ")
        if key in {"Campo", "ADR"} or set(key) <= {"-"}:
            continue
        out.setdefault(key, value.strip())
    return out


def refs(value: str, digits: tuple[int, int] = DIGITS) -> list[int]:
    """Números de ADR citados en un valor, normalizados, sin repetidos y en orden."""
    return list(dict.fromkeys(adr_num(n) for n in ref_re(digits).findall(value)))


def index_rows(text: str, digits: tuple[int, int] = DIGITS) -> dict[int, tuple[str, str, str | None]]:
    """Filas del índice por número: (enlace, estado, Sustituido por o None)."""
    listed: dict[int, tuple[str, str, str | None]] = {}
    for m in index_row_re(digits).finditer(text):
        listed[adr_num(m.group(1))] = (m.group(2), m.group(3), m.group(4))
    return listed
