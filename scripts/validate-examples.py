#!/usr/bin/env python3
"""Valida examples/*.yaml y sdaf.config.example.yaml contra sdaf.config.schema.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "sdaf.config.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)


def main() -> int:
    files = sorted((ROOT / "examples").glob("*.yaml"))
    files.append(ROOT / "sdaf.config.example.yaml")
    errors = 0
    for path in files:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        errs = sorted(VALIDATOR.iter_errors(data), key=lambda e: list(e.path))
        if errs:
            errors += 1
            print(f"FAIL {path.relative_to(ROOT)}")
            for e in errs:
                loc = "/".join(str(p) for p in e.path) or "(root)"
                print(f"  - {loc}: {e.message}")
        else:
            print(f"OK   {path.relative_to(ROOT)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
