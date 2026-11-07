"""Diff reutilizable contra git: qué rutas cambian y cuáles caen bajo las rutas de código configuradas.

check-worklog-presence.py (con guion en el nombre, no importable) la usa y
otros comprobadores pueden reutilizarla. API pura: sin main, sin efectos
sobre el proceso. `git_changed` ejecuta git en el `cwd` que recibe.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, NamedTuple

import yaml


class ConfigUnreadable(ValueError):
    """`sdaf.config.yaml` existe pero no se pueden leer de él las rutas de código; el mensaje es el motivo."""


class Unit(NamedTuple):
    """Una unidad de código del consumidor: `name` solo en `stack.units`, `tests` es opcional."""

    name: str | None
    src: str
    tests: str | None


def _mapping(value: Any, what: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ConfigUnreadable(f"«{what}» no es un mapa")
    return value


def _path_text(value: Any, what: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigUnreadable(f"{what} no es un texto no vacío")
    return value


def _unit(item: Any, index: int) -> Unit:
    where = f"stack.units[{index}]"
    if not isinstance(item, dict):
        raise ConfigUnreadable(f"{where} no es un mapa")
    name = item.get("name")
    tests = item.get("tests")
    return Unit(
        name if isinstance(name, str) else None,
        _path_text(item.get("src"), f"{where}.src"),
        None if tests is None else _path_text(tests, f"{where}.tests"),
    )


def load_units(cwd: Path) -> list[Unit]:
    """Unidades de código del consumidor: `stack.units` o, si no hay, la única del atajo.

    Sin `sdaf.config.yaml` devuelve la unidad por defecto (`src`, `tests`). Con `stack.units`
    gana la lista sobre `src_path`/`tests_path` (validate-config ya rechaza que convivan).
    Una config que no se puede leer lanza `ConfigUnreadable` con el motivo; nunca otra excepción.
    """
    cfg = cwd / "sdaf.config.yaml"
    if not cfg.is_file():
        return [Unit(None, "src", "tests")]
    try:
        data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        raise ConfigUnreadable("el YAML no es válido") from None
    except UnicodeDecodeError:
        raise ConfigUnreadable("el fichero no es UTF-8") from None
    except OSError:
        raise ConfigUnreadable("no se puede leer el fichero") from None
    stack = _mapping(_mapping(data, "raíz").get("stack"), "stack")
    if "units" in stack:
        units = stack["units"]
        if not isinstance(units, list) or not units:
            raise ConfigUnreadable("stack.units no es una lista con al menos una unidad")
        return [_unit(item, i) for i, item in enumerate(units)]
    return [Unit(None, str(stack.get("src_path") or "src"), str(stack.get("tests_path") or "tests"))]


def _prefix(path: str) -> str:
    return path.replace("\\", "/").rstrip("/") + "/"


def load_product_prefixes(cwd: Path) -> list[str]:
    """Prefijos de las rutas de código de todas las unidades (src y, si hay, tests), sin repetir."""
    prefixes: list[str] = []
    for unit in load_units(cwd):
        for path in (unit.src, unit.tests):
            if path is not None and _prefix(path) not in prefixes:
                prefixes.append(_prefix(path))
    return prefixes


def is_product(path: str, prefixes: list[str]) -> bool:
    norm = path.replace("\\", "/")
    return any(norm == p.rstrip("/") or norm.startswith(p) for p in prefixes)


class DiffUnavailable(Exception):
    """Hay un PR que comprobar pero git no puede calcular su diff."""


def git_changed(base: str | None, cwd: Path) -> list[str] | None:
    if os.environ.get("GITHUB_EVENT_NAME") == "pull_request":
        event_path = os.environ.get("GITHUB_EVENT_PATH")
        sha = None
        if event_path and Path(event_path).is_file():
            payload = json.loads(Path(event_path).read_text(encoding="utf-8"))
            sha = (payload.get("pull_request") or {}).get("base", {}).get("sha")
        sha = sha or os.environ.get("GITHUB_BASE_SHA")
        if not sha:
            raise DiffUnavailable("evento pull_request sin SHA base")
        proc = subprocess.run(
            ["git", "diff", "--name-only", f"{sha}...HEAD"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=cwd,
        )
        if proc.returncode != 0:
            raise DiffUnavailable(proc.stderr.strip() or f"git diff {sha}...HEAD falló")
        return [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    if base:
        proc = subprocess.run(
            ["git", "diff", "--name-only", f"{base}...HEAD"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=cwd,
        )
        if proc.returncode != 0:
            raise DiffUnavailable(proc.stderr.strip() or f"git diff {base}...HEAD falló")
        return [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    return None
