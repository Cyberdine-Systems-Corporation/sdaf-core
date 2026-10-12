"""Parser sustituible de versión/historial de artefactos markdown o sidecar YAML.

El bloque 5 (andamiaje en handbook/_meta) usa la misma API.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

HEADER_VERSION_RE = re.compile(
    r"^\|\s*\*{0,2}Versión\*{0,2}\s*\|\s*([0-9]+(?:\.[0-9]+){1,2})\s*\|",
    re.MULTILINE,
)
HISTORIAL_HEADING_RE = re.compile(
    r"^##\s+(?:\d+\.\s+)?Historial\s*$",
    re.MULTILINE,
)
ROW_RE = re.compile(
    r"^\|\s*([0-9]+(?:\.[0-9]+){1,2})\s*\|\s*([^\|]+)\|\s*(.+?)\s*\|\s*$"
)


def parse_semver(text: str) -> tuple[int, ...]:
    return tuple(int(p) for p in text.split("."))


@dataclass
class VersionInfo:
    path: Path
    header: str | None
    history: list[str]
    source: str  # sidecar | body | missing

    @property
    def history_max(self) -> str | None:
        if not self.history:
            return None
        return max(self.history, key=parse_semver)


def _history_from_markdown(text: str) -> list[str]:
    match = HISTORIAL_HEADING_RE.search(text)
    if not match:
        return []
    block = text[match.end() :]
    next_h = re.search(r"^##\s+", block, re.MULTILINE)
    if next_h:
        block = block[: next_h.start()]
    versions: list[str] = []
    for line in block.splitlines():
        row = ROW_RE.match(line.strip())
        if row:
            versions.append(row.group(1))
    return versions


def _header_from_markdown(text: str) -> str | None:
    match = HEADER_VERSION_RE.search(text)
    return match.group(1) if match else None


def sidecar_path(md_path: Path, root: Path) -> Path | None:
    try:
        rel = md_path.resolve().relative_to((root / "handbook").resolve())
    except ValueError:
        return None
    if rel.as_posix() == "CHANGELOG.md":
        return None
    return root / "handbook" / "_meta" / f"{md_path.stem}.yaml"


def load_from_sidecar(path: Path) -> VersionInfo | None:
    if not path.is_file():
        return None
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    header = data.get("version")
    if not header:
        cab = data.get("cabecera") or {}
        header = cab.get("Versión") or cab.get("Version") or cab.get("versión")
    hist = data.get("historial") or []
    versions: list[str] = []
    for row in hist:
        if isinstance(row, dict) and row.get("version"):
            versions.append(str(row["version"]))
        elif isinstance(row, str):
            versions.append(row)
    return VersionInfo(
        path=path,
        header=str(header) if header is not None else None,
        history=versions,
        source="sidecar",
    )


def load_version_info(md_path: Path, root: Path) -> VersionInfo:
    side = sidecar_path(md_path, root)
    if side is not None:
        info = load_from_sidecar(side)
        if info is not None:
            info.path = md_path
            return info
    text = md_path.read_text(encoding="utf-8")
    header = _header_from_markdown(text)
    history = _history_from_markdown(text)
    source = "body" if header or history else "missing"
    return VersionInfo(path=md_path, header=header, history=history, source=source)


def history_rows_from_markdown(text: str) -> list[tuple[str, str, str]]:
    """Filas (versión, fecha, cambio) de la tabla Historial del cuerpo."""
    match = HISTORIAL_HEADING_RE.search(text)
    if not match:
        return []
    block = text[match.end() :]
    next_h = re.search(r"^##\s+", block, re.MULTILINE)
    if next_h:
        block = block[: next_h.start()]
    rows: list[tuple[str, str, str]] = []
    for line in block.splitlines():
        row = ROW_RE.match(line.strip())
        if row:
            rows.append((row.group(1), row.group(2).strip(), row.group(3).strip()))
    return rows


def history_rows_from_sidecar(text: str) -> list[tuple[str, str, str]]:
    """Filas (versión, fecha, cambio) del historial de un sidecar YAML."""
    data = yaml.safe_load(text) or {}
    rows: list[tuple[str, str, str]] = []
    for row in data.get("historial") or []:
        if isinstance(row, dict) and row.get("version"):
            rows.append(
                (str(row["version"]), str(row.get("fecha", "")), str(row.get("cambio", "")))
            )
    return rows


DATE_RE = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}(?:T[0-9]{2}:[0-9]{2}(?::[0-9]{2})?(?:Z|[+-][0-9]{2}:[0-9]{2}))?$"
)
DATETIME_RE = re.compile(r"T[0-9]{2}:[0-9]{2}(?::[0-9]{2})?(?:Z|[+-][0-9]{2}:[0-9]{2})$")
HEADER_FECHA_RE = re.compile(
    r"^\|\s*\*{0,2}(?:Fecha|Última actualización)\*{0,2}\s*\|\s*([^|]+?)\s*\|",
    re.MULTILINE,
)


def has_time(fecha: str) -> bool:
    """True si la fecha lleva hora y zona horaria (ISO 8601)."""
    return bool(DATETIME_RE.search(fecha))


def fecha_key(fecha: str):
    """Orden cronológico entre fechas con o sin hora (sin hora = inicio del día UTC)."""
    import datetime

    text = fecha.replace("Z", "+00:00")
    try:
        value = datetime.datetime.fromisoformat(text)
    except ValueError:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=datetime.timezone.utc)
    return value


def load_dates(md_path: Path, root: Path) -> tuple[str | None, list[tuple[str, str]], str]:
    """Fecha de cabecera y filas (versión, fecha) del historial, del sidecar o del cuerpo."""
    side = sidecar_path(md_path, root)
    if side is not None and side.is_file():
        text = side.read_text(encoding="utf-8")
        data = yaml.safe_load(text) or {}
        cab = data.get("cabecera") or {}
        header = data.get("fecha") or cab.get("Fecha") or cab.get("Última actualización")
        rows = [(v, f) for v, f, _ in history_rows_from_sidecar(text)]
        return (str(header) if header else None), rows, "sidecar"
    text = md_path.read_text(encoding="utf-8")
    match = HEADER_FECHA_RE.search(text)
    rows = [(v, f) for v, f, _ in history_rows_from_markdown(text)]
    return (match.group(1).strip() if match else None), rows, "body"
