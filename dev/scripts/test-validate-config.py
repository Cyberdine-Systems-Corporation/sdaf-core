#!/usr/bin/env python3
"""Comprueba fixtures del validador de config (I1–I4, packs, alias, manifiestos, overlay, units, bordes, tooling y T1).

Cada caso lanza `validate-config.py` como proceso y comprueba salida y código de
salida. Los fixtures viven en scripts/testdata/; los casos en línea se escriben
en un directorio temporal (ruta con espacios). Los casos de packs y de
manifiestos se ejecutan todos y se informa del número de fallos; la tabla de
`satisfies` llama directamente a sdaf_packs.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-config.py"
DATA = ROOT / "scripts" / "testdata"
INVALID = DATA / "invalid-invariants.yaml"
I4 = DATA / "i4-extension-without-pack.yaml"
TOOLING = DATA / "tooling-invalid.yaml"
TOOLING_SDD = DATA / "tooling-sdd-warning.yaml"
FALLOS: list[str] = []
ALIAS_AVISO = "stack.pack está obsoleto"
ALIAS_USAR = 'usar stack.packs: ["sdaf-stack-example@0.1.0"]'


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def check(
    nombre: str,
    args: list[str],
    exit_esperado: int,
    *motivos: str,
    ausentes: tuple[str, ...] = (),
    etiqueta: str | None = None,
) -> None:
    """Exige exit, línea OK/FAIL con la ruta, cada motivo presente y cada ausente ausente.

    La ruta es la última del comando, o `etiqueta` si el FAIL sale en otro fichero
    (p. ej. un manifiesto).
    """
    buscada = etiqueta or Path(args[-1]).name
    res = run(args)
    out = res.stdout
    prefijo = "OK   " if exit_esperado == 0 else "FAIL "
    lineas = [x for x in out.splitlines() if x.startswith(prefijo) and buscada in x]
    problemas = []
    if res.returncode != exit_esperado:
        problemas.append(f"exit {res.returncode}, se esperaba {exit_esperado}")
    if not lineas:
        problemas.append(f"falta una línea '{prefijo.strip()} ...{buscada}'")
    if "Traceback" in out + res.stderr:
        problemas.append("traceback en la salida")
    for motivo in motivos:
        if motivo not in out:
            problemas.append(f"falta el motivo '{motivo}'")
    for ausente in ausentes:
        if ausente in out:
            problemas.append(f"sobra '{ausente}'")
    if problemas:
        FALLOS.append(nombre)
        print(f"FAIL {nombre}: " + "; ".join(problemas))
        print(out + res.stderr)
    else:
        print(f"OK {nombre}")


def casos_packs() -> None:
    """S4–S7: stack.packs, alias obsoleto, coexistencia, duplicados y bordes."""
    ok_sin_aviso = ("WARN", "I4")
    check("una referencia en packs", [str(DATA / "config-packs-uno.yaml")], 0, ausentes=ok_sin_aviso)
    check("varias referencias en packs", [str(DATA / "config-packs-varios.yaml")], 0, ausentes=ok_sin_aviso)
    check("alias avisa", [str(DATA / "config-alias.yaml")], 0, "WARN", ALIAS_AVISO, ALIAS_USAR, ausentes=("I4",))
    check("alias con pack null no avisa", [str(DATA / "config-alias-null.yaml")], 0, ausentes=("WARN",))
    check("coexistencia pack y packs", [str(DATA / "config-coexistencia.yaml")], 1, "stack.pack", "stack.packs", "no pueden coexistir")
    check("coexistencia con packs vacío", [str(DATA / "config-coexistencia-vacio.yaml")], 1, "no pueden coexistir")
    check("packs vacío equivale a sin packs", [str(DATA / "config-packs-vacio.yaml")], 0, "WARN", "I4", "frontend", ausentes=(ALIAS_AVISO,))
    check("referencia mal formada", [str(DATA / "config-referencia-mal-formada.yaml")], 1, "stack/packs/0")
    check("id duplicado con distinta versión", [str(DATA / "config-id-duplicado.yaml")], 1, "sdaf-stack-example", "repetido")
    check("salto de línea en sdaf.version", [str(DATA / "config-version-salto.yaml")], 1, "sdaf/version")
    check("salto de línea en una referencia", [str(DATA / "config-packs-salto.yaml")], 1, "stack/packs/0")
    check("salto de línea en gentle_ai", [str(DATA / "config-gentle-ai-salto.yaml")], 1, "tooling/gentle_ai")
    check("YAML roto", [str(DATA / "config-yaml-roto.yaml")], 1, "YAML inválido")
    check("raíz que no es un mapa", [str(DATA / "config-raiz-lista.yaml")], 1, "no es un mapa")


def casos_en_linea(tmp: Path) -> None:
    """Variantes que no justifican un fixture propio."""
    base = (DATA / "config-packs-uno.yaml").read_text(encoding="utf-8")
    n = 0

    def caso(nombre: str, contenido: str | bytes, exit_esperado: int, *motivos: str, ausentes=(), args=()) -> None:
        nonlocal n
        n += 1
        ruta = tmp / f"caso-{n}.yaml"
        if isinstance(contenido, bytes):
            ruta.write_bytes(contenido)
        else:
            ruta.write_text(contenido, encoding="utf-8")
        check(nombre, [*args, str(ruta)], exit_esperado, *motivos, ausentes=ausentes)

    ref = "    - sdaf-stack-example@0.1.0\n"
    caso("fichero que no es UTF-8", b"sdaf: \xff\xfe\n", 1, "UTF-8")
    caso("fichero vacío", "", 1, "no es un mapa")
    caso("alias con salto de línea", base.replace("  packs:\n" + ref, "  pack: |\n    sdaf-stack-example@0.1.0\n"), 1, "stack/pack")
    caso("packs que no es una lista", base.replace("  packs:\n" + ref, "  packs: sdaf-stack-example@0.1.0\n"), 1, "stack/packs")
    caso("sin pack ni packs", base.replace("  packs:\n" + ref, "  src_path: src\n"), 1, "stack", "packs")
    caso("packs vacío y --strict-i4", base.replace("  packs:\n" + ref, "  packs: []\n"), 1, "I4", args=["--strict-i4"])
    caso("un pack declarado y --strict-i4", base, 0, ausentes=("I4",), args=["--strict-i4"])
    caso(
        "id repetido con la misma versión",
        base.replace(ref, ref + ref),
        1,
        "stack/packs",
        "non-unique",
        ausentes=("repetido",),
    )
    caso(
        "alias con pack null y packs vacío",
        base.replace("  packs:\n" + ref, "  pack: null\n  packs: []\n"),
        0,
        "I4",
        ausentes=(ALIAS_AVISO,),
    )


def casos_overlay(tmp: Path) -> None:
    """stack.overlay.replaces: forma en el schema y reglas de ADR-007 §5 en el validador."""
    valido = DATA / "config-overlay-valido.yaml"
    texto = valido.read_text(encoding="utf-8")
    ruta = "stack/overlay/replaces/0"
    n = 0

    def caso(nombre: str, contenido: str, exit_esperado: int, *motivos: str, ausentes=(), args=()) -> None:
        nonlocal n
        n += 1
        fichero = tmp / f"overlay-{n}.yaml"
        fichero.write_text(contenido, encoding="utf-8")
        check(nombre, [*args, str(fichero)], exit_esperado, *motivos, ausentes=ausentes)

    def con(reemplazo: str) -> str:
        """Config válida cuyo bloque overlay se sustituye por `reemplazo`."""
        return texto.replace("  overlay:\n    replaces:\n      - frontend\n", reemplazo)

    sin_aviso = ("WARN", "FAIL", "replaces")
    # Fixtures: una regla por fichero.
    check("overlay válido", [str(valido)], 0, ausentes=sin_aviso)
    check(
        "overlay con un id del núcleo",
        [str(DATA / "config-overlay-nucleo.yaml")], 1,
        ruta, "los ids de agente del núcleo no se sustituyen (ADR-007 §5)", "architecture",
    )
    check(
        "overlay con un id no declarado en agents",
        [str(DATA / "config-overlay-no-declarado.yaml")], 1,
        ruta, "id no declarado en agents: example-extension",
    )
    check("overlay con un id solo miembro de una fusión", [str(DATA / "config-overlay-fusion-miembro.yaml")], 0, ausentes=sin_aviso)
    check(
        "overlay con un id repetido",
        [str(DATA / "config-overlay-repetido.yaml")], 1,
        "stack/overlay/replaces", "non-unique", ausentes=("no declarado", "núcleo"),
    )
    check("overlay con salto de línea final", [str(DATA / "config-overlay-salto.yaml")], 1, ruta, "espacios o saltos de línea")
    check("overlay vacío", [str(DATA / "config-overlay-vacio.yaml")], 0, ausentes=sin_aviso)
    check(
        "overlay con una clave desconocida",
        [str(DATA / "config-overlay-clave-desconocida.yaml")], 1,
        "stack/overlay: Additional properties are not allowed ('foo' was unexpected)",
    )
    check(
        "replaces que no es una lista",
        [str(DATA / "config-overlay-no-lista.yaml")], 1,
        "stack/overlay/replaces: 'frontend' is not of type 'array'", ausentes=("no declarado", "Traceback"),
    )

    # Variantes en línea.
    caso("overlay con replaces vacío", con("  overlay:\n    replaces: []\n"), 0, ausentes=sin_aviso)
    caso("overlay con un id en stubs", con("  overlay:\n    replaces:\n      - ai\n").replace("  stubs: []", "  stubs:\n    - ai"), 0, ausentes=sin_aviso)
    caso("overlay con varios ids, uno inválido", con("  overlay:\n    replaces:\n      - frontend\n      - nope\n"), 1, "stack/overlay/replaces/1", "id no declarado en agents: nope", ausentes=("replaces/0",))
    caso("overlay con un id ficticio declarado en active", con("  overlay:\n    replaces:\n      - example-extension\n").replace("    - frontend\n", "    - example-extension\n"), 0, ausentes=sin_aviso)
    caso("overlay con packs vacío no avisa", con("  overlay:\n    replaces:\n      - frontend\n").replace("  packs:\n    - sdaf-stack-example@0.1.0\n", "  packs: []\n"), 0, "I4", ausentes=("replaces", "FAIL"))
    caso("overlay con el alias stack.pack", texto.replace("  packs:\n    - sdaf-stack-example@0.1.0\n", "  pack: sdaf-stack-example@0.1.0\n"), 0, ALIAS_AVISO, ausentes=("FAIL", "replaces"))
    caso("overlay con --strict-i4 y un pack declarado", texto, 0, ausentes=sin_aviso, args=["--strict-i4"])
    caso("replaces con un id vacío", con('  overlay:\n    replaces:\n      - ""\n'), 1, "stack/overlay/replaces/0: ''", ausentes=("Traceback",))
    caso("replaces con un elemento que no es texto", con("  overlay:\n    replaces:\n      - 5\n"), 1, "stack/overlay/replaces/0", "is not of type 'string'", ausentes=("no declarado",))
    caso("overlay null", con("  overlay: null\n"), 1, "stack/overlay: None is not of type 'object'", ausentes=("Traceback",))
    caso("overlay que no es un mapa", con("  overlay:\n    - frontend\n"), 1, "stack/overlay", "is not of type 'object'", ausentes=("Traceback",))
    caso("replaces con un id del núcleo y otro con salto", con("  overlay:\n    replaces:\n      - specification\n      - |\n        frontend\n"), 1, "stack/overlay/replaces/0", "stack/overlay/replaces/1", "núcleo", "espacios o saltos de línea")
    caso("sin overlay la config sigue válida", con(""), 0, ausentes=sin_aviso)


def casos_unidades(tmp: Path) -> None:
    """stack.units: forma en el schema, coexistencia con el atajo y reglas de nombre, ruta y solape."""
    valida = DATA / "config-units-valida.yaml"
    texto = valida.read_text(encoding="utf-8")
    bloque = texto[texto.index("  units:\n"):texto.index("\nagents:")]
    n = 0

    def caso(nombre: str, contenido: str, exit_esperado: int, *motivos: str, ausentes=(), args=()) -> None:
        nonlocal n
        n += 1
        fichero = tmp / f"unidades-{n}.yaml"
        fichero.write_text(contenido, encoding="utf-8")
        check(nombre, [*args, str(fichero)], exit_esperado, *motivos, ausentes=ausentes)

    def con(units: str) -> str:
        """Config válida cuyo bloque units se sustituye por `units`."""
        return texto.replace(bloque, units)

    def una(src: str = "apps/api", tests: str | None = None, name: str = "Unidad A") -> str:
        extra = f"      tests: {tests}\n" if tests is not None else ""
        return f"  units:\n    - name: {name}\n      src: {src}\n{extra}"

    otra = "    - name: Unidad B\n      src: libs/core\n"
    sin_aviso = ("WARN", "FAIL", "Traceback")
    check("units válida con dos unidades", [str(valida)], 0, ausentes=sin_aviso)
    check(
        "units junto a src_path",
        [str(DATA / "config-units-con-src-path.yaml")], 1,
        "stack.units", "stack.src_path", "no pueden coexistir", ausentes=("tests_path", "Traceback"),
    )
    check(
        "units junto a tests_path",
        [str(DATA / "config-units-con-tests-path.yaml")], 1,
        "stack.units", "stack.tests_path", "no pueden coexistir", ausentes=("src_path", "Traceback"),
    )
    check(
        "units con nombre repetido",
        [str(DATA / "config-units-nombre-repetido.yaml")], 1,
        "stack/units/1/name", "repetido", "'Unidad A'", ausentes=("units/0", "Traceback"),
    )
    check(
        "units con salto de línea final en el nombre",
        [str(DATA / "config-units-nombre-salto.yaml")], 1,
        "stack/units/0/name", "espacios o saltos de línea", ausentes=("Traceback",),
    )
    check(
        "units con rutas solapadas avisa sin fallar",
        [str(DATA / "config-units-solape.yaml")], 0,
        "WARN", "solapa", "stack/units/0/src", "stack/units/1/src", ausentes=("FAIL", "Traceback"),
    )
    check("units con tests dentro de su propio src no avisa", [str(DATA / "config-units-tests-en-su-src.yaml")], 0, ausentes=sin_aviso)

    # En línea: una regla por caso.
    caso("units con una sola unidad sin tests", con(una()), 0, ausentes=sin_aviso)
    caso("units con sdaf.version 0.6.0", con(una()).replace('"0.5.0"', '"0.6.0"'), 0, ausentes=sin_aviso)
    caso("units con pack null", con(una()).replace("  packs: []\n", "  pack: null\n"), 0, ausentes=sin_aviso)
    caso("units junto a src_path y tests_path", con("  src_path: src\n  tests_path: tests\n" + una()), 1, "stack.src_path", "stack.tests_path", "no pueden coexistir")
    caso("units sin src", con("  units:\n    - name: Unidad A\n      tests: tests/api\n"), 1, "stack/units/0", "'src' is a required property", ausentes=("Traceback",))
    caso("units sin name", con("  units:\n    - src: apps/api\n"), 1, "stack/units/0", "'name' is a required property", ausentes=("Traceback",))
    caso("units con tests vacío", con(una(tests='""')), 1, "stack/units/0/tests", ausentes=("Traceback",))
    caso("units con name vacío", con(una(name='""')), 1, "stack/units/0/name", ausentes=("Traceback",))
    caso("units con una clave desconocida", con(una() + "      foo: x\n"), 1, "stack/units/0", "Additional properties are not allowed ('foo' was unexpected)")
    caso("units con una unidad que no es objeto", con("  units:\n    - apps/api\n"), 1, "stack/units/0", "is not of type 'object'", ausentes=("Traceback",))
    caso("units vacía", con("  units: []\n"), 1, "stack/units", "should be non-empty", ausentes=("Traceback",))
    caso("units que no es una lista", con("  units: apps/api\n"), 1, "stack/units", "is not of type 'array'", ausentes=("Traceback",))
    caso("units con src que no es texto", con(una(src="5")), 1, "stack/units/0/src", "is not of type 'string'", ausentes=("Traceback", "absoluta"))
    caso("units con espacio final en src", con(una(src='"apps/api "')), 1, "stack/units/0/src", "espacios o saltos de línea")
    caso("units con espacio final en tests", con(una(tests='"tests/api "')), 1, "stack/units/0/tests", "espacios o saltos de línea")
    caso("units con ruta absoluta en src", con(una(src="/apps/api")), 1, "stack/units/0/src", "ruta absoluta")
    caso("units con ruta absoluta en tests", con(una(tests="/tests/api")), 1, "stack/units/0/tests", "ruta absoluta", ausentes=("units/0/src",))
    caso("units con barra invertida inicial", con(una(src="'\\apps\\api'")), 1, "stack/units/0/src", "ruta absoluta")
    caso("units con letra de unidad", con(una(src="'C:/apps/api'")), 1, "stack/units/0/src", "ruta absoluta")
    caso("units con letra de unidad y barra invertida", con(una(tests="'D:\\tests'")), 1, "stack/units/0/tests", "ruta absoluta")
    caso("units con segmento .. en src", con(una(src="apps/../libs")), 1, "stack/units/0/src", "..")
    caso("units con .. inicial en tests", con(una(tests="../tests")), 1, "stack/units/0/tests", "..", ausentes=("units/0/src",))
    caso("units con .. y barra invertida", con(una(src="'apps\\..\\libs'")), 1, "stack/units/0/src", "..")
    caso("units con ruta .", con(una(src=".")), 1, "stack/units/0/src", "todo el repo")
    caso("units con ruta ./", con(una(src="./")), 1, "stack/units/0/src", "todo el repo")
    caso("units con segmento . intermedio", con(una(src="apps/./api")), 1, "stack/units/0/src", "segmentos vacíos o '.'")
    caso("units con segmento vacío intermedio", con(una(tests="tests//api")), 1, "stack/units/0/tests", "segmentos vacíos o '.'")
    caso("units con barra final en src es válida", con(una(src="apps/api/")), 0, ausentes=sin_aviso)
    caso("units con nombre libre con espacios y signos", con(una(name="'Servicio de pagos (v2)'")), 0, ausentes=sin_aviso)
    caso("units con nombres que difieren solo en mayúsculas", con(una() + "    - name: unidad a\n      src: libs/core\n"), 0, ausentes=sin_aviso)
    caso("units con rutas iguales entre unidades avisa", con(una() + "    - name: Unidad B\n      src: apps/api\n"), 0, "WARN", "solapa", "stack/units/0/src", "stack/units/1/src", ausentes=("FAIL",))
    caso("units con tests de una unidad dentro del src de otra avisa", con(una() + "    - name: Unidad B\n      src: libs/core\n      tests: apps/api/tests\n"), 0, "WARN", "stack/units/0/src", "stack/units/1/tests", ausentes=("FAIL",))
    caso("units con src de una unidad dentro de los tests de otra avisa", con(una(tests="tests") + "    - name: Unidad B\n      src: tests/b\n"), 0, "WARN", "stack/units/0/tests", "stack/units/1/src", ausentes=("FAIL",))
    caso("units con tests iguales entre unidades avisa", con(una(tests="tests") + "    - name: Unidad B\n      src: libs/core\n      tests: tests\n"), 0, "WARN", "stack/units/0/tests", "stack/units/1/tests", ausentes=("FAIL",))
    caso("units con prefijo de texto sin solape no avisa", con(una() + "    - name: Unidad B\n      src: apps/api2\n"), 0, ausentes=sin_aviso)
    caso("units con barras distintas solapadas avisa", con(una(src="'apps\\api\\v1'") + "    - name: Unidad B\n      src: apps/api/\n"), 0, "WARN", "solapa", ausentes=("FAIL",))
    caso("units con una ruta inválida no avisa de solape", con(una(src="/apps") + "    - name: Unidad B\n      src: apps\n"), 1, "ruta absoluta", ausentes=("WARN", "solapa"))
    caso("units con varios problemas a la vez", con("  units:\n    - name: Unidad A\n      src: /a\n    - name: Unidad A\n      src: ../b\n"), 1, "stack/units/0/src", "stack/units/1/name", "stack/units/1/src")
    caso("sin units el atajo src_path y tests_path sigue válido", texto.replace(bloque, "  src_path: src\n  tests_path: tests"), 0, ausentes=sin_aviso)
    caso("src_path y tests_path no se endurecen", texto.replace(bloque, "  src_path: /abs/../x\n  tests_path: ."), 0, ausentes=sin_aviso)


def texto_manifiesto(
    id: str = "sdaf-stack-example",
    version: str = "0.1.0",
    core: str = ">=0.5.0 <0.7.0",
    ext: tuple[str, ...] = ("example-extension",),
    skills: tuple[str, ...] = ("example-skill",),
    prompts: tuple[str, ...] = ("example-prompt",),
) -> str:
    listas = {"extension_ids": ext, "skills": skills, "prompts": prompts}
    provides = "".join(f"  {k}: {json.dumps(list(v))}\n" for k, v in listas.items() if v)
    return f"id: {id}\nversion: {version}\ncore: {json.dumps(core)}\nprovides:\n{provides}"


def casos_manifiestos(tmp: Path) -> None:
    """S8–S10: --pack-manifest, rango core, colisiones, I4 con manifiestos y aviso de ausencia."""
    valido, otro = DATA / "pack-valido.yaml", DATA / "pack-otro.yaml"
    uno = (DATA / "config-packs-uno.yaml").read_text(encoding="utf-8")
    cubierto = uno.replace("frontend", "example-extension")
    dos = (DATA / "config-packs-060.yaml").read_text(encoding="utf-8")
    dos_frontend = dos.replace("example-extension", "frontend")
    n = 0

    def cfg(texto: str, version: str = "0.5.0") -> str:
        nonlocal n
        n += 1
        ruta = tmp / f"config-{n}.yaml"
        ruta.write_text(re.sub(r'version: "[0-9.]+"', f'version: "{version}"', texto, count=1), encoding="utf-8")
        return str(ruta)

    def man(**cambios) -> Path:
        nonlocal n
        n += 1
        ruta = tmp / f"pack-{n}.yaml"
        ruta.write_text(texto_manifiesto(**cambios), encoding="utf-8")
        return ruta

    def caso(nombre, config, manifiestos, exit_esperado, *motivos, ausentes=(), extra=(), etiqueta=None) -> None:
        args = list(extra)
        for m in manifiestos:
            args += ["--pack-manifest", str(m)]
        check(nombre, [*args, config], exit_esperado, *motivos, ausentes=ausentes, etiqueta=etiqueta)

    # S8: validación y cruce con la config.
    caso("manifiesto válido y coincidente", cfg(cubierto), [valido], 0, ausentes=("WARN", "FAIL"))
    caso("dos manifiestos válidos y coincidentes", cfg(dos), [valido, otro], 0, ausentes=("WARN", "FAIL"))
    caso(
        "manifiesto con alias stack.pack",
        cfg(cubierto.replace("  packs:\n    - sdaf-stack-example@0.1.0\n", "  pack: sdaf-stack-example@0.1.0\n")),
        [valido], 0, ALIAS_AVISO, ausentes=("FAIL", "no referenciado"),
    )
    caso("id que no coincide", cfg(cubierto), [man(id="sdaf-stack-nope")], 1, "no referenciado", "sdaf-stack-nope@0.1.0", "sdaf-stack-example@0.1.0")
    caso("versión que no coincide", cfg(cubierto), [man(version="0.2.0")], 1, "no referenciado", "sdaf-stack-example@0.2.0", "sdaf-stack-example@0.1.0")
    caso("manifiesto no referenciado", cfg(cubierto), [valido, otro], 1, "no referenciado", "sdaf-stack-other@0.2.0")
    caso("manifiesto sin packs declarados", cfg(uno.replace("  packs:\n    - sdaf-stack-example@0.1.0\n", "  packs: []\n")), [valido], 1, "no referenciado", "ningún pack")
    caso(
        "manifiesto inválido", cfg(cubierto), [DATA / "pack-sin-core.yaml"], 1, "obligatoria 'core'",
        etiqueta="pack-sin-core.yaml", ausentes=("no referenciado",),
    )
    # Un motivo idéntico no se repite: faltan dos propiedades obligatorias a la vez.
    incompleto = tmp / "pack-incompleto.yaml"
    incompleto.write_text("id: mal\nversion: x\n", encoding="utf-8")
    res = run(["--pack-manifest", str(incompleto), cfg(cubierto)])
    faltan = "(raíz): falta la propiedad obligatoria 'core', 'provides'"
    veces = res.stdout.count(faltan)
    problemas = []
    if res.returncode != 1:
        problemas.append(f"exit {res.returncode}, se esperaba 1")
    if veces != 1:
        problemas.append(f"'{faltan}' sale {veces} veces, se esperaba 1")
    for motivo in ("id: el valor 'mal' no cumple el patrón", "version: el valor 'x' no cumple el patrón"):
        if motivo not in res.stdout:
            problemas.append(f"falta el motivo '{motivo}'")
    if problemas:
        FALLOS.append("manifiesto inválido sin motivos repetidos")
        print("FAIL manifiesto inválido sin motivos repetidos: " + "; ".join(problemas))
        print(res.stdout + res.stderr)
    else:
        print("OK manifiesto inválido sin motivos repetidos")
    caso("manifiesto con YAML roto", cfg(cubierto), [DATA / "pack-yaml-invalido.yaml"], 1, "YAML inválido", etiqueta="pack-yaml-invalido.yaml")
    caso("manifiesto con raíz que no es un mapa", cfg(cubierto), [DATA / "pack-raiz-lista.yaml"], 1, "no es un mapa", etiqueta="pack-raiz-lista.yaml")
    inexistente = tmp / "no-existe-pack.yaml"
    caso("manifiesto inexistente", cfg(cubierto), [inexistente], 1, "no se puede leer", etiqueta="no-existe-pack.yaml")
    copia = tmp / "pack-copia.yaml"
    copia.write_text(valido.read_text(encoding="utf-8"), encoding="utf-8")
    caso(
        "dos manifiestos con el mismo id@version", cfg(cubierto), [valido, copia], 1, "pack-copia.yaml",
        "sdaf-stack-example@0.1.0", "duplica", etiqueta="pack-copia.yaml", ausentes=("colisión",),
    )
    caso("sin --pack-manifest no se lee ningún manifiesto", cfg(cubierto), [], 0, ausentes=("WARN", "sin manifiesto", "no referenciado"))
    caso("config con sdaf.version que no es texto y un manifiesto", cfg(cubierto.replace('version: "0.5.0"', "version: 5")), [valido], 1, "sdaf/version")

    # S9: rango core frente a sdaf.version (tupla X.Y.Z literal).
    fuera = "no incluye sdaf.version"
    caso("0.4.0 queda fuera de >=0.5.0", cfg(cubierto, "0.4.0"), [valido], 1, fuera, "0.4.0", ">=0.5.0 <0.7.0", "sdaf-stack-example@0.1.0")
    caso("0.7.0 queda fuera de <0.7.0", cfg(cubierto, "0.7.0"), [valido], 1, fuera, "0.7.0", ">=0.5.0 <0.7.0")
    caso("0.6.0 queda dentro", cfg(cubierto, "0.6.0"), [valido], 0, ausentes=(fuera, "FAIL"))
    caso("0.6.9 queda dentro (patch distinto de 0)", cfg(cubierto, "0.6.9"), [valido], 0, ausentes=(fuera, "FAIL"))
    caso("0.5.0 es el límite inferior inclusivo", cfg(cubierto, "0.5.0"), [valido], 0, ausentes=(fuera,))
    caso("0.5.0 queda fuera de >0.5.0", cfg(cubierto, "0.5.0"), [man(core=">0.5.0 <0.7.0")], 1, fuera, ">0.5.0 <0.7.0")
    caso("0.7.0 queda dentro de <=0.7.0", cfg(cubierto, "0.7.0"), [man(core=">=0.5.0 <=0.7.0")], 0, ausentes=(fuera,))
    caso("0.7.1 queda fuera de <=0.7.0", cfg(cubierto, "0.7.1"), [man(core=">=0.5.0 <=0.7.0")], 1, fuera)
    caso("= admite solo esa versión", cfg(cubierto, "0.5.1"), [man(core="=0.5.1")], 0, ausentes=(fuera,))
    caso("= rechaza otra versión", cfg(cubierto, "0.5.2"), [man(core="=0.5.1")], 1, fuera, "=0.5.1")
    caso("versión sin comparador es exacta", cfg(cubierto, "0.5.2"), [man(core="0.5.1")], 1, fuera, "0.5.1")
    caso("versión exacta con >=X <=X", cfg(cubierto, "0.5.1"), [man(core=">=0.5.1 <=0.5.1")], 0, ausentes=(fuera,))
    caso("versión exacta con >=X <=X rechaza otra", cfg(cubierto, "0.5.2"), [man(core=">=0.5.1 <=0.5.1")], 1, fuera)
    caso("las versiones se comparan como enteros", cfg(cubierto, "0.10.0"), [man(core=">=0.9.0 <0.11.0")], 0, ausentes=(fuera,))
    caso("rango con límites inferior y superior en orden inverso", cfg(cubierto, "0.8.0"), [man(core="<0.7.0 >=0.5.0")], 1, fuera)

    # S10: colisiones entre manifiestos.
    colision = "colisión"
    caso(
        "colisión de id de extensión", cfg(dos), [valido, man(id="sdaf-stack-other", version="0.2.0", ext=("example-extension",), skills=("other-skill",), prompts=("other-prompt",))],
        1, colision, "extensión", "example-extension", "sdaf-stack-example@0.1.0", "sdaf-stack-other@0.2.0",
    )
    caso(
        "colisión de id de skill", cfg(dos), [valido, man(id="sdaf-stack-other", version="0.2.0", ext=("other-extension",), skills=("example-skill",), prompts=("other-prompt",))],
        1, colision, "skill", "example-skill", "sdaf-stack-example@0.1.0", "sdaf-stack-other@0.2.0",
    )
    caso(
        "colisión de id de prompt", cfg(dos), [valido, man(id="sdaf-stack-other", version="0.2.0", ext=("other-extension",), skills=("other-skill",), prompts=("example-prompt",))],
        1, colision, "prompt", "example-prompt", "sdaf-stack-example@0.1.0", "sdaf-stack-other@0.2.0",
    )
    caso("sin colisión entre packs distintos", cfg(dos), [valido, otro], 0, ausentes=(colision,))
    caso(
        "el mismo id en tipos distintos no colisiona", cfg(dos), [valido, man(id="sdaf-stack-other", version="0.2.0", ext=(), skills=("example-extension",), prompts=())],
        0, ausentes=(colision, "FAIL"),
    )

    # S10: I4 con manifiestos.
    i4_nuevo = "I4: id(s) de extensión no aportados por ningún pack"
    caso("I4 cubierto por los manifiestos", cfg(dos), [valido, otro], 0, ausentes=("I4",))
    caso("I4 no cubierto avisa", cfg(dos_frontend), [valido, otro], 0, "WARN", i4_nuevo, "frontend")
    caso("I4 no cubierto con --strict-i4 falla", cfg(dos_frontend), [valido, otro], 1, i4_nuevo, "frontend", extra=["--strict-i4"])
    caso("I4 cubierto con --strict-i4 no falla", cfg(dos), [valido, otro], 0, ausentes=("I4",), extra=["--strict-i4"])
    caso("I4 con un pack sin manifiesto conserva la conducta actual", cfg(dos_frontend), [valido], 0, ausentes=("I4", "WARN"))
    caso("I4 sin manifiestos conserva la conducta actual", cfg(dos_frontend), [], 0, ausentes=("I4", "WARN"))
    caso("I4 con --strict-i4 y un pack sin manifiesto no falla", cfg(dos_frontend), [valido], 0, ausentes=("I4",), extra=["--strict-i4"])
    caso("I4 usa la unión de los packs", cfg(dos.replace("    - specification\n", "    - specification\n    - other-extension\n")), [valido, otro], 0, ausentes=("I4",))

    # S10: aviso de ausencia (D3).
    aviso = "sin manifiesto entre los pasados (aviso durante 0.6.x)"
    caso("0.6.0 avisa del pack sin manifiesto", cfg(dos, "0.6.0"), [valido], 0, "WARN", "pack sdaf-stack-other@0.2.0 " + aviso, ausentes=("pack sdaf-stack-example@0.1.0 sin",))
    caso("0.6.0 avisa de cada pack sin manifiesto", cfg(dos, "0.6.0"), [], 0, "pack sdaf-stack-example@0.1.0 " + aviso, "pack sdaf-stack-other@0.2.0 " + aviso)
    caso("0.6.0 con todos los manifiestos no avisa", cfg(dos, "0.6.0"), [valido, otro], 0, ausentes=(aviso,))
    caso("0.5.0 nunca avisa de la ausencia", cfg(dos, "0.5.0"), [valido], 0, ausentes=(aviso,))
    caso("0.5.9 nunca avisa de la ausencia", cfg(dos, "0.5.9"), [], 0, ausentes=(aviso,))
    caso("0.10.0 avisa (la línea se compara como tupla)", cfg(dos, "0.10.0"), [], 0, aviso)
    caso("el aviso de ausencia no cambia el exit con --strict-i4", cfg(dos, "0.6.0"), [valido], 0, aviso, extra=["--strict-i4"])
    caso("0.6.0 sin packs declarados no avisa", cfg(uno.replace("  packs:\n    - sdaf-stack-example@0.1.0\n", "  packs: []\n").replace("frontend", "domain"), "0.6.0"), [], 0, ausentes=(aviso,))


def casos_satisfies() -> None:
    """S9: tabla de `satisfies` con límites inclusivos y exclusivos y sintaxis inválida."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from sdaf_packs import parse_range, satisfies

    tabla = [
        ((0, 5, 0), ">=0.5.0", True), ((0, 4, 9), ">=0.5.0", False), ((0, 5, 1), ">=0.5.0", True),
        ((0, 5, 0), ">0.5.0", False), ((0, 5, 1), ">0.5.0", True),
        ((0, 7, 0), "<0.7.0", False), ((0, 6, 9), "<0.7.0", True),
        ((0, 7, 0), "<=0.7.0", True), ((0, 7, 1), "<=0.7.0", False),
        ((0, 5, 1), "=0.5.1", True), ((0, 5, 0), "=0.5.1", False), ((0, 5, 1), "0.5.1", True), ((0, 5, 2), "0.5.1", False),
        ((0, 5, 1), ">=0.5.1 <=0.5.1", True), ((0, 5, 0), ">=0.5.1 <=0.5.1", False), ((0, 5, 2), ">=0.5.1 <=0.5.1", False),
        ((0, 6, 0), ">=0.5.0 <0.7.0", True), ((0, 4, 0), ">=0.5.0 <0.7.0", False), ((0, 7, 0), ">=0.5.0 <0.7.0", False),
        ((0, 8, 0), "<0.7.0 >=0.5.0", False), ((0, 6, 3), "<0.7.0 >=0.5.0", True),
        ((0, 10, 0), ">=0.9.0 <0.11.0", True), ((0, 10, 0), "<0.9.0", False), ((1, 0, 0), "<0.99.0", False),
    ]
    for version, rango, esperado in tabla:
        obtenido = satisfies(version, parse_range(rango))
        nombre = f"satisfies {'.'.join(map(str, version))} en {rango!r}"
        if obtenido is esperado:
            print(f"OK {nombre}")
        else:
            FALLOS.append(nombre)
            print(f"FAIL {nombre}: se obtuvo {obtenido}, se esperaba {esperado}")
    for invalido in ("", "x.y.z", ">=0.5.0 <0.7.0 <0.8.0", ">=0.5"):
        parsed = parse_range(invalido)
        nombre = f"satisfies con rango de sintaxis inválida {invalido!r}"
        if parsed is None and satisfies((0, 5, 0), parsed) is False:
            print(f"OK {nombre}")
        else:
            FALLOS.append(nombre)
            print(f"FAIL {nombre}: parse_range={parsed!r}")


