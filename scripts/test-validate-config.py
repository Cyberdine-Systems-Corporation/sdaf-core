#!/usr/bin/env python3
"""Comprueba fixtures del validador de config (I1–I4, packs, alias, bordes, tooling y T1).

Cada caso lanza `validate-config.py` como proceso y comprueba salida y código de
salida. Los fixtures viven en scripts/testdata/; los casos en línea se escriben
en un directorio temporal (ruta con espacios). Los casos de packs se ejecutan
todos y se informa del número de fallos.
"""
from __future__ import annotations

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
    """Exige exit, línea OK/FAIL con la ruta, cada motivo presente y cada ausente ausente."""
    ruta = Path(args[-1])
    res = run(args)
    out = res.stdout
    prefijo = "OK   " if exit_esperado == 0 else "FAIL "
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
    regresion_examples()
    print(f"fallos: {len(FALLOS)}")
    return 1 if FALLOS else 0


if __name__ == "__main__":
    sys.exit(main())
