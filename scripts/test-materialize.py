#!/usr/bin/env python3
"""Comprueba la materialización del core y de los packs con fixtures.

Cada caso lanza `materialize.py` como proceso (o, para simular un fallo del
sistema, lo importa y parchea `make_symlink`) y comprueba la salida, el código de
salida y el árbol en disco. Los entornos se crean en un directorio temporal (ruta con
espacios) a partir de scripts/testdata/materialize: un consumidor con overlay y
config, un core simulado y dos packs. Ante cualquier FAIL se exige que el árbol
quede idéntico (nada escrito). Se ejecutan todos los casos y se informa del número
de fallos; los casos que dependen de enlaces simbólicos se marcan SKIP si el
sistema no los permite.
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "materialize.py"
FIXTURES = ROOT / "scripts" / "testdata" / "materialize"
REGISTRO = ".sdaf-origin"
FALLOS: list[str] = []
SALTADOS: list[str] = []

CORE = [
    "agents/specification-agent.md",
    "agents/architecture-agent.md",
    "prompts/agents/specification-agent.md",
    "skills/core-skill",
]
EXAMPLE = [
    "agents/example-extension-agent.md",
    "prompts/agents/example-extension-agent.md",
    "skills/example-skill",
]
OTRO = [
    "agents/other-extension-agent.md",
    "prompts/agents/other-extension-agent.md",
    "skills/other-skill",
]
TODOS = CORE + EXAMPLE + OTRO


# --- utilidades -------------------------------------------------------------------


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=cwd,
        env={**os.environ, "PYTHONUTF8": "1"},
    )


def caso(nombre: str, problemas: list[str], salida: str = "") -> None:
    if problemas:
        FALLOS.append(nombre)
        print(f"FAIL {nombre}: " + "; ".join(problemas))
        if salida:
            print(salida)
    else:
        print(f"OK {nombre}")


def saltar(nombre: str, motivo: str) -> None:
    SALTADOS.append(nombre)
    print(f"SKIP {nombre}: {motivo}")


def leer(ruta: Path) -> str | None:
    return ruta.read_text(encoding="utf-8") if ruta.is_file() else None


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_dir(path: Path) -> str:
    """Hash esperado de una skill: ruta relativa y hash de cada fichero, ordenados."""
    digest = hashlib.sha256()
    ficheros = sorted(f.relative_to(path).as_posix() for f in path.rglob("*") if f.is_file())
    for rel in ficheros:
        digest.update(rel.encode("utf-8") + b"\0" + sha(path / rel).encode() + b"\n")
    return digest.hexdigest()


def instantanea(raiz: Path) -> dict:
    """Estado del árbol sin seguir enlaces: ficheros por hash, enlaces por destino."""
    estado: dict[str, tuple] = {}
    for dirpath, dirs, files in os.walk(raiz, followlinks=False):
        for nombre in dirs + files:
            ruta = Path(dirpath) / nombre
            rel = ruta.relative_to(raiz).as_posix()
            if ruta.is_symlink():
                estado[rel] = ("enlace", os.readlink(ruta))
            elif ruta.is_dir():
                estado[rel] = ("dir",)
            else:
                estado[rel] = ("fichero", sha(ruta))
    return estado


def puede_enlazar(tmp: Path) -> bool:
    sonda = Path(tempfile.mkdtemp(dir=tmp, prefix="sonda "))
    try:
        (sonda / "t.txt").write_text("x", encoding="utf-8")
        os.symlink("t.txt", sonda / "l.txt")
        return (sonda / "l.txt").is_symlink()
    except (OSError, NotImplementedError):
        return False


class Entorno:
    """Consumidor con .sdaf (core) y dos packs fuera de él, en un directorio nuevo."""

    contador = 0

    def __init__(self, tmp: Path) -> None:
        Entorno.contador += 1
        self.base = tmp / f"entorno {Entorno.contador}"
        self.consumer = self.base / "consumer"
        shutil.copytree(FIXTURES / "consumer", self.consumer)
        shutil.copytree(FIXTURES / "core", self.consumer / ".sdaf")
        self.example = self.base / "packs" / "example"
        self.otro = self.base / "packs" / "otro"
        shutil.copytree(FIXTURES / "packs" / "example", self.example)
        shutil.copytree(FIXTURES / "packs" / "otro", self.otro)

    def args(self, *extra: str, packs: list[Path] | None = None) -> list[str]:
        rutas = [self.example, self.otro] if packs is None else packs
        pack_args = [x for p in rutas for x in ("--pack", str(p))]
        return ["--consumer-root", str(self.consumer), *pack_args, *extra]

    def escribir(self, rel: str, texto: str) -> None:
        ruta = self.consumer / rel
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(texto, encoding="utf-8")

    def config_replaces(self, *ids: str) -> None:
        lista = "".join(f"      - {i}\n" for i in ids)
        self.escribir(
            "sdaf.config.yaml",
            'sdaf:\n  version: "0.5.0"\nstack:\n  packs:\n    - sdaf-stack-example@0.1.0\n'
            f"  overlay:\n    replaces:\n{lista}",
        )

    def registro(self) -> dict:
        if not (self.consumer / REGISTRO).is_file():
            return {"entries": []}
        return json.loads((self.consumer / REGISTRO).read_text(encoding="utf-8"))

    def bytes_registro(self) -> bytes:
        ruta = self.consumer / REGISTRO
        return ruta.read_bytes() if ruta.is_file() else b""

    def entradas(self) -> dict[str, dict]:
        return {e["dest"]: e for e in self.registro()["entries"]}


def check(
    nombre: str,
    res: subprocess.CompletedProcess[str],
    exit_esperado: int,
    *motivos: str,
    ausentes: tuple[str, ...] = (),
    extra: list[str] | None = None,
) -> None:
    """Exige código de salida, motivos en la salida, ausentes y que no haya traceback."""
    salida = res.stdout + res.stderr
    problemas = list(extra or [])
    if res.returncode != exit_esperado:
        problemas.append(f"exit {res.returncode}, se esperaba {exit_esperado}")
    if exit_esperado == 1 and "FAIL" not in res.stdout:
        problemas.append("falta una línea FAIL")
    if "Traceback" in salida:
        problemas.append("traceback en la salida")
    for motivo in motivos:
        if motivo not in salida:
            problemas.append(f"falta '{motivo}'")
    for ausente in ausentes:
        if ausente in salida:
            problemas.append(f"no debía aparecer '{ausente}'")
    caso(nombre, problemas, salida)


def check_fail_sin_escribir(nombre: str, env: Entorno, args: list[str], *motivos: str) -> None:
    """Exit 1 con los motivos dados y el árbol del consumidor y de los packs sin cambios."""
    antes = instantanea(env.base)
    res = run(args)
    despues = instantanea(env.base)
    extra = [] if antes == despues else ["se escribió algo pese al FAIL"]
    check(nombre, res, 1, *motivos, extra=extra)


def cargar_modulo():
    """Importa materialize.py (con sus dependencias) para parchear make_symlink."""
    sys.path.insert(0, str(SCRIPT.parent))
    spec = importlib.util.spec_from_file_location("materialize_bajo_test", SCRIPT)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def en_proceso(modulo, args: list[str]) -> tuple[int, str]:
    salida = io.StringIO()
    with contextlib.redirect_stdout(salida):
        codigo = modulo.main(args)
    return codigo, salida.getvalue()


# --- casos ------------------------------------------------------------------------


def casos_copia(tmp: Path) -> None:
    """S1, S4, S5: copia de core + dos packs con registro de origen y hashes."""
    env = Entorno(tmp)
    res = run(env.args("--mode", "copy"))
    check("copia: materializa core y dos packs", res, 0, "OK", ausentes=("FAIL", "WARN"))
    problemas = []
    fuentes = {
        **{d: env.consumer / ".sdaf" / d for d in CORE},
        **{d: env.example / d for d in EXAMPLE},
        **{d: env.otro / d for d in OTRO},
    }
    for dest, origen in fuentes.items():
        ruta = env.consumer / dest
        if ruta.is_symlink():
            problemas.append(f"{dest} es un enlace")
        elif origen.is_dir():
            if not (ruta / "SKILL.md").is_file() or hash_dir(ruta) != hash_dir(origen):
                problemas.append(f"{dest}: contenido distinto")
        elif not ruta.is_file() or ruta.read_bytes() != origen.read_bytes():
            problemas.append(f"{dest}: contenido distinto")
    if not (env.consumer / "skills/core-skill/references/notas.md").is_file():
        problemas.append("la skill del core no se copió entera")
    for no_aporte in ("agents/README.md", "skills/README.md"):
        if (env.consumer / no_aporte).exists():
            problemas.append(f"{no_aporte} no es un aporte y se materializó")
    for overlay in ("agents/local-agent.md", "skills/local-skill/SKILL.md"):
        if not (env.consumer / overlay).is_file():
            problemas.append(f"{overlay} del overlay desapareció")
    caso("copia: ficheros y overlay en disco", problemas)

    problemas = []
    texto = env.bytes_registro()
    if b"\r" in texto or not texto.endswith(b"\n"):
        problemas.append("el registro no usa LF o no termina en salto de línea")
    try:
        texto.decode("utf-8")
    except UnicodeDecodeError:
        problemas.append("el registro no es UTF-8")
    entradas = env.entradas()
    if not entradas:
        problemas.append("no existe el registro")
    if entradas and sorted(entradas) != sorted(TODOS):
        problemas.append(f"destinos del registro: {sorted(entradas)}")
    if [e["dest"] for e in env.registro()["entries"]] != sorted(entradas):
        problemas.append("las entradas no están ordenadas por destino")
    capas = {
        **{d: "core" for d in CORE},
        **{d: "pack:sdaf-stack-example" for d in EXAMPLE},
        **{d: "pack:sdaf-stack-other" for d in OTRO},
    }
    for dest, entrada in entradas.items():
        origen = Path(os.path.abspath(env.consumer / entrada["origin"]))
        esperado = hash_dir(origen) if origen.is_dir() else sha(origen)
        if entrada["layer"] != capas[dest]:
            problemas.append(f"{dest}: capa {entrada['layer']}")
        if entrada["type"] != "copy":
            problemas.append(f"{dest}: tipo {entrada['type']}")
        if entrada["sha256"] != esperado or esperado != (hash_dir(env.consumer / dest) if origen.is_dir() else sha(env.consumer / dest)):
            problemas.append(f"{dest}: sha256 no coincide")
    if entradas.get("agents/specification-agent.md", {}).get("origin") != ".sdaf/agents/specification-agent.md":
        problemas.append("origen relativo del core incorrecto")
    if entradas.get("skills/example-skill", {}).get("origin") != "../packs/example/skills/example-skill":
        problemas.append("origen relativo del pack incorrecto")
    caso("copia: registro .sdaf-origin con capa, origen, tipo y hash", problemas)


def casos_symlink(tmp: Path) -> None:
    """S8: enlaces simbólicos relativos; sin soporte del SO el caso se salta."""
    if not puede_enlazar(tmp):
        saltar("symlink: enlaces relativos", "el sistema no permite enlaces simbólicos")
        saltar("symlink: ancestro enlazado", "el sistema no permite enlaces simbólicos")
        saltar("symlink: idempotente", "el sistema no permite enlaces simbólicos")
        return
    env = Entorno(tmp)
    res = run(env.args("--mode", "symlink"))
    check("symlink: materializa", res, 0, ausentes=("FAIL", "WARN"))
    problemas = []
    fuentes = {
        **{d: env.consumer / ".sdaf" / d for d in CORE},
        **{d: env.example / d for d in EXAMPLE},
        **{d: env.otro / d for d in OTRO},
    }
    for dest, origen in fuentes.items():
        ruta = env.consumer / dest
        if not ruta.is_symlink():
            problemas.append(f"{dest} no es un enlace")
            continue
        destino = os.readlink(ruta)
        if os.path.isabs(destino) or destino.startswith("\\\\"):
            problemas.append(f"{dest}: el enlace no es relativo ({destino})")
        if Path(os.path.realpath(ruta)) != Path(os.path.realpath(origen)):
            problemas.append(f"{dest}: el enlace no llega al origen")
    tipos = {e["type"] for e in env.entradas().values()}
    if tipos != {"symlink"}:
        problemas.append(f"tipos del registro: {tipos}")
    if (env.consumer / "agents/local-agent.md").is_symlink():
        problemas.append("el overlay quedó convertido en enlace")
    caso("symlink: enlaces relativos que llegan al origen", problemas)

    antes = instantanea(env.base)
    res = run(env.args("--mode", "symlink"))
    extra = [] if instantanea(env.base) == antes else ["el árbol cambió al repetir"]
    check("symlink: idempotente", res, 0, "sin cambios", extra=extra)

    env2 = Entorno(tmp)
    shutil.rmtree(env2.consumer / "agents")
    real = env2.base / "otro-agents"
    real.mkdir()
    os.symlink(os.path.relpath(real, env2.consumer), env2.consumer / "agents")
    check_fail_sin_escribir("symlink: un directorio ancestro enlazado se rechaza", env2, env2.args("--mode", "copy"), "agents", "enlace simbólico")


def casos_auto(tmp: Path) -> None:
    """S8: auto cae a copia cuando el enlace falla; symlink falla sin escribir."""
    try:
        modulo = cargar_modulo()
    except (OSError, ImportError) as exc:
        caso("auto: el script se puede importar", [f"no se pudo importar materialize.py ({exc})"])
        return

    def sin_enlaces(*_args):
        raise OSError("simulado: sin privilegio para enlaces")

    env = Entorno(tmp)
    original = modulo.make_symlink
    modulo.make_symlink = sin_enlaces
    try:
        codigo, salida = en_proceso(modulo, env.args("--mode", "auto"))
    finally:
        modulo.make_symlink = original
    problemas = []
    if codigo != 0:
        problemas.append(f"exit {codigo}")
    if "no permite enlaces simbólicos" not in salida:
        problemas.append("falta el INFO de caída a copia")
    if any(e["type"] != "copy" for e in env.entradas().values()) or len(env.entradas()) != len(TODOS):
        problemas.append("el registro no describe copias de todos los elementos")
    if any((env.consumer / d).is_symlink() for d in TODOS):
        problemas.append("quedó algún enlace")
    caso("auto: cae a copia si el sondeo de enlaces falla", problemas, salida)

    env = Entorno(tmp)
    llamadas = []

    def falla_tras_sonda(*args):
        llamadas.append(args)
        if len(llamadas) > 1:
            raise OSError("simulado: falla el enlace del elemento")
        return original(*args)

    modulo.make_symlink = falla_tras_sonda
    try:
        codigo, salida = en_proceso(modulo, env.args("--mode", "auto"))
    finally:
        modulo.make_symlink = original
    problemas = []
    if codigo != 0:
        problemas.append(f"exit {codigo}")
    if len(env.entradas()) != len(TODOS) or any(e["type"] != "copy" for e in env.entradas().values()):
        problemas.append("el registro no describe copias de todos los elementos")
    if any((env.consumer / d).is_symlink() for d in TODOS):
        problemas.append("quedó algún enlace")
    caso("auto: cae a copia si falla el enlace de un elemento", problemas, salida)

    env = Entorno(tmp)
    antes = instantanea(env.base)
    modulo.make_symlink = sin_enlaces
    try:
        codigo, salida = en_proceso(modulo, env.args("--mode", "symlink"))
    finally:
        modulo.make_symlink = original
    problemas = []
    if codigo != 1 or "FAIL" not in salida:
        problemas.append(f"exit {codigo}, se esperaba 1 con FAIL")
    if instantanea(env.base) != antes:
        problemas.append("se escribió algo pese al FAIL")
    caso("symlink: falla si el sistema no permite enlaces y no escribe", problemas, salida)


def casos_colisiones(tmp: Path) -> None:
    """S6, S8: colisiones entre capas y con el overlay, siempre antes de escribir."""
    env = Entorno(tmp)
    shutil.copy(env.consumer / ".sdaf/agents/specification-agent.md", env.example / "agents/specification-agent.md")
    check_fail_sin_escribir("colisión core/pack", env, env.args("--mode", "copy"),
                            "agents/specification-agent.md", "core", "pack:sdaf-stack-example")

    env = Entorno(tmp)
    shutil.copy(env.example / "agents/example-extension-agent.md", env.otro / "agents/example-extension-agent.md")
    check_fail_sin_escribir("colisión pack/pack", env, env.args("--mode", "copy"),
                            "agents/example-extension-agent.md", "pack:sdaf-stack-example", "pack:sdaf-stack-other")

    env = Entorno(tmp)
    env.escribir("agents/example-extension-agent.md", "# Agente del overlay\n")
    check_fail_sin_escribir("colisión pack/overlay en agente de extensión sin replaces", env,
                            env.args("--mode", "copy"), "agents/example-extension-agent.md", "stack.overlay.replaces")

    env = Entorno(tmp)
    env.escribir("agents/example-extension-agent.md", "# Agente del overlay\n")
    env.config_replaces("example-extension")
    res = run(env.args("--mode", "copy"))
    problemas = []
    if leer(env.consumer / "agents/example-extension-agent.md") != "# Agente del overlay\n":
        problemas.append("el fichero del overlay no se respetó")
    entradas = env.entradas()
    if "agents/example-extension-agent.md" in entradas:
        problemas.append("el agente sustituido figura en el registro")
    for dest in ("prompts/agents/example-extension-agent.md", "skills/example-skill", *CORE, *OTRO):
        if dest not in entradas:
            problemas.append(f"{dest} no se materializó")
    check("pack/overlay con replaces: INFO y overlay intacto", res, 0, "INFO", "agents/example-extension-agent.md",
          ausentes=("FAIL",), extra=problemas)

    env = Entorno(tmp)
    env.escribir("skills/example-skill/SKILL.md", "# Skill del overlay\n")
    env.config_replaces("example-extension", "example-skill")
    check_fail_sin_escribir("colisión pack/overlay en skill, aunque figure en replaces", env,
                            env.args("--mode", "copy"), "skills/example-skill", "skill")

    env = Entorno(tmp)
    env.escribir("prompts/agents/example-extension-agent.md", "# Prompt del overlay\n")
    env.config_replaces("example-extension")
    check_fail_sin_escribir("colisión pack/overlay en prompt, aunque figure en replaces", env,
                            env.args("--mode", "copy"), "prompts/agents/example-extension-agent.md", "prompt")

    env = Entorno(tmp)
    env.escribir("agents/specification-agent.md", "# Agente del overlay\n")
    env.config_replaces("specification")
    check_fail_sin_escribir("id del núcleo en el overlay, aunque figure en replaces", env,
                            env.args("--mode", "copy"), "agents/specification-agent.md", "núcleo")

    env = Entorno(tmp)
    env.escribir("skills/core-skill/SKILL.md", "# Skill del overlay\n")
    check_fail_sin_escribir("skill del núcleo en el overlay", env, env.args("--mode", "copy"),
                            "skills/core-skill", "núcleo")


def casos_articulo_colision(tmp: Path) -> None:
    """Defecto de mensaje: la colisión con el overlay concuerda en género según el tipo."""
    cola = "; las skills y los prompts no se sustituyen"

    env = Entorno(tmp)
    env.escribir("skills/example-skill/SKILL.md", "# Skill del overlay\n")
    env.config_replaces("example-extension", "example-skill")
    check_fail_sin_escribir(
        "colisión pack/overlay en skill: «en una skill»", env, env.args("--mode", "copy"),
        "skills/example-skill: colisión entre el pack sdaf-stack-example y el overlay en una skill" + cola)

    env = Entorno(tmp)
    env.escribir("prompts/agents/example-extension-agent.md", "# Prompt del overlay\n")
    env.config_replaces("example-extension")
    res = run(env.args("--mode", "copy"))
    check(
        "colisión pack/overlay en prompt: «en un prompt»", res, 1,
        "prompts/agents/example-extension-agent.md: colisión entre el pack sdaf-stack-example y el overlay en un prompt"
        + cola,
        ausentes=("en una prompt", "en un skill"),
    )


def casos_ruta_de_pack(tmp: Path) -> None:
    """Los FAIL de un pack muestran la ruta tal como se pasó en --pack, no la resuelta."""
    marca = "sdaf mat"  # prefijo del directorio temporal: delata una ruta absoluta resuelta
    for forma in ("relativa", "absoluta"):
        def ruta(env: Entorno, rel: str) -> str:
            return rel if forma == "relativa" else (env.base / rel).as_posix()

        def lanzar(env: Entorno, *packs: str) -> subprocess.CompletedProcess[str]:
            args = ["--consumer-root", str(env.consumer), "--mode", "copy"]
            for p in packs:
                args += ["--pack", p]
            return run(args, cwd=env.base)

        def ausentes(env: Entorno, rel: str) -> tuple[str, ...]:
            if forma == "absoluta":
                return ()
            return (marca, str(env.base / rel), (env.base / rel).as_posix())

        env = Entorno(tmp)
        arg = ruta(env, "packs/no-existe")
        res = lanzar(env, arg + "/")
        check(f"ruta {forma}: pack inexistente, sin barra final", res, 1, f"FAIL {arg}: no existe el directorio del pack",
              ausentes=(f"{arg}/:", *ausentes(env, "packs/no-existe")))

        env = Entorno(tmp)
        (env.otro / "sdaf-pack.yaml").unlink()
        arg = ruta(env, "packs/otro")
        res = lanzar(env, arg)
        check(f"ruta {forma}: pack sin manifiesto", res, 1, f"FAIL {arg}: falta sdaf-pack.yaml",
              ausentes=ausentes(env, "packs/otro"))

        env = Entorno(tmp)
        (env.otro / "sdaf-pack.yaml").write_text("id: sdaf-stack-other\nversion: 0.2.0\n", encoding="utf-8")
        arg = ruta(env, "packs/otro")
        res = lanzar(env, arg)
        check(f"ruta {forma}: manifiesto inválido", res, 1,
              f"FAIL {arg}/sdaf-pack.yaml: (raíz): falta la propiedad obligatoria 'core', 'provides'",
              ausentes=ausentes(env, "packs/otro"))
        if res.stdout.count("falta la propiedad obligatoria 'core', 'provides'") != 1:
            caso(f"ruta {forma}: el motivo del manifiesto no se repite", ["el motivo sale más de una vez"], res.stdout)

        env = Entorno(tmp)
        shutil.copytree(env.example, env.base / "packs" / "copia")
        primero, segundo = ruta(env, "packs/example"), ruta(env, "packs/copia")
        res = lanzar(env, primero, segundo)
        check(f"ruta {forma}: id repetido", res, 1,
              f"FAIL {segundo}: el pack sdaf-stack-example ya se pasó desde {primero}",
              ausentes=ausentes(env, "packs/copia"))


def casos_dry_run(tmp: Path) -> None:
    """S7: --dry-run imprime el plan y no escribe nada, ni el registro."""
    env = Entorno(tmp)
    antes = instantanea(env.base)
    res = run(env.args("--dry-run"))
    extra = [] if instantanea(env.base) == antes else ["se escribió algo en --dry-run"]
    if (env.consumer / REGISTRO).exists():
        extra.append("se creó el registro")
    check("dry-run: plan sin escribir", res, 0, "plan", "agents/specification-agent.md", "skills/other-skill",
          "dry-run", ausentes=("FAIL",), extra=extra)

    env.escribir("agents/example-extension-agent.md", "# Agente del overlay\n")
    check_fail_sin_escribir("dry-run: detecta colisiones", env, env.args("--dry-run"), "agents/example-extension-agent.md")

    env = Entorno(tmp)
    run(env.args("--mode", "copy"))
    env.escribir(".sdaf/agents/specification-agent.md", "# Nueva versión\n")
    antes = instantanea(env.base)
    res = run(env.args("--mode", "copy", "--dry-run"))
    extra = [] if instantanea(env.base) == antes else ["se escribió algo en --dry-run"]
    check("dry-run sobre una materialización previa: planifica el reemplazo", res, 0, "reemplazar",
          "agents/specification-agent.md", extra=extra)


def casos_idempotencia(tmp: Path) -> None:
    """S7: re-ejecutar reemplaza solo lo registrado y aborta ante cambios ajenos."""
    env = Entorno(tmp)
    run(env.args("--mode", "copy"))
    antes = instantanea(env.base)
    registro = env.bytes_registro()
    res = run(env.args("--mode", "copy"))
    problemas = []
    if instantanea(env.base) != antes:
        problemas.append("el árbol cambió en la segunda ejecución")
    if env.bytes_registro() != registro:
        problemas.append("el registro cambió en la segunda ejecución")
    check("idempotencia: la segunda ejecución no cambia nada", res, 0, "sin cambios", ausentes=("FAIL",), extra=problemas)

    env.escribir(".sdaf/agents/specification-agent.md", "# Nueva versión\n")
    res = run(env.args("--mode", "copy"))
    problemas = []
    if leer(env.consumer / "agents/specification-agent.md") != "# Nueva versión\n":
        problemas.append("la copia registrada no se actualizó")
    if env.entradas().get("agents/specification-agent.md", {}).get("sha256") != sha(env.consumer / ".sdaf/agents/specification-agent.md"):
        problemas.append("el hash del registro no se actualizó")
    check("idempotencia: una copia intacta se reemplaza con el origen nuevo", res, 0, extra=problemas)

    env = Entorno(tmp)
    run(env.args("--mode", "copy"))
    env.escribir("agents/specification-agent.md", "# Editada a mano\n")
    check_fail_sin_escribir("copia registrada editada: FAIL sin escribir", env, env.args("--mode", "copy"),
                            "agents/specification-agent.md", "modificado")

    env = Entorno(tmp)
    run(env.args("--mode", "copy"))
    env.escribir("skills/example-skill/SKILL.md", "# Editada a mano\n")
    check_fail_sin_escribir("skill copiada y editada: FAIL sin escribir", env, env.args("--mode", "copy"),
                            "skills/example-skill", "modificado")

    env = Entorno(tmp)
    run(env.args("--mode", "copy"))
    registro = env.bytes_registro()
    (env.consumer / "agents/specification-agent.md").unlink(missing_ok=True)
    res = run(env.args("--mode", "copy"))
    problemas = []
    if not (env.consumer / "agents/specification-agent.md").is_file():
        problemas.append("no se recreó el elemento registrado ausente")
    if env.bytes_registro() != registro:
        problemas.append("el registro cambió")
    check("idempotencia: un elemento registrado ausente se recrea", res, 0, extra=problemas)

    env = Entorno(tmp)
    run(env.args("--mode", "copy"))
    res = run(env.args("--mode", "copy", packs=[env.example]))
    problemas = []
    for dest in OTRO:
        if (env.consumer / dest).exists():
            problemas.append(f"{dest} no se eliminó")
        if dest in env.entradas():
            problemas.append(f"{dest} sigue en el registro")
    for dest in CORE + EXAMPLE:
        if not (env.consumer / dest).exists() or dest not in env.entradas():
            problemas.append(f"{dest} debía conservarse")
    for overlay in ("agents/local-agent.md", "skills/local-skill/SKILL.md"):
        if not (env.consumer / overlay).exists():
            problemas.append(f"{overlay} del overlay desapareció")
    check("idempotencia: lo que ya no se aporta se elimina si sigue intacto", res, 0, ausentes=("FAIL",), extra=problemas)

    env = Entorno(tmp)
    run(env.args("--mode", "copy"))
    env.escribir("agents/other-extension-agent.md", "# Editada a mano\n")
    res = run(env.args("--mode", "copy", packs=[env.example]))
    problemas = []
    if leer(env.consumer / "agents/other-extension-agent.md") != "# Editada a mano\n":
        problemas.append("se tocó una copia editada que ya no se aporta")
    if "agents/other-extension-agent.md" in env.entradas():
        problemas.append("sigue en el registro")
    check("idempotencia: lo que ya no se aporta y fue editado se conserva con WARN", res, 0, "WARN",
          "agents/other-extension-agent.md", ausentes=("FAIL",), extra=problemas)

    env = Entorno(tmp)
    run(env.args("--mode", "copy"))
    env.escribir(".sdaf/skills/core-skill/references/notas.md", "Cambiada\n")
    res = run(env.args("--mode", "copy"))
    esperado = hash_dir(env.consumer / ".sdaf/skills/core-skill")
    problemas = []
    if env.entradas().get("skills/core-skill", {}).get("sha256") != esperado:
        problemas.append("el hash de la skill no cubre sus ficheros auxiliares")
    check("hash de skill: cambia al cambiar un fichero auxiliar", res, 0, extra=problemas)

    if puede_enlazar(tmp):
        env = Entorno(tmp)
        run(env.args("--mode", "symlink"))
        res = run(env.args("--mode", "copy"))
        problemas = []
        if (env.consumer / "agents/specification-agent.md").is_symlink():
            problemas.append("el enlace registrado no se sustituyó por una copia")
        if {e["type"] for e in env.entradas().values()} != {"copy"}:
            problemas.append("el registro no describe copias")
        check("idempotencia: de enlaces a copias reemplaza los enlaces registrados", res, 0, extra=problemas)
    else:
        saltar("idempotencia: de enlaces a copias", "el sistema no permite enlaces simbólicos")


def casos_errores(tmp: Path) -> None:
    """Entradas inválidas: FAIL limpio, sin traceback y sin escribir."""
    env = Entorno(tmp)
    (env.otro / "sdaf-pack.yaml").write_text("id: [roto\n", encoding="utf-8")
    check_fail_sin_escribir("pack con manifiesto YAML roto", env, env.args("--mode", "copy"), "YAML inválido")

    env = Entorno(tmp)
    (env.otro / "sdaf-pack.yaml").write_text("id: sdaf-stack-other\nversion: 0.2.0\n", encoding="utf-8")
    check_fail_sin_escribir("pack con manifiesto inválido por schema", env, env.args("--mode", "copy"),
                            "sdaf-pack.yaml", "core")

    env = Entorno(tmp)
    (env.otro / "sdaf-pack.yaml").unlink()
    check_fail_sin_escribir("pack sin sdaf-pack.yaml", env, env.args("--mode", "copy"), "falta sdaf-pack.yaml")

    env = Entorno(tmp)
    check_fail_sin_escribir("ruta de pack inexistente", env,
                            env.args("--mode", "copy", packs=[env.base / "no-existe"]), "no existe")

    env = Entorno(tmp)
    check_fail_sin_escribir("mismo id de pack pasado dos veces", env,
                            env.args("--mode", "copy", packs=[env.example, env.example]), "sdaf-stack-example")

    env = Entorno(tmp)
    shutil.rmtree(env.consumer / ".sdaf")
    check_fail_sin_escribir("core inexistente", env, env.args("--mode", "copy"), "core", "no existe")

    env = Entorno(tmp)
    check_fail_sin_escribir("consumer-root inexistente", env,
                            ["--consumer-root", str(env.base / "no-existe"), "--mode", "copy"], "consumer-root")

    env = Entorno(tmp)
    env.escribir("sdaf.config.yaml", "stack: [roto\n")
    check_fail_sin_escribir("config con YAML roto", env, env.args("--mode", "copy"), "sdaf.config.yaml", "YAML inválido")

    env = Entorno(tmp)
    env.escribir("sdaf.config.yaml", "- una\n- lista\n")
    check_fail_sin_escribir("config cuya raíz no es un mapa", env, env.args("--mode", "copy"), "no es un mapa")

    env = Entorno(tmp)
    (env.consumer / "sdaf.config.yaml").unlink()
    res = run(env.args("--mode", "copy"))
    check("sin config: lista de replaces vacía", res, 0, ausentes=("FAIL",))

    env = Entorno(tmp)
    env.escribir(REGISTRO, "{no es json")
    check_fail_sin_escribir("registro corrupto", env, env.args("--mode", "copy"), REGISTRO)

    env = Entorno(tmp)
    env.escribir(REGISTRO, json.dumps({"version": 1, "entries": [
        {"dest": "../fuera.txt", "layer": "core", "origin": "x", "type": "copy", "sha256": "0"}]}))
    check_fail_sin_escribir("registro con destino fuera de la convención", env, env.args("--mode", "copy"),
                            REGISTRO, "convención")

    env = Entorno(tmp)
    env.escribir(REGISTRO, json.dumps({"version": 1, "entries": [
        {"dest": "skills/.", "layer": "core", "origin": "x", "type": "copy", "sha256": "0"}]}))
    check_fail_sin_escribir("registro con destino que es el propio directorio de skills", env,
                            env.args("--mode", "copy"), REGISTRO, "convención")

    env = Entorno(tmp)
    shutil.rmtree(env.consumer / "agents")
    env.escribir("agents", "soy un fichero")
    check_fail_sin_escribir("un ancestro que es un fichero se rechaza", env, env.args("--mode", "copy"),
                            "agents", "no es un directorio")


def casos_defecto(tmp: Path) -> None:
    """S3: --consumer-root y --core toman sus valores por defecto."""
    env = Entorno(tmp)
    res = run(["--mode", "copy", "--pack", str(env.example), "--pack", str(env.otro)], cwd=env.consumer)
    problemas = []
    if not (env.consumer / "agents/specification-agent.md").is_file():
        problemas.append("no se tomó .sdaf como core por defecto")
    if len(env.entradas()) != len(TODOS):
        problemas.append("el registro no está en el directorio actual")
    check("defectos: consumer-root es el directorio actual y core es .sdaf", res, 0, ausentes=("FAIL",), extra=problemas)

    env = Entorno(tmp)
    res = run(["--mode", "copy", "--core", str(env.consumer / ".sdaf")], cwd=env.consumer)
    check("sin packs: solo el core", res, 0, ausentes=("FAIL",),
          extra=[] if sorted(env.entradas()) == sorted(CORE) else ["el registro no contiene solo el core"])


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="sdaf mat ") as tmpdir:
        tmp = Path(tmpdir)
        casos_copia(tmp)
        casos_symlink(tmp)
        casos_auto(tmp)
        casos_colisiones(tmp)
        casos_articulo_colision(tmp)
        casos_ruta_de_pack(tmp)
        casos_dry_run(tmp)
        casos_idempotencia(tmp)
        casos_errores(tmp)
        casos_defecto(tmp)
    print(f"fallos: {len(FALLOS)}, saltados: {len(SALTADOS)}")
    return 1 if FALLOS else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
