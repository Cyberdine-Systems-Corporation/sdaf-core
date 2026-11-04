#!/usr/bin/env python3
"""Valida manifiestos de pack (sdaf-pack.yaml) contra el schema y la coherencia.

Sin argumentos: templates/sdaf-pack.yaml. Salida `OK  <ruta>` o una línea
`FAIL <ruta>: <motivo>` por cada problema; sale 0 si todo valida y 1 si hay algún
FAIL. Un YAML inválido, un fichero que no es UTF-8 o una raíz que no es un mapa
son FAIL, nunca un traceback.

Además del schema (sdaf-pack.schema.json) comprueba, en `core` y en cada
`requires[].version`, la coherencia del rango, que un pack no se requiere a sí
mismo, y que `id`, `version`, `core`, los valores de `requires` y cada elemento de
`provides` no lleven espacios o saltos de línea en los extremos. Las reglas del
manifiesto (schema, rangos y bordes) viven en sdaf_packs.py. Un rango son uno o dos comparadores
`X.Y.Z` separados por un espacio. Los comparadores admitidos son `>=` y `>`
(límite inferior), `<=` y `<` (límite superior) y `=` o ninguno (versión exacta).
Las versiones se comparan como tuplas
de enteros (0.10.0 es mayor que 0.9.0), nunca como texto. Con dos comparadores
debe haber un límite inferior y uno superior, en cualquier orden; el rango no
puede quedar vacío: el inferior debe ser menor que el superior, salvo
`>=X.Y.Z <=X.Y.Z`, que fija una única versión. La igualdad no se combina con
otro comparador.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sdaf_packs import ROOT, label_of, manifest_file_issues  # noqa: E402

TEMPLATE = ROOT / "templates" / "sdaf-pack.yaml"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Valida manifiestos de pack (sdaf-pack.yaml) contra schema y coherencia."
    )
    parser.add_argument(
        "paths", nargs="*", help="Rutas YAML. Sin argumentos: templates/sdaf-pack.yaml"
    )
    args = parser.parse_args(argv)

    failed = False
    for raw in args.paths or [str(TEMPLATE)]:
        path = Path(raw)
        if not path.is_file():
            print(f"FAIL {raw}: ruta inexistente o no es un fichero")
            failed = True
            continue
        reasons = manifest_file_issues(path)
        label = label_of(path)
        if reasons:
            failed = True
            for reason in reasons:
                print(f"FAIL {label}: {reason}")
        else:
            print(f"OK  {label}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