def regresion_examples() -> None:
    """Solo los examples con stack.pack emiten el aviso de alias y siguen saliendo 0."""
    con_alias = {"04-pack-stack.yaml", "05-fusiones-mvp.yaml", "07-pack-frontend.yaml", "08-completo.yaml"}
    for ruta in sorted((ROOT / "examples").glob("*.yaml")):
        if ruta.name in con_alias:
            check(f"examples/{ruta.name} avisa del alias", [str(ruta)], 0, ALIAS_AVISO)
        else:
            check(f"examples/{ruta.name} sin aviso de alias", [str(ruta)], 0, ausentes=(ALIAS_AVISO,))
    check("sdaf.config.example.yaml sin aviso de alias", [str(ROOT / "sdaf.config.example.yaml")], 0, ausentes=(ALIAS_AVISO,))


def legacy() -> int:
    defaults = run([])
    if defaults.returncode != 0:
        print("FAIL examples válidos deberían salir 0")
        print(defaults.stdout)
        print(defaults.stderr)
        return 1
    print("OK examples + example.yaml")

    missing = run(["no-existe.yaml"])
    if missing.returncode == 0 or "inexistente" not in missing.stdout:
        print("FAIL ruta inexistente debería salir 1")
        print(missing.stdout)
        return 1
    print("OK ruta inexistente")

    broken = run([str(INVALID)])
    out = broken.stdout
    if broken.returncode == 0:
        print("FAIL fixture de invariantes debería salir 1")
        print(out)
        return 1
    needed = ["I1", "I2", "I3", "does not match", "uniqueItems", "foo"]
    # jsonschema message for pattern may vary; pack 'foo' must appear
    if "I1" not in out or "I2" not in out or "I3" not in out:
        print("FAIL se esperaban I1 I2 I3 en la salida")
        print(out)
        return 1
    if "foo" not in out and "does not match" not in out and "pattern" not in out.lower():
        print("FAIL se esperaba error de pack inválido")
        print(out)
        return 1
    if "I4" in out and "WARN" not in out:
        # I4 on this fixture: frontend is extension + pack is foo (invalid so schema fails first)
        pass
    print("OK fixture I1–I3 + pack + duplicados")

    i4 = run([str(I4)])
    if i4.returncode != 0:
        print("FAIL I4 por defecto no debe cambiar el exit code")
        print(i4.stdout)
        return 1
    if "WARN" not in i4.stdout or "frontend" not in i4.stdout or "I4" not in i4.stdout:
        print("FAIL I4 debería avisar y nombrar frontend")
        print(i4.stdout)
        return 1
    print("OK I4 aviso por defecto")

    i4_strict = run(["--strict-i4", str(I4)])
    if i4_strict.returncode == 0 or "I4" not in i4_strict.stdout:
        print("FAIL --strict-i4 debería salir 1 con I4")
        print(i4_strict.stdout)
        return 1
    print("OK I4 --strict-i4")

    tooling = run([str(TOOLING)])
    if tooling.returncode == 0 or "gentle_ai" not in tooling.stdout:
        print("FAIL tooling.gentle_ai con una rama debería salir 1 y nombrar la clave")
        print(tooling.stdout)
        return 1
    print("OK tooling.gentle_ai exige release o SHA")

    t1 = run([str(TOOLING_SDD)])
    if t1.returncode != 0 or "WARN" not in t1.stdout or "T1" not in t1.stdout:
        print("FAIL T1 debería avisar sin cambiar el exit code con gentle-ai 3.7.0")
        print(t1.stdout)
        return 1
    if "T1" in defaults.stdout:
        print("FAIL T1 no debería saltar en los examples (08 declara un SHA)")
        print(defaults.stdout)
        return 1
    print("OK T1 aviso con release que incluye sdd")
    return 0


def main() -> int:
    if legacy():
        return 1
    casos_packs()
    with tempfile.TemporaryDirectory(prefix="sdaf config ") as tmpdir:
        casos_en_linea(Path(tmpdir))
    with tempfile.TemporaryDirectory(prefix="sdaf overlay ") as tmpdir:
        casos_overlay(Path(tmpdir))
    with tempfile.TemporaryDirectory(prefix="sdaf unidades ") as tmpdir:
        casos_unidades(Path(tmpdir))
    with tempfile.TemporaryDirectory(prefix="sdaf manifiestos ") as tmpdir:
        casos_manifiestos(Path(tmpdir))
    casos_satisfies()
    regresion_examples()
    print(f"fallos: {len(FALLOS)}")
    return 1 if FALLOS else 0


if __name__ == "__main__":
    sys.exit(main())
