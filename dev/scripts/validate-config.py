#!/usr/bin/env python3
"""Valida sdaf.config.yaml (o rutas dadas) contra el JSON Schema y las invariantes.

Sin argumentos: examples/*.yaml y sdaf.config.example.yaml.
I1–I3 son error. I4 es aviso salvo --strict-i4. T1 es siempre aviso.
Los packs se declaran en stack.packs; stack.pack es un alias obsoleto que avisa.
Un YAML roto, un fichero que no es UTF-8 o una raíz que no es un mapa son FAIL,
nunca un traceback.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sdaf_packs import edge_issue  # noqa: E402
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
# Última release de gentle-ai que incluye el componente sdd (retirado en main por
# el merge 520ed86e8 y ausente desde v4.0.0). Un SHA no se evalúa: sin red no se sabe
# si es anterior.
GENTLE_AI_LAST_SDD = (3, 7, 0)
SEMVER_RE = re.compile(r"^([0-9]+)\.([0-9]+)\.([0-9]+)$")


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


def declared_packs(stack: dict) -> tuple[list[str], bool]:
    """Devuelve (referencias `id@version` declaradas, si se usa el alias stack.pack).

    Las referencias salen de `stack.packs`; si solo hay alias no nulo, de
    `[stack.pack]`; si no hay ninguna, de `[]`. `stack.pack: null` no cuenta
    como alias. Solo se recogen cadenas: el schema rechaza el resto.
    """
    alias = stack.get("pack")
    packs = stack.get("packs")
    if isinstance(packs, list):
        refs = [x for x in packs if isinstance(x, str)]
    elif "packs" not in stack and isinstance(alias, str) and alias:
        refs = [alias]
    else:
        refs = []
    return refs, alias is not None


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

    stack = data.get("stack") if isinstance(data.get("stack"), dict) else {}
    packs, alias_used = declared_packs(stack)

    if alias_used and "packs" in stack:
        errors.append(
            "stack: stack.pack y stack.packs no pueden coexistir; "
            "usar solo stack.packs"
        )
    elif alias_used:
        warnings.append(
            "stack.pack está obsoleto; usar stack.packs: "
            f"[{json.dumps(stack['pack'], ensure_ascii=False)}]"
        )

    by_id: dict[str, list[str]] = {}
    for ref in dict.fromkeys(packs):
        by_id.setdefault(ref.split("@", 1)[0], []).append(ref)
    for pack_id, refs in by_id.items():
        if len(refs) > 1:
            errors.append(
                f"stack/packs: el id {pack_id} está repetido con distinta versión "
                f"({', '.join(refs)})"
            )

    sdaf_block = data.get("sdaf") if isinstance(data.get("sdaf"), dict) else {}
    tooling = data.get("tooling") if isinstance(data.get("tooling"), dict) else {}
    edges = [
        ("sdaf/version", sdaf_block.get("version")),
        ("stack/pack", stack.get("pack")),
        ("tooling/gentle_ai", tooling.get("gentle_ai")),
    ]
    if isinstance(stack.get("packs"), list):
        edges.extend((f"stack/packs/{i}", ref) for i, ref in enumerate(stack["packs"]))
    for where, value in edges:
        issue = edge_issue(where, value)
        if issue:
            errors.append(issue)

    used = set(active) | set(stubs) | set(fusions)
    for members in fusions.values():
        used.update(members)

    extension_used = sorted(
        i for i in used if i in EXTENSION_IDS or (i not in CORE_IDS)
    )
    if extension_used and not packs:
        missing_contracts: list[str] = []
        if consumer_root is not None:
            for ext_id in extension_used:
                contract = consumer_root / "agents" / f"{ext_id}-agent.md"
                if not contract.is_file():
                    missing_contracts.append(ext_id)
        msg_ids = ", ".join(extension_used)
        detail = f"I4: id(s) de extensión sin packs: {msg_ids}"
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

    gentle_ai = tooling.get("gentle_ai")
    match = SEMVER_RE.match(gentle_ai) if isinstance(gentle_ai, str) else None
    if match and tuple(int(g) for g in match.groups()) <= GENTLE_AI_LAST_SDD:
        warnings.append(
            f"T1: gentle-ai {gentle_ai} incluye el componente sdd; "
            "no instalarlo (ADR-004)"
        )

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


def load(path: Path) -> tuple[object, str | None]:
    """Lee el YAML; devuelve (datos, motivo de error o None)."""
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as exc:
        return None, f"el fichero no es UTF-8 válido (byte inválido en la posición {exc.start})"
    except OSError as exc:
        return None, f"no se puede leer el fichero: {exc.strerror or exc}"
    try:
        return yaml.safe_load(text), None
    except yaml.YAMLError as exc:
        return None, "YAML inválido: " + " ".join(str(exc).split())


def validate_file(
    path: Path,
    *,
    strict_i4: bool,
    consumer_root: Path | None,
) -> tuple[bool, list[str], list[str]]:
    data, error = load(path)
    if error:
        return False, [error], []
    if not isinstance(data, dict):
        return False, [f"la raíz no es un mapa (se encontró {type(data).__name__})"], []
    schema_errs = sorted(VALIDATOR.iter_errors(data), key=lambda e: list(e.path))
    messages: list[str] = []
    for e in schema_errs:
        loc = "/".join(str(p) for p in e.path) or "(root)"
        if e.validator == "anyOf" and list(e.path) == ["stack"]:
            messages.append(f"{loc}: falta stack.packs (o el alias obsoleto stack.pack)")
        else:
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
