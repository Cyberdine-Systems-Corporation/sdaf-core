"""Parseo reutilizable de ADRs: tabla de campos, referencias, nombre, título e índice.

check-adrs.py (con guion en el nombre, no importable) valida con esta API y
otros comprobadores pueden reutilizarla. Un ADR se identifica por su número
normalizado a entero (ADR-001 y ADR-0001 son el mismo); `adr_num` y
`adr_label` son el único punto de paso entre texto e entero.

El ancho admitido del número es `digits = (mínimo, máximo)` de dígitos y por
defecto vale DIGITS = (3, 3). El mínimo fija además el relleno de ADR-NNN.

`index_rows` lee el índice con columnas fijas (ADR | Estado | Título | [Sustituido
por]); `index_table` lo lee por el nombre de las cabeceras, con las fijas como
posición por defecto.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

DIGITS = (3, 3)
ADR_DIGITS = (3, 4)  # ancho admitido de ADR-N al leer ficheros: 3 en el core, 3 o 4 en consumidores
ADR_FOLDER = "architecture/decisions"
# Equivalencias de estado de los ADRs heredados (minúsculas → estado canónico).
ESTADOS_HEREDADOS = {
    "proposed": "Propuesto", "propuesto": "Propuesto", "propuesta": "Propuesto",
    "accepted": "Aceptado", "aceptado": "Aceptado", "aceptada": "Aceptado",
    "rejected": "Rechazado", "rechazado": "Rechazado", "rechazada": "Rechazado",
    "superseded": "Sustituido", "sustituido": "Sustituido", "sustituida": "Sustituido",
    "deprecated": "Deprecado", "deprecado": "Deprecado", "deprecada": "Deprecado",
}
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
def title_re(digits: tuple[int, int] = DIGITS, flex_sep: bool = False) -> re.Pattern[str]:
    """Título «# ADR-NNN — …»; el grupo 1 son los dígitos.

    Con `flex_sep` el separador puede ser también «-» o «:» (ADR-NNN: …).
    """
    sep = r"(?:[ \t]+[—-][ \t]+|[ \t]*:[ \t]+)" if flex_sep else " — "
    return re.compile(r"^# ADR-([0-9]%s)%s.+$" % (_width(digits), sep), re.MULTILINE)


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


@dataclass
class IndexTable:
    """Índice leído por cabeceras: filas por número y posición de cada columna."""

    rows: dict[int, tuple[str, list[str]]] = field(default_factory=dict)  # número → (enlace sin «./», celdas)
    header: list[str] | None = None  # celdas de la cabecera reconocida; None si se usan las posiciones por defecto
    cols: dict[str, int] = field(default_factory=dict)  # «estado» / «sustituido por» → posición (desde 0)

    def cell(self, num: int, column: str) -> str | None:
        """Valor de la columna en la fila de `num`; None si la columna no existe o la fila es más corta."""
        pos = self.cols.get(column)
        cells = self.rows[num][1]
        return cells[pos] if pos is not None and pos < len(cells) else None

    def column_name(self, column: str) -> str:
        """Nombre y posición de la columna para los mensajes: «Estado» (4.ª)."""
        pos = self.cols[column]
        name = self.header[pos] if self.header else column.capitalize()
        return f"«{name}» ({pos + 1}.ª)"


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def index_table(text: str, digits: tuple[int, int] = DIGITS) -> IndexTable:
    """Lee el índice. Las columnas «Estado» y «Sustituido por» se localizan por la
    primera fila de cabecera que las nombre (sin distinguir mayúsculas); sin
    cabecera reconocible valen la 2.ª y la 4.ª. La primera celda es [ADR-N](href)
    y un «./» inicial del enlace se descarta."""
    link = re.compile(r"\[ADR-([0-9]%s)\]\(([^)]+)\)" % _width(digits))
    table = IndexTable()
    lines = [_cells(line) for line in text.splitlines() if line.lstrip().startswith("|")]
    for cells in lines:
        names = {c.strip("* ").casefold(): i for i, c in enumerate(cells)}
        found = {k: names[k] for k in ("estado", "sustituido por") if k in names}
        if found:
            table.header, table.cols = cells, found
            break
    else:
        table.cols = {"estado": 1, "sustituido por": 3}
    for cells in lines:
        m = link.match(cells[0])
        if m:
            table.rows[adr_num(m.group(1))] = (m.group(2).removeprefix("./"), cells)
    return table


def _read(path: Path) -> str | None:
    """Texto UTF-8 del fichero (BOM tolerado); None si no existe o no decodifica."""
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError):
        return None


def _adr_files(root: Path) -> list[tuple[int, Path]]:
    """(número, ruta) de los `ADR-N-slug.md` de `<root>/architecture/decisions`, de 3 o 4 dígitos, por nombre.

    Si dos ficheros comparten número (ADR-001 y ADR-0001) gana el primero por orden de nombre.
    """
    folder = root / ADR_FOLDER
    out: dict[int, Path] = {}
    if not folder.is_dir():
        return []
    for path in sorted(folder.glob("ADR-*.md")):
        match = file_re(ADR_DIGITS).match(path.name)
        if match:
            out.setdefault(adr_num(match.group(1)), path)
    return list(out.items())


def adr_index(root: Path) -> dict[int, tuple[str, str | None]]:
    """Número de ADR → (nombre del fichero, Estado tal como figura o None si falta o el fichero es ilegible)."""
    out: dict[int, tuple[str, str | None]] = {}
    for num, path in _adr_files(root):
        text = _read(path)
        out[num] = (path.name, fields(text).get("Estado") if text is not None else None)
    return out


class AdrVigencia(NamedTuple):
    """Vigencia de un ADR leída de su fichero (ADR-006 §4)."""

    fichero: str  # nombre del fichero
    estado: str | None  # Estado canónico (vía ESTADOS_HEREDADOS); None si falta, no se reconoce o el fichero es ilegible
    sustituido_por: list[int]  # ADRs de «Sustituido por»; vacía si no hay fila o vale «—», «-», «N/A»…
    legible: bool  # False si el fichero no existe o no es UTF-8
    vigente: bool  # estado canónico Aceptado y sin «Sustituido por»


def adr_vigencia(root: Path) -> dict[int, AdrVigencia]:
    """Número de ADR → su vigencia, leída de los ficheros ADR (no del índice README)."""
    out: dict[int, AdrVigencia] = {}
    for num, path in _adr_files(root):
        text = _read(path)
        if text is None:
            out[num] = AdrVigencia(path.name, None, [], False, False)
            continue
        data = fields(text)
        estado = ESTADOS_HEREDADOS.get(data.get("Estado", "").strip().casefold())
        sustituido_por = refs(data.get("Sustituido por", ""), ADR_DIGITS)
        out[num] = AdrVigencia(path.name, estado, sustituido_por, True, estado == "Aceptado" and not sustituido_por)
    return out
