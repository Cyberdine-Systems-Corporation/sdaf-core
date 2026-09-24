#!/usr/bin/env python3
"""Envoltura de compatibilidad. Preferir scripts/validate-config.py."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).with_name("validate-config.py")


def main() -> int:
    return subprocess.call([sys.executable, str(SCRIPT), *sys.argv[1:]])


if __name__ == "__main__":
    sys.exit(main())
