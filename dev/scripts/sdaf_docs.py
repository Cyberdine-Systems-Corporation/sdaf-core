"""Lectura reutilizable de documentos del método: cabecera, secciones, tablas, specs, PBIs y línea base.

check-gate0.py (con guion en el nombre, no importable) lee con esta API y
otros comprobadores (p. ej. ARQ-6.2) pueden reutilizarla. API pura: sin main,
sin efectos sobre el proceso; los ficheros ilegibles se devuelven como None
o se ignoran, nunca lanzan.

Un documento tiene un encabezado `# `, una primera tabla `| Campo | Valor |`
con su cabecera (`header_fields`) y secciones `## …` (`section`). Specs y
PBIs se identifican por la fila `ID` de esa cabecera.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

H1_RE = re.compile(r"^# ", re.MULTILINE)
FIELD_HEADER_RE = re.compile(r"^\|\s*Campo\s*\|\s*Valor\s*\|\s*$")
FIELD_ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$")
SEPARATOR_CELL_RE = re.compile(r"^:?-+:?$")
FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)^---[ \t]*$", re.MULTILINE | re.DOTALL)
PLACEHOLDER_RE = re.compile(r"XXX|YYYY|<[^<>\n]+>|nombres exactos de la línea base|SPEC-ACC-000|enlace a la sección de acceptance")
TRAILING_PAREN_RE = re.compile(r"\s*\([^()]*\)\s*$")
# Coma o «;» fuera de paréntesis (no hay «)» antes de la siguiente «(»).
LIST_SEP_RE = re.compile(r"[,;](?![^(]*\))")
UNITS_TITLE_RE = r"Unidades\s*$"
INHERITED_RE = re.compile(r"\bheredada\b", re.IGNORECASE)
TEMPLATE_RESPONSIBILITY = "Qué hace y qué no hace"


def read(path: Path) -> str | None:
    """Texto UTF-8 del fichero (BOM tolerado); None si no existe o no decodifica."""
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError):
        return None


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _is_separator(cells: list[str]) -> bool:
    return all(SEPARATOR_CELL_RE.match(c) for c in cells)


def header_fields(text: str) -> dict[str, str]:
    """Campos de la primera tabla `Campo | Valor` tras el primer `# `; si hay claves repetidas gana la primera."""
    h1 = H1_RE.search(text)
    lines = text[h1.start():].splitlines() if h1 else text.splitlines()
    out: dict[str, str] = {}
    in_table = False
    for line in lines:
        if not in_table:
            in_table = bool(FIELD_HEADER_RE.match(line.strip()))
            continue
        m = FIELD_ROW_RE.match(line.strip())
        if not m:
            break
        key = m.group(1).strip("* ")
        if not key or _is_separator([key]):
            continue
        out.setdefault(key, m.group(2).strip())
    return out


def section(text: str, titulo_re: str) -> str:
    """Cuerpo de la primera sección `## …` cuyo título casa con la regex; "" si no existe."""
    body: list[str] = []
    found = False
    for line in text.splitlines():
        if line.startswith("## "):
            if found:
                break
            found = re.search(titulo_re, line[3:].strip()) is not None
            continue
        if found:
            body.append(line)
    return "\n".join(body)


def _table(block: str) -> tuple[list[str], list[list[str]]]:
    """(cabecera, filas de datos) de la primera tabla markdown del bloque; ([], []) si no hay."""
    rows: list[list[str]] = []
    started = False
    for line in block.splitlines():
        if line.lstrip().startswith("|"):
            started = True
            rows.append(_cells(line))
        elif started:
            break
    if not rows:
        return [], []
    return rows[0], [r for r in rows[1:] if not _is_separator(r)]


def table_rows(block: str) -> list[list[str]]:
    """Filas de datos de la primera tabla del bloque, sin cabecera ni separadora."""
    return _table(block)[1]


def split_list(value: str) -> list[str]:
    """Valores separados por coma o `;`, sin backticks ni paréntesis finales ni vacíos."""
    out = []
    for item in LIST_SEP_RE.split(value.replace("`", "")):
        item = TRAILING_PAREN_RE.sub("", item).strip()
        if item:
            out.append(item)
    return out


def is_placeholder(value: str) -> bool:
    """True si el valor está vacío, es `…` o conserva texto de plantilla (XXX, YYYY, <…>, línea base)."""
    value = value.strip()
    return not value or value == "…" or PLACEHOLDER_RE.search(value) is not None


def frontmatter(text: str) -> dict | None:
    """Mapa YAML del bloque `---` inicial; None si no hay bloque, no es un mapa o el YAML es inválido."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def _index_ids(root: Path, folder: str) -> dict[str, list[Path]]:
    """ID (fila `ID` de la cabecera) → rutas de `<root>/<folder>/**/*.md`; más de una = duplicado."""
    base = root / folder
    found: dict[str, list[Path]] = {}
    if not base.is_dir():
        return found
    for path in sorted(base.rglob("*.md")):
        text = read(path)
        doc_id = header_fields(text).get("ID") if text is not None else None
        if doc_id:
            found.setdefault(doc_id, []).append(path)
    return found


def spec_index(root: Path) -> dict[str, list[Path]]:
    """Specs de `specs/**/*.md` por ID."""
    return _index_ids(root, "specs")


def find_pbis(root: Path) -> dict[str, list[Path]]:
    """PBIs de `backlog/**/*.md` por ID."""
    return _index_ids(root, "backlog")


def baseline(root: Path) -> tuple[str | None, list[str], list[str]] | None:
    """Línea base `architecture/description.md`: (Estado o None, unidades, unidades «heredada»).

    None si el fichero no existe o no decodifica. La tabla de la plantilla sin
    rellenar o una sección sin tabla (`N/A: …`) dan listas vacías.
    """
    text = read(root / "architecture" / "description.md")
    if text is None:
        return None
    header, rows = _table(section(text, UNITS_TITLE_RE))
    names = [h.casefold() for h in header]
    unit_col = names.index("unidad") if "unidad" in names else 0
    resp_col = names.index("responsabilidad") if "responsabilidad" in names else 2
    units: list[str] = []
    inherited: list[str] = []
    for cells in rows:
        if len(cells) <= unit_col or not cells[unit_col]:
            continue
        resp = cells[resp_col] if resp_col < len(cells) else ""
        if resp == TEMPLATE_RESPONSIBILITY:
            continue
        units.append(cells[unit_col])
        if INHERITED_RE.search(resp):
            inherited.append(cells[unit_col])
    return header_fields(text).get("Estado"), units, inherited
