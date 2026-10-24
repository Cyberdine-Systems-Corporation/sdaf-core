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

import yaml


def load_product_prefixes(cwd: Path) -> list[str]:
    prefixes = ["src/", "tests/"]
    cfg = cwd / "sdaf.config.yaml"
    if not cfg.is_file():
        return prefixes
    data = yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}
    stack = data.get("stack") or {}
    src = stack.get("src_path") or "src"
    tests = stack.get("tests_path") or "tests"
    prefixes = [str(src).replace("\\", "/").rstrip("/") + "/"]
    prefixes.append(str(tests).replace("\\", "/").rstrip("/") + "/")
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
