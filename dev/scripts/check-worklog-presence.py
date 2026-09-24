#!/usr/bin/env python3
"""Falla si el diff toca código de producto y no hay cambio bajo worklogs/.

No parsea campos del worklog. Un diff solo de markdown (typo) sale 0.
Sin diff de PR y sin --changed: sale 0 (nada que comprobar).
En un PR, si no se puede calcular el diff (checkout superficial, base
ausente), sale 1: el chequeo no se da por bueno sin haber mirado.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKLOG_PREFIX = "worklogs/"
MD_SUFFIXES = {".md", ".md.template"}


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


def is_worklog(path: str) -> bool:
    return path.replace("\\", "/").startswith(WORKLOG_PREFIX)


def is_markdown(path: str) -> bool:
    norm = path.replace("\\", "/").lower()
    return Path(norm).suffix.lower() in {".md"} or norm.endswith(".md.template")


class DiffUnavailable(Exception):
    """Hay un PR que comprobar pero git no puede calcular su diff."""


def git_changed(base: str | None) -> list[str] | None:
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
        )
        if proc.returncode != 0:
            raise DiffUnavailable(proc.stderr.strip() or f"git diff {base}...HEAD falló")
        return [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Exige worklog si hay código de producto.")
    parser.add_argument("--changed", nargs="*", help="Lista de rutas (modo prueba).")
    parser.add_argument("--base", default=None, help="Ref git para diff local.")
    parser.add_argument("--cwd", default=".", help="Raíz del repo a inspeccionar.")
    args = parser.parse_args()
    cwd = Path(args.cwd).resolve()
    prefixes = load_product_prefixes(cwd)

    if args.changed is not None:
        changed = [p.replace("\\", "/") for p in args.changed]
    else:
        os.chdir(cwd)
        try:
            changed = git_changed(args.base)
        except DiffUnavailable as exc:
            print(f"FAIL no se pudo calcular el diff del PR: {exc}")
            print("  Revisa que el checkout use fetch-depth: 0.")
            return 1
        if changed is None:
            print("OK sin diff de PR que comprobar")
            return 0

    if not changed:
        print("OK diff vacío")
        return 0

    product = [p for p in changed if is_product(p, prefixes)]
    if not product:
        print("OK sin código de producto en el diff")
        return 0

    if any(is_worklog(p) for p in changed):
        print("OK worklog presente en el diff")
        return 0

    print("FAIL el diff toca código de producto y no modifica worklogs/:")
    for p in product:
        print(f"  - {p}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
