#!/usr/bin/env python3
"""Valida sdaf.config.yaml (o rutas dadas) contra el JSON Schema y las invariantes.

Sin argumentos: examples/*.yaml y sdaf.config.example.yaml.
I1–I3 son error. I4 es aviso salvo --strict-i4.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "sdaf.config.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)

CORE_IDS = {
    "specification",
    "architecture",
    "testing-review",
    "product",
    "domain",
    "application",
    "devops",
    "review",
    "testing",
}
EXTENSION_IDS = {
    "domain-application",
    "frontend",
    "infrastructure",
    "ai",
}


def _list(value) -> list:
    if not value:
        return []
    if isinstance(value, list):
        return [str(x) for x in value]
    return []


def collect_ids(data: dict) -> tuple[list[str], list[str], dict[str, list[str]]]:
    agents = data.get("agents") or {}
    active = _list(agents.get("active"))
    stubs = _list(agents.get("stubs"))
    fusions = agents.get("fusions") or {}
    if not isinstance(fusions, dict):
        fusions = {}
    fused = {str(k): _list(v) for k, v in fusions.items()}
    return active, stubs, fused


def semantic_issues(
    data: dict,
    *,
    strict_i4: bool = False,
    consumer_root: Path | None = None,
) -> tuple[list[str], list[str]]:
    """Devuelve (errores, avisos)."""
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return ["la raíz no es un objeto"], []

    active, stubs, fusions = collect_ids(data)
    active_set = set(active)
    stubs_set = set(stubs)

    overlap = active_set & stubs_set
    if overlap:
        ids = ", ".join(sorted(overlap))
        errors.append(f"I1: id(s) a la vez en active y stubs: {ids}")

    for key in fusions:
        if key not in active_set:
            errors.append(f"I2: clave de fusions no está en active: {key}")

    for key, members in fusions.items():
        for member in members:
            if member in active_set:
                errors.append(
                    f"I3: miembro de fusión {key} está en active: {member}"
                )

    pack = None
    stack = data.get("stack") if isinstance(data.get("stack"), dict) else {}
    pack = stack.get("pack")

    used = set(active) | set(stubs) | set(fusions)
    for members in fusions.values():
        used.update(members)

    extension_used = sorted(
        i for i in used if i in EXTENSION_IDS or (i not in CORE_IDS)
    )
    if extension_used and not pack:
        missing_contracts: list[str] = []
        if consumer_root is not None:
            for ext_id in extension_used:
                contract = consumer_root / "agents" / f"{ext_id}-agent.md"
                if not contract.is_file():
                    missing_contracts.append(ext_id)
        msg_ids = ", ".join(extension_used)
        detail = f"I4: id(s) de extensión sin stack.pack: {msg_ids}"
        if consumer_root is not None and missing_contracts:
            detail += (
                " (sin contrato local: "
                + ", ".join(missing_contracts)
                + ")"
            )
        if strict_i4:
            errors.append(detail)
        else:
            warnings.append(detail)

    return errors, warnings


def default_files() -> list[Path]:
    files = sorted((ROOT / "examples").glob("*.yaml"))
    files.append(ROOT / "sdaf.config.example.yaml")
    return files


def resolve_paths(raw: list[str]) -> tuple[list[Path], list[str]]:
    found: list[Path] = []
    missing: list[str] = []
    for item in raw:
        path = Path(item)
        if not path.is_absolute():
            path = Path.cwd() / path
        if not path.is_file():
            missing.append(item)
            continue
        found.append(path)
    return found, missing


def validate_file(
    path: Path,
    *,
    strict_i4: bool,
    consumer_root: Path | None,
) -> tuple[bool, list[str], list[str]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    schema_errs = sorted(VALIDATOR.iter_errors(data), key=lambda e: list(e.path))
    messages: list[str] = []
    for e in schema_errs:
        loc = "/".join(str(p) for p in e.path) or "(root)"
        messages.append(f"{loc}: {e.message}")
    sem_err, sem_warn = semantic_issues(
        data if isinstance(data, dict) else {},
        strict_i4=strict_i4,
        consumer_root=consumer_root,
    )
    messages.extend(sem_err)
    ok = not schema_errs and not sem_err
    return ok, messages, sem_warn


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Valida sdaf.config.yaml contra schema e invariantes."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Rutas YAML. Sin argumentos: examples/ + sdaf.config.example.yaml",
    )
    parser.add_argument(
        "--strict-i4",
        action="store_true",
        help="I4 (ids de extensión sin pack) es error en lugar de aviso.",
    )
    parser.add_argument(
        "--consumer-root",
        type=Path,
        default=None,
        help="Raíz del consumidor para buscar contratos locales (I4).",
    )
    args = parser.parse_args(argv)

    if args.paths:
        files, missing = resolve_paths(args.paths)
        if missing:
            for item in missing:
                print(f"FAIL ruta inexistente: {item}")
            return 1
    else:
        files = default_files()

    errors = 0
    for path in files:
        try:
            rel = path.resolve().relative_to(ROOT.resolve())
            label = str(rel).replace("\\", "/")
        except ValueError:
            label = str(path)
        ok, messages, warnings = validate_file(
            path,
            strict_i4=args.strict_i4,
            consumer_root=args.consumer_root,
        )
        if ok:
            print(f"OK   {label}")
        else:
            errors += 1
            print(f"FAIL {label}")
            for msg in messages:
                print(f"  - {msg}")
        for warn in warnings:
            print(f"WARN {label}: {warn}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
