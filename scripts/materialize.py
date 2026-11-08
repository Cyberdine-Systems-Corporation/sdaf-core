#!/usr/bin/env python3
"""Materializa los aportes del core y de los packs en un repositorio consumidor.

Orden de capas: core, después los packs (en el orden de `--pack`) y por último el
overlay del consumidor (ADR-007 §7). Los aportes se reconocen por convención de
ruta, idéntica en el core y en cada pack, y se materializan en la misma ruta
relativa de la raíz del consumidor:

    agents/<id>-agent.md
    prompts/agents/<id>-agent.md
    skills/<id>/SKILL.md      (la skill se materializa como el directorio skills/<id>/)

Solo existen esos tres tipos de aporte. El overlay no es una capa que el script
cree: es lo que ya hay en el destino como fichero o directorio real, que no es un
enlace simbólico ni un elemento del registro lateral.

Uso:

    materialize.py [--consumer-root RAIZ] [--core RUTA] [--pack RUTA]...
                   [--mode auto|symlink|copy] [--dry-run]

`--consumer-root` toma por defecto el directorio actual y `--core` toma
`<consumer-root>/.sdaf`. Cada `--pack` es la raíz de un pack con `sdaf-pack.yaml`,
validado con `sdaf_packs` (un manifiesto inválido o ausente es un FAIL).

Modos: `symlink` crea enlaces simbólicos RELATIVOS y falla si el sistema no los
permite; `copy` copia siempre; `auto` (defecto) intenta el enlace y cae a copia si
el sistema no lo permite. Nunca se crean junctions.

Marca de origen: el fichero `.sdaf-origin` de la raíz del consumidor (JSON ordenado,
UTF-8, LF) registra cada elemento materializado, enlace o copia: destino, capa
(`core` o `pack:<id>`), origen relativo a la raíz, tipo y sha256 (del contenido; para
una skill, un hash determinista de sus ficheros). El contenido copiado no se altera.

Colisiones, todas detectadas antes de escribir nada:
- el mismo destino aportado por dos capas (core y pack, o dos packs): error;
- un destino ocupado por un aporte real del overlay: error para el núcleo, para las
  skills y para los prompts; para el contrato de agente de un pack, error salvo que su
  id figure en `stack.overlay.replaces` de `sdaf.config.yaml` (ADR-007 §5): entonces
  el aporte del pack se omite con un INFO y el fichero del overlay se respeta.
Del `sdaf.config.yaml` del consumidor solo se lee esa lista (opcional).

Idempotencia: al volver a ejecutar solo se reemplazan los elementos del registro cuyo
destino siga siendo el enlace o la copia registrada. Una copia editada, o un destino
real no registrado que choca con un aporte no permitido, aborta con FAIL sin escribir
nada. Un elemento registrado que ya no se aporta se elimina solo si sigue intacto; si
no, se conserva, se avisa con WARN y deja de figurar en el registro. `--dry-run`
imprime el plan y no escribe nada, tampoco el registro.

Salida: líneas `OK`, `INFO`, `WARN` y `FAIL <motivo>`; código 0 si todo va bien y 1 si
hay algún FAIL.

Límites conocidos: el script no valida `provides` contra los ficheros reales del pack
(lo que se materializa es lo que hay en disco) y no materializa AGENTS.md ni las
reglas de editor.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sdaf_packs import load_manifest, read_manifest  # noqa: E402

REGISTRY_NAME = ".sdaf-origin"
CONFIG_NAME = "sdaf.config.yaml"
MANIFEST_NAME = "sdaf-pack.yaml"
AGENT_SUFFIX = "-agent.md"
REGISTRY_VERSION = 1
DEST_PATTERNS = (
    re.compile(r"agents/[^/]+-agent\.md"),
    re.compile(r"prompts/agents/[^/]+-agent\.md"),
    re.compile(r"skills/[^/]+"),
)


class MaterializeError(Exception):
    """Fallo controlado: se informa como FAIL, nunca como traceback."""


@dataclass(frozen=True)
class Item:
    dest: str  # ruta relativa a la raíz del consumidor, con `/`
    kind: str  # agent | prompt | skill
    ident: str
    layer: str  # core | pack:<id>
    source: Path
    is_dir: bool


@dataclass
class Action:
    op: str  # create | replace | unchanged | skip | remove
    dest: str
    layer: str = ""
    type: str = ""
    entry: dict | None = None  # entrada del registro resultante (o la retirada)
    item: Item | None = None


# --- hashes y sistema de ficheros -------------------------------------------------


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 16), b""):
            digest.update(block)
    return digest.hexdigest()


def hash_path(path: Path) -> str:
    """sha256 de un fichero o hash determinista de los ficheros de un directorio."""
    if not path.is_dir():
        return sha256_file(path)
    files = {
        f.relative_to(path).as_posix(): f for f in path.rglob("*") if f.is_file()
    }
    digest = hashlib.sha256()
    for rel in sorted(files):
        digest.update(rel.encode("utf-8") + b"\0" + sha256_file(files[rel]).encode() + b"\n")
    return digest.hexdigest()


def make_symlink(target: str, dest: Path, is_dir: bool) -> None:
    """Único punto donde se crean enlaces simbólicos (nunca junctions)."""
    os.symlink(target, dest, target_is_directory=is_dir)


def symlinks_available() -> bool:
    """Sondea en un directorio temporal si el sistema permite crear enlaces simbólicos."""
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        (base / "t.txt").write_text("x", encoding="utf-8")
        try:
            make_symlink("t.txt", base / "l.txt", False)
        except (OSError, NotImplementedError):
            return False
        return (base / "l.txt").is_symlink()


def remove_path(path: Path) -> None:
    if path.is_symlink():
        try:
            path.unlink()
        except OSError:
            os.rmdir(path)
    elif path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def norm(text: str) -> str:
    return text.replace("\\", "/")


def rel_origin(consumer: Path, source: Path) -> str:
    """Origen relativo a la raíz del consumidor; absoluto si no hay ruta relativa."""
    try:
        return norm(os.path.relpath(source, consumer))
    except ValueError:
        return source.as_posix()


def link_target(consumer: Path, origin: str, dest: str) -> str | None:
    """Destino relativo del enlace desde el directorio de `dest`; None si no existe."""
    source = Path(os.path.abspath(consumer / origin))
    parent = Path(os.path.abspath(consumer / dest)).parent
    try:
        return os.path.relpath(source, parent)
    except ValueError:
        return None


# --- lectura de entradas ----------------------------------------------------------


def read_replaces(consumer: Path) -> list[str]:
    """Ids de `stack.overlay.replaces`; vacío si no hay config o no hay lista."""
    path = consumer / CONFIG_NAME
    if not os.path.lexists(path):
        return []
    data, error = load_manifest(path)
    if error:
        raise MaterializeError(f"{CONFIG_NAME}: {error}")
    if data is None:
        return []
    if not isinstance(data, dict):
        raise MaterializeError(f"{CONFIG_NAME}: la raíz no es un mapa")
    stack = data.get("stack")
    overlay = stack.get("overlay") if isinstance(stack, dict) else None
    replaces = overlay.get("replaces") if isinstance(overlay, dict) else None
    if not isinstance(replaces, list):
        return []
    return [x for x in replaces if isinstance(x, str)]


def load_registry(consumer: Path) -> dict[str, dict]:
    path = consumer / REGISTRY_NAME
    if not os.path.lexists(path):
        return {}
    try:
        data = json.loads(path.read_bytes().decode("utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise MaterializeError(f"{REGISTRY_NAME}: registro ilegible ({exc})") from exc
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        raise MaterializeError(f"{REGISTRY_NAME}: falta la lista 'entries'")
    registry: dict[str, dict] = {}
    for entry in entries:
        ok = isinstance(entry, dict) and all(
            isinstance(entry.get(k), str) for k in ("dest", "layer", "origin", "type", "sha256")
        )
        if not ok or entry["type"] not in ("symlink", "copy"):
            raise MaterializeError(f"{REGISTRY_NAME}: entrada mal formada ({entry!r})")
        dest = entry["dest"]
        if not any(p.fullmatch(dest) for p in DEST_PATTERNS) or any(
            part in ("", ".", "..") for part in dest.split("/")
        ):
            raise MaterializeError(f"{REGISTRY_NAME}: destino fuera de la convención ({dest!r})")
        if dest in registry:
            raise MaterializeError(f"{REGISTRY_NAME}: destino repetido ({dest})")
        registry[dest] = entry
    return registry


def collect(layer: str, root: Path) -> list[Item]:
    """Aportes de una capa por convención de ruta."""
    items: list[Item] = []
    for sub, kind in (("agents", "agent"), ("prompts/agents", "prompt")):
        base = root / sub
        if not base.is_dir():
            continue
        for entry in sorted(base.iterdir(), key=lambda p: p.name):
            name = entry.name
            if entry.is_file() and name.endswith(AGENT_SUFFIX) and len(name) > len(AGENT_SUFFIX):
                items.append(Item(f"{sub}/{name}", kind, name[: -len(AGENT_SUFFIX)], layer, entry, False))
    skills = root / "skills"
    if skills.is_dir():
        for entry in sorted(skills.iterdir(), key=lambda p: p.name):
            if entry.is_dir() and (entry / "SKILL.md").is_file():
                items.append(Item(f"skills/{entry.name}", "skill", entry.name, layer, entry, True))
    return items


def resolve_layers(
    consumer: Path, core: Path, pack_args: list[str], errors: list[str]
) -> list[tuple[str, Path]]:
    """Valida el core y los packs; devuelve [(capa, raíz)] en orden core -> packs."""
    layers: list[tuple[str, Path]] = []
    if not core.is_dir():
        errors.append(f"core: no existe el directorio {core}")
    else:
        layers.append(("core", core))
    seen: dict[str, str] = {}
    for arg in pack_args:
        root = Path(os.path.abspath(arg))
        # Los FAIL de un pack muestran la ruta tal como se pasó en --pack (sin barras
        # finales), no la ruta resuelta: un pack fuera del repo del core no se delata
        # con una ruta absoluta que el usuario no escribió.
        label = arg.rstrip("/\\") or arg
        if not root.is_dir():
            errors.append(f"{label}: no existe el directorio del pack")
            continue
        manifest = root / MANIFEST_NAME
        if not manifest.is_file():
            errors.append(f"{label}: falta {MANIFEST_NAME}")
            continue
        data, reasons = read_manifest(manifest)
        if data is None:
            errors.extend(f"{label}/{MANIFEST_NAME}: {reason}" for reason in reasons)
            continue
        if data["id"] in seen:
            errors.append(f"{label}: el pack {data['id']} ya se pasó desde {seen[data['id']]}")
            continue
        seen[data["id"]] = label
        layers.append((f"pack:{data['id']}", root))
    return layers


# --- plan -------------------------------------------------------------------------


def intact(consumer: Path, entry: dict) -> bool:
    """True si el destino sigue siendo el enlace o la copia que el registro describe."""
    path = consumer / entry["dest"]
    if entry["type"] == "symlink":
        if not path.is_symlink():
            return False
        expected = link_target(consumer, entry["origin"], entry["dest"])
        return expected is not None and norm(os.readlink(path)) == norm(expected)
    if path.is_symlink() or not path.exists():
        return False
    return hash_path(path) == entry["sha256"]


def ancestor_problem(consumer: Path, dest: str) -> str | None:
    current = consumer
    for part in dest.split("/")[:-1]:
        current = current / part
        if current.is_symlink():
            return f"{dest}: el directorio {current.relative_to(consumer).as_posix()} es un enlace simbólico"
        if os.path.lexists(current) and not current.is_dir():
            return f"{dest}: {current.relative_to(consumer).as_posix()} existe y no es un directorio"
    return None


def overlay_decision(item: Item, replaces: list[str]) -> tuple[bool, str]:
    """(omitir, motivo de error) ante un aporte real del overlay en el destino."""
    if item.layer == "core":
        return False, f"{item.dest}: el overlay ocupa un destino del núcleo; los ids del núcleo no se sustituyen"
    if item.kind == "agent":
        if item.ident in replaces:
            return True, ""
        return False, (
            f"{item.dest}: colisión entre el pack {item.layer[5:]} y el overlay; "
            f"declare '{item.ident}' en stack.overlay.replaces para sustituirlo"
        )
    what = "una skill" if item.kind == "skill" else "un prompt"
    return False, (
        f"{item.dest}: colisión entre el pack {item.layer[5:]} y el overlay en {what}; "
        "las skills y los prompts no se sustituyen"
    )


def build_plan(
    consumer: Path,
    items: list[Item],
    registry: dict[str, dict],
    replaces: list[str],
    planned_type: str,
) -> tuple[list[Action], list[str], list[str]]:
    """Calcula las acciones sin escribir. Devuelve (acciones, errores, avisos)."""
    errors: list[str] = []
    warnings: list[str] = []
    actions: list[Action] = []
    by_dest: dict[str, list[Item]] = {}
    for item in items:
        by_dest.setdefault(item.dest, []).append(item)

    for dest in sorted(by_dest):
        group = by_dest[dest]
        if len(group) > 1:
            layers = " y ".join(i.layer for i in group)
            errors.append(f"{dest}: colisión, lo aportan {layers}")
            continue
        item = group[0]
        problem = ancestor_problem(consumer, dest)
        if problem:
            errors.append(problem)
            continue
        path = consumer / dest
        if os.path.abspath(path) == os.path.abspath(item.source):
            errors.append(f"{dest}: el origen y el destino son el mismo")
            continue
        new_entry = {
            "dest": dest,
            "layer": item.layer,
            "origin": rel_origin(consumer, Path(os.path.abspath(item.source))),
            "type": planned_type,
            "sha256": hash_path(item.source),
        }
        registered = registry.get(dest)
        if registered is not None:
            if not os.path.lexists(path):
                actions.append(Action("create", dest, item.layer, planned_type, new_entry, item))
            elif not intact(consumer, registered):
                errors.append(
                    f"{dest}: el elemento registrado ({registered['type']}) fue modificado; "
                    "revíselo o elimínelo antes de volver a materializar"
                )
            elif {k: registered[k] for k in new_entry} == new_entry:
                actions.append(Action("unchanged", dest, item.layer, planned_type, registered, item))
            else:
                actions.append(Action("replace", dest, item.layer, planned_type, new_entry, item))
        elif os.path.lexists(path):
            if path.is_symlink():
                errors.append(f"{dest}: el destino es un enlace simbólico que no figura en {REGISTRY_NAME}")
                continue
            skip, reason = overlay_decision(item, replaces)
            if skip:
                actions.append(Action("skip", dest, item.layer, "", None, item))
            else:
                errors.append(reason)
        else:
            actions.append(Action("create", dest, item.layer, planned_type, new_entry, item))

    for dest in sorted(registry):
        if dest in by_dest:
            continue
        entry = registry[dest]
        path = consumer / dest
        if not os.path.lexists(path):
            actions.append(Action("drop", dest, entry["layer"], entry["type"], entry))
        elif intact(consumer, entry):
            actions.append(Action("remove", dest, entry["layer"], entry["type"], entry))
        else:
            warnings.append(
                f"{dest}: ya no se aporta y fue modificado; se conserva y deja de figurar en {REGISTRY_NAME}"
            )
            actions.append(Action("drop", dest, entry["layer"], entry["type"], entry))
    return actions, errors, warnings


# --- aplicación -------------------------------------------------------------------


def write_item(consumer: Path, action: Action, mode: str) -> str:
    """Escribe un elemento y devuelve el tipo realmente creado (symlink | copy)."""
    item = action.item
    assert item is not None
    dest = consumer / item.dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    if action.type == "symlink":
        target = link_target(consumer, action.entry["origin"], item.dest)
        try:
            if target is None:
                raise OSError("no hay ruta relativa entre el destino y el origen")
            make_symlink(target, dest, item.is_dir)
            return "symlink"
        except (OSError, NotImplementedError) as exc:
            if mode == "symlink":
                raise MaterializeError(f"{item.dest}: no se pudo crear el enlace simbólico ({exc})") from exc
            if os.path.lexists(dest):
                remove_path(dest)
    if item.is_dir:
        shutil.copytree(item.source, dest)
    else:
        shutil.copyfile(item.source, dest)
    return "copy"


def save_registry(consumer: Path, entries: dict[str, dict], had_registry: bool) -> None:
    if not entries and not had_registry:
        return
    body = {"version": REGISTRY_VERSION, "entries": [entries[d] for d in sorted(entries)]}
    text = json.dumps(body, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    (consumer / REGISTRY_NAME).write_bytes(text.encode("utf-8"))


def describe(action: Action) -> str:
    where = f"{action.dest} <- {action.layer} [{action.type}]"
    return where


def apply_plan(consumer: Path, actions: list[Action], registry: dict[str, dict], mode: str) -> None:
    entries = dict(registry)
    had_registry = os.path.lexists(consumer / REGISTRY_NAME)
    try:
        for action in actions:
            if action.op in ("remove", "drop"):
                if action.op == "remove":
                    remove_path(consumer / action.dest)
                    print(f"OK  {action.dest} eliminado (ya no se aporta, {action.layer})")
                else:
                    print(f"INFO {action.dest} deja de figurar en {REGISTRY_NAME}")
                entries.pop(action.dest, None)
        for action in actions:
            if action.op == "skip":
                print(f"INFO {action.dest}: se respeta el del overlay (stack.overlay.replaces), se omite el de {action.layer}")
            elif action.op == "unchanged":
                print(f"OK  {action.dest} sin cambios ({action.layer})")
            elif action.op in ("create", "replace"):
                path = consumer / action.dest
                if os.path.lexists(path):
                    remove_path(path)
                actual = write_item(consumer, action, mode)
                if actual != action.type:
                    print(f"INFO {action.dest}: sin enlaces simbólicos, se copia")
                    action.entry = {**action.entry, "type": actual}
                    action.type = actual
                entries[action.dest] = action.entry
                print(f"OK  {describe(action)}")
    finally:
        save_registry(consumer, entries, had_registry)


def print_plan(actions: list[Action]) -> None:
    labels = {"create": "crear", "replace": "reemplazar", "unchanged": "sin cambios",
              "remove": "eliminar", "drop": "dejar de registrar"}
    for action in actions:
        if action.op == "skip":
            print(f"INFO plan: {action.dest} se respeta el del overlay, se omite el de {action.layer}")
        else:
            print(f"INFO plan: {labels[action.op]} {describe(action)}")


# --- orquestación -----------------------------------------------------------------


def run(args: argparse.Namespace) -> int:
    consumer = Path(os.path.abspath(args.consumer_root))
    if not consumer.is_dir():
        print(f"FAIL consumer-root: no existe el directorio {consumer}")
        return 1
    core = Path(os.path.abspath(args.core)) if args.core else consumer / ".sdaf"
    errors: list[str] = []
    layers = resolve_layers(consumer, core, args.pack, errors)
    if errors:
        for reason in errors:
            print(f"FAIL {reason}")
        return 1

    replaces = read_replaces(consumer)
    registry = load_registry(consumer)
    items = [item for layer, root in layers for item in collect(layer, root)]

    planned_type = "copy"
    if args.mode != "copy":
        if symlinks_available():
            planned_type = "symlink"
        elif args.mode == "symlink":
            print("FAIL --mode symlink: el sistema no permite crear enlaces simbólicos; use --mode copy o auto")
            return 1
        else:
            print("INFO el sistema no permite enlaces simbólicos: se copia")

    actions, errors, warnings = build_plan(consumer, items, registry, replaces, planned_type)
    for reason in warnings:
        print(f"WARN {reason}")
    if errors:
        for reason in errors:
            print(f"FAIL {reason}")
        print("FAIL no se escribió nada")
        return 1

    if args.dry_run:
        print_plan(actions)
        print(f"OK  dry-run: {len(actions)} acciones planificadas, no se escribió nada")
        return 0
    apply_plan(consumer, actions, registry, args.mode)
    written = [a for a in actions if a.op in ("create", "replace", "unchanged")]
    print(f"OK  {len(written)} elementos materializados desde {len(layers)} capas ({REGISTRY_NAME})")
    return 0


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Materializa agents, prompts y skills del core y de los packs en un consumidor."
    )
    parser.add_argument("--consumer-root", default=".", help="raíz del consumidor (defecto: directorio actual)")
    parser.add_argument("--core", help="raíz del core (defecto: <consumer-root>/.sdaf)")
    parser.add_argument("--pack", action="append", default=[], metavar="RUTA",
                        help="raíz de un pack con sdaf-pack.yaml; repetible")
    parser.add_argument("--mode", choices=("auto", "symlink", "copy"), default="auto")
    parser.add_argument("--dry-run", action="store_true", help="imprime el plan y no escribe nada")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        return run(args)
    except MaterializeError as exc:
        print(f"FAIL {exc}")
        return 1
    except OSError as exc:
        print(f"FAIL error del sistema de ficheros: {exc.strerror or exc} ({exc.filename or ''})".replace(" ()", ""))
        return 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
