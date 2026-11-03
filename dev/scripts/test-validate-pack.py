#!/usr/bin/env python3
"""Comprueba el schema de manifiesto de pack y su validador con fixtures.

Cada caso lanza `validate-pack.py` como proceso y comprueba salida y código de
salida. Los casos en línea se escriben en un directorio temporal (ruta con
espacios) y los fixtures viven en scripts/testdata/pack-*.yaml. Se ejecutan
todos los casos y se informa del número de fallos.
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-pack.py"
SCHEMA = ROOT / "sdaf-pack.schema.json"
DATA = ROOT / "scripts" / "testdata"
FALLOS: list[str] = []

BASE = {
    "id": "sdaf-stack-example",
    "version": "0.1.0",
    "core": ">=0.5.0 <0.7.0",
    "provides": {"skills": ["example-skill"]},
}


def manifest(**cambios) -> str:
    """Manifiesto mínimo válido con cambios; un valor None elimina la clave."""
    datos = copy.deepcopy(BASE)
    for clave, valor in cambios.items():
        if valor is None:
            datos.pop(clave, None)
        else:
            datos[clave] = valor
    return yaml.safe_dump(datos, sort_keys=False)


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def check(nombre: str, ruta: Path, exit_esperado: int, *motivos: str) -> None:
    """Valida `ruta` y exige exit, línea OK/FAIL con la ruta y cada motivo."""
    res = run(str(ruta))
    out = res.stdout
    prefijo = "OK  " if exit_esperado == 0 else "FAIL "
    lineas = [x for x in out.splitlines() if x.startswith(prefijo) and ruta.name in x]
    problemas = []
    if res.returncode != exit_esperado:
        problemas.append(f"exit {res.returncode}, se esperaba {exit_esperado}")
    if not lineas:
        problemas.append(f"falta una línea '{prefijo.strip()} ...{ruta.name}'")
    if "Traceback" in out + res.stderr:
        problemas.append("traceback en la salida")
    for motivo in motivos:
        if motivo not in out:
            problemas.append(f"falta el motivo '{motivo}'")
    if problemas:
        FALLOS.append(nombre)
        print(f"FAIL {nombre}: " + "; ".join(problemas))
        print(out + res.stderr)
    else:
        print(f"OK {nombre}")


def check_schema() -> None:
    """S1: schema 2020-12 válido, $id fijo y additionalProperties false en cada objeto."""
    problemas = []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    if schema.get("$id") != "https://sdaf.local/sdaf-pack.schema.json":
        problemas.append("$id inesperado")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        problemas.append("$schema no es 2020-12")

    def recorrer(nodo, ruta: str) -> None:
        if isinstance(nodo, dict):
            if nodo.get("type") == "object" and nodo.get("additionalProperties") is not False:
                problemas.append(f"{ruta or '(raíz)'} sin additionalProperties: false")
            for clave, valor in nodo.items():
                recorrer(valor, f"{ruta}/{clave}")
        elif isinstance(nodo, list):
            for i, valor in enumerate(nodo):
                recorrer(valor, f"{ruta}/{i}")

    recorrer(schema, "")
    if sorted(schema.get("required", [])) != ["core", "id", "provides", "version"]:
        problemas.append("required debe ser id, version, core y provides")
    if "requires" in schema.get("required", []):
        problemas.append("requires debe ser opcional")
    if problemas:
        FALLOS.append("schema")
        print("FAIL schema: " + "; ".join(problemas))
    else:
        print("OK schema 2020-12 con additionalProperties false")


def fixtures() -> None:
    check("fixture válido", DATA / "pack-valido.yaml", 0)
    casos = [
        ("sin core", "pack-sin-core.yaml", "obligatoria 'core'"),
        ("sin provides", "pack-sin-provides.yaml", "obligatoria 'provides'"),
        ("provides vacío", "pack-provides-vacio.yaml", "provides", "al menos 1"),
        ("id mal formado", "pack-id-mal-formado.yaml", "id:", "patrón"),
        ("version no semver", "pack-version-no-semver.yaml", "version:", "patrón"),
        ("core mal formado", "pack-core-mal-formado.yaml", "core:", "patrón"),
        ("core invertido", "pack-core-invertido.yaml", "core:", "límite inferior"),
        ("propiedad desconocida", "pack-propiedad-desconocida.yaml", "no permitida", "desconocida"),
        ("requires mal formado", "pack-requires-mal-formado.yaml", "requires/0", "mapa"),
        ("requires a sí mismo", "pack-requires-a-si-mismo.yaml", "requires/0/id", "a sí mismo"),
        ("YAML inválido", "pack-yaml-invalido.yaml", "YAML inválido"),
        ("raíz que no es un mapa", "pack-raiz-lista.yaml", "no es un mapa"),
    ]
    for nombre, fichero, *motivos in casos:
        check(f"fixture {nombre}", DATA / fichero, 1, *motivos)


def en_linea(tmp: Path) -> None:
    """Casos que cubren rangos, anidados y listas sin multiplicar fixtures."""
    n = 0

    def caso(nombre: str, texto: str, exit_esperado: int, *motivos: str) -> None:
        nonlocal n
        n += 1
        ruta = tmp / f"caso-{n}.yaml"
        ruta.write_text(texto, encoding="utf-8")
        check(nombre, ruta, exit_esperado, *motivos)

    # Rangos aceptados (incluye orden inverso, igualdad y comparación numérica).
    for core in ["0.5.0", "=0.5.0", ">0.5.0", ">=0.5.0", "<0.7.0 >=0.5.0",
                 ">=0.5.0 <=0.5.0", ">=0.9.0 <0.10.0"]:
        caso(f"core válido {core!r}", manifest(core=core), 0)
    # Sintaxis rechazada por el schema.
    for core in [">=0.5", ">= 0.5.0", ">=0.5.0  <0.7.0", ">=0.5.0 <0.6.0 <0.7.0",
                 ">=0.5.0,<0.7.0", "v0.5.0", ""]:
        caso(f"core sintaxis {core!r}", manifest(core=core), 1, "core:", "patrón")
    # Coherencia del rango (validate-pack.py).
    caso("core vacío por igualdad exclusiva", manifest(core=">0.5.0 <=0.5.0"), 1, "límite inferior")
    caso("core numérico y no léxico", manifest(core=">=0.10.0 <0.9.0"), 1, "límite inferior")
    caso("core con dos límites inferiores", manifest(core=">=0.5.0 >=0.6.0"), 1, "mismo sentido")
    caso("core con igualdad y otro límite", manifest(core="=0.5.0 <0.7.0"), 1, "igualdad")
    # id y version.
    caso("id con mayúsculas", manifest(id="sdaf-stack-Example"), 1, "id:", "patrón")
    caso("id con guion final", manifest(id="sdaf-stack-example-"), 1, "id:", "patrón")
    caso("version con prefijo v", manifest(version="v0.1.0"), 1, "version:", "patrón")
    # Un salto de línea final (p. ej. un bloque literal `|` de YAML) no debe colarse:
    # `$` en las expresiones regulares de Python lo admite, así que lo rechaza el validador.
    caso("id con salto de línea final", manifest(id="sdaf-stack-example\n"), 1, "id:", "saltos de línea")
    caso("version con salto de línea final", manifest(version="0.1.0\n"), 1, "version:", "saltos de línea")
    caso("core con salto de línea final", manifest(core=">=0.5.0 <0.7.0\n"), 1, "core:", "saltos de línea")
    caso("requires con salto de línea final",
         manifest(requires=[{"id": "sdaf-stack-base", "version": ">=1.0.0\n"}]), 1, "requires/0/version", "saltos de línea")
    # provides.
    caso("provides con clave desconocida", manifest(provides={"agents": ["x"]}), 1, "provides", "no permitida")
    caso("provides con lista repetida", manifest(provides={"skills": ["a-b", "a-b"]}), 1, "provides/skills", "repetidos")
    caso("provides con id no kebab-case", manifest(provides={"prompts": ["Example_Prompt"]}), 1, "provides/prompts/0", "patrón")
    caso("provides con lista que no es lista", manifest(provides={"extension_ids": "example-extension"}), 1, "provides/extension_ids", "lista")
    caso("provides con las tres listas", manifest(provides={
        "extension_ids": ["example-extension"], "skills": ["example-skill"], "prompts": ["example-prompt"]}), 0)
    # Lo mismo en cada elemento de provides: un bloque literal `|` deja "id\n".
    caso("provides.extension_ids con salto de línea final",
         manifest(provides={"extension_ids": ["example-extension\n"]}), 1,
         "provides/extension_ids/0", "saltos de línea")
    caso("provides.skills con salto de línea final",
         manifest(provides={"skills": ["a-skill\n"]}), 1, "provides/skills/0", "saltos de línea")
    caso("provides.prompts con salto de línea final",
         manifest(provides={"prompts": ["example-prompt\n"]}), 1, "provides/prompts/0", "saltos de línea")
    # requires.
    req = {"id": "sdaf-stack-base", "version": ">=1.0.0 <2.0.0"}
    caso("requires válido", manifest(requires=[req]), 0)
    caso("requires con propiedad extra", manifest(requires=[{**req, "extra": 1}]), 1, "requires/0", "no permitida")
    caso("requires sin version", manifest(requires=[{"id": req["id"]}]), 1, "obligatoria 'version'")
    caso("requires sin id", manifest(requires=[{"version": req["version"]}]), 1, "obligatoria 'id'")
    caso("requires con id mal formado", manifest(requires=[{**req, "id": "base"}]), 1, "requires/0/id", "patrón")
    caso("requires con version mal formada", manifest(requires=[{**req, "version": "^1.0.0"}]), 1, "requires/0/version", "patrón")
    caso("requires con rango invertido", manifest(requires=[{**req, "version": ">=2.0.0 <1.0.0"}]), 1,
         "requires/0/version", "límite inferior")
    caso("requires repetido", manifest(requires=[req, dict(req)]), 1, "requires", "repetidos")
    caso("requires que no es lista", manifest(requires=req), 1, "requires", "lista")
    caso("requires a sí mismo en el segundo elemento",
         manifest(requires=[req, {**req, "id": BASE["id"]}]), 1, "requires/1/id", "a sí mismo")
    # Mensajes sin traceback.
    caso("fichero vacío", "", 1, "no es un mapa")
    caso("valor escalar", "hola\n", 1, "no es un mapa")


def cli(tmp: Path) -> None:
    res = run()
    ok = res.returncode == 0 and "OK  templates/sdaf-pack.yaml" in res.stdout
    print("OK sin argumentos valida la plantilla" if ok else f"FAIL sin argumentos\n{res.stdout}{res.stderr}")
    if not ok:
        FALLOS.append("sin argumentos")

    res = run("no-existe.yaml")
    ok = res.returncode == 1 and "FAIL" in res.stdout and "inexistente" in res.stdout
    print("OK ruta inexistente" if ok else f"FAIL ruta inexistente\n{res.stdout}{res.stderr}")
    if not ok:
        FALLOS.append("ruta inexistente")

    invalido = tmp / "no-utf8.yaml"
    invalido.write_bytes(b"id: sdaf-stack-example\ndescripcion: \xff\xfe\n")
    check("fichero no UTF-8", invalido, 1, "UTF-8")

    res = run(str(DATA / "pack-valido.yaml"), str(DATA / "pack-sin-core.yaml"))
    ok = res.returncode == 1 and "OK  " in res.stdout and "FAIL " in res.stdout
    print("OK varias rutas: informa de cada una y sale 1" if ok else f"FAIL varias rutas\n{res.stdout}{res.stderr}")
    if not ok:
        FALLOS.append("varias rutas")


def main() -> int:
    check_schema()
    fixtures()
    with tempfile.TemporaryDirectory(prefix="sdaf pack ") as tmpdir:
        tmp = Path(tmpdir)
        en_linea(tmp)
        cli(tmp)
    print(f"fallos: {len(FALLOS)}")
    return 1 if FALLOS else 0


if __name__ == "__main__":
    sys.exit(main())
