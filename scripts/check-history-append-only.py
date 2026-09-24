#!/usr/bin/env python3
"""Falla si una fila de Historial que existía en la base ha desaparecido o cambiado.

El historial publicado solo crece: se añaden filas, no se reescriben
(criterio de H08 §7 aplicado a la norma publicada). Compara cada artefacto
versionado contra la ref base, tanto si el historial vive en el cuerpo
como en handbook/_meta (el artefacto puede haber cambiado de formato).

Desde la línea 0.4.0, una fila nueva de una versión que la base no tenía
lleva fecha con hora y zona (ISO 8601). Las filas que describen versiones ya
publicadas pueden conservar solo el día.

Ref base: --base; en un PR de GitHub, el SHA base del evento; si no, HEAD
(compara el árbol de trabajo con el último commit).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sdaf_meta import (  # noqa: E402
    HEADER_VERSION_RE,
    has_time,
    parse_semver,
    history_rows_from_markdown,
    history_rows_from_sidecar,
    sidecar_path,
)

INCLUDE_GLOBS = [
    "handbook/*.md",
    "agents/*.md",
    "prompts/**/*.md",
    "skills/**/*.md",
    "templates/*.md",
    "AGENTS.md.template",
]


def normalize(cambio: str) -> str:
    """Ignora el marcado que se pierde al pasar de tabla markdown a YAML."""
    text = re.sub(r"[`*\"«»]", "", cambio)
    return re.sub(r"\s+", " ", text).strip()


def git_show(ref: str, rel: str) -> str | None:
    proc = subprocess.run(
        ["git", "show", f"{ref}:{rel}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return proc.stdout if proc.returncode == 0 else None


def rows_at(ref: str | None, md_rel: str) -> list[tuple[str, str, str]]:
    """Historial de un artefacto en una ref (None = árbol de trabajo)."""
    side = sidecar_path(ROOT / md_rel, ROOT)
    side_rel = side.relative_to(ROOT).as_posix() if side is not None else None
    if ref is None:
        if side is not None and side.is_file():
            return history_rows_from_sidecar(side.read_text(encoding="utf-8"))
        path = ROOT / md_rel
        return history_rows_from_markdown(path.read_text(encoding="utf-8")) if path.is_file() else []
    if side_rel is not None:
        text = git_show(ref, side_rel)
        if text is not None:
            return history_rows_from_sidecar(text)
    text = git_show(ref, md_rel)
    return history_rows_from_markdown(text) if text is not None else []


def header_version_at(ref: str, md_rel: str) -> str | None:
    """Versión de cabecera publicada en la ref (sidecar o tabla del cuerpo)."""
    side = sidecar_path(ROOT / md_rel, ROOT)
    if side is not None:
        text = git_show(ref, side.relative_to(ROOT).as_posix())
        if text is not None:
            match = re.search(r"^version:\s*\"?([0-9.]+)", text, re.MULTILINE)
            if match:
                return match.group(1)
    text = git_show(ref, md_rel)
    if text is None:
        return None
    match = HEADER_VERSION_RE.search(text)
    return match.group(1) if match else None


def base_ref(cli: str | None) -> str:
    if cli:
        return cli
    if os.environ.get("GITHUB_EVENT_NAME") == "pull_request":
        event_path = os.environ.get("GITHUB_EVENT_PATH")
        if event_path and Path(event_path).is_file():
            payload = json.loads(Path(event_path).read_text(encoding="utf-8"))
            sha = (payload.get("pull_request") or {}).get("base", {}).get("sha")
            if sha:
                return sha
    return "HEAD"


def targets() -> list[str]:
    found: set[str] = set()
    for glob in INCLUDE_GLOBS:
        for path in ROOT.glob(glob):
            if path.name == "CHANGELOG.md":
                continue
            found.add(path.relative_to(ROOT).as_posix())
    return sorted(found)


def main() -> int:
    global ROOT
    parser = argparse.ArgumentParser(description="Historial solo crece.")
    parser.add_argument("--base", default=None, help="Ref git contra la que comparar.")
    parser.add_argument("--root", default=str(ROOT), help="Raíz del repo git a comprobar (fixtures).")
    args = parser.parse_args()
    ROOT = Path(args.root).resolve()
    ref = base_ref(args.base)

    probe = subprocess.run(
        ["git", "rev-parse", "--verify", f"{ref}^{{commit}}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if probe.returncode != 0:
        print(f"FAIL ref base no disponible: {ref} (¿checkout con fetch-depth: 0?)")
        return 1

    failed = 0
    checked = 0
    for rel in targets():
        before = rows_at(ref, rel)
        published = header_version_at(ref, rel)
        base_keys = {(v, f.strip()) for v, f, _ in before}
        for version, fecha, _ in rows_at(None, rel):
            if (version, fecha.strip()) in base_keys or has_time(fecha.strip()):
                continue
            # Una fila que describe una versión ya publicada puede quedarse con el día.
            if published and parse_semver(version) <= parse_semver(published):
                continue
            failed += 1
            print(f"FAIL {rel}: la fila nueva {version} | {fecha} no lleva hora y zona (ISO 8601)")
        if not before:
            continue
        checked += 1
        now = Counter((v, f.strip(), normalize(c)) for v, f, c in rows_at(None, rel))
        lost = Counter((v, f.strip(), normalize(c)) for v, f, c in before) - now
        for (version, fecha, cambio), n in sorted(lost.items()):
            failed += 1
            print(f"FAIL {rel}: falta la fila {version} | {fecha} | {cambio}" + (f" (x{n})" if n > 1 else ""))
    if failed:
        print(f"{failed} fila(s) de historial desaparecidas, reescritas o sin hora respecto a {ref}")
        return 1
    print(f"OK historial solo crece respecto a {ref} ({checked} artefactos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
