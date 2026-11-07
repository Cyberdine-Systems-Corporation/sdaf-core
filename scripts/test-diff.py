#!/usr/bin/env python3
"""Autocomprobación de la lectura de rutas de código (sdaf_diff.py).

Ejercita `load_units`, `load_product_prefixes` e `is_product` con configs
escritas en directorios temporales (fuera del repo): atajo `src_path`/
`tests_path`, `stack.units` y lectura endurecida (una config ilegible lanza
`ConfigUnreadable`, nunca otra excepción). Imprime OK/FAIL por caso. Sale 0 si
todos pasan y 1 si alguno falla.
"""
from __future__ import annotations

import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import sdaf_diff  # noqa: E402
from sdaf_diff import ConfigUnreadable, Unit, is_product, load_product_prefixes, load_units  # noqa: E402

DEFAULT_UNITS = [Unit(None, "src", "tests")]
DEFAULT_PREFIXES = ["src/", "tests/"]
UNREADABLE = "ilegible"  # marca de resultado esperado: ConfigUnreadable

# (etiqueta, contenido de sdaf.config.yaml o None si no existe, unidades esperadas, prefijos esperados)
CASES: list[tuple[str, str | bytes | None, Any, Any]] = [
    ("sin config: unidad por defecto", None, DEFAULT_UNITS, DEFAULT_PREFIXES),
    ("config sin stack: unidad por defecto", "sdaf:\n  version: \"0.5.0\"\n", DEFAULT_UNITS, DEFAULT_PREFIXES),
    ("stack sin rutas: unidad por defecto", "stack:\n  packs: []\n", DEFAULT_UNITS, DEFAULT_PREFIXES),
    ("stack nulo: unidad por defecto", "stack:\n", DEFAULT_UNITS, DEFAULT_PREFIXES),
    ("config vacío", "", DEFAULT_UNITS, DEFAULT_PREFIXES),
    ("config {}", "{}\n", DEFAULT_UNITS, DEFAULT_PREFIXES),
    ("config de solo comentarios", "# nada\n# más nada\n", DEFAULT_UNITS, DEFAULT_PREFIXES),
    ("atajo con rutas propias",
     "stack:\n  src_path: apps/api\n  tests_path: apps/api.tests\n",
     [Unit(None, "apps/api", "apps/api.tests")], ["apps/api/", "apps/api.tests/"]),
    ("atajo con barra invertida y barra final",
     "stack:\n  src_path: 'apps\\api\\'\n  tests_path: tests/unit/\n",
     [Unit(None, "apps\\api\\", "tests/unit/")], ["apps/api/", "tests/unit/"]),
    ("atajo solo con src_path: tests por defecto",
     "stack:\n  src_path: apps/api\n", [Unit(None, "apps/api", "tests")], ["apps/api/", "tests/"]),
    ("atajo solo con tests_path: src por defecto",
     "stack:\n  tests_path: spec\n", [Unit(None, "src", "spec")], ["src/", "spec/"]),
    ("atajo con src_path: . (se conserva ./)",
     "stack:\n  src_path: .\n", [Unit(None, ".", "tests")], ["./", "tests/"]),
    ("atajo con rutas vacías: por defecto",
     "stack:\n  src_path: ''\n  tests_path:\n", DEFAULT_UNITS, DEFAULT_PREFIXES),
    ("units con dos unidades (una sin tests)",
     "stack:\n  units:\n    - name: Unidad A\n      src: apps/api\n      tests: tests/api\n"
     "    - name: Unidad B\n      src: libs/core\n",
     [Unit("Unidad A", "apps/api", "tests/api"), Unit("Unidad B", "libs/core", None)],
     ["apps/api/", "tests/api/", "libs/core/"]),
    ("units sin nombre ni tests, con barra invertida",
     "stack:\n  units:\n    - src: 'apps\\web\\'\n", [Unit(None, "apps\\web\\", None)], ["apps/web/"]),
    ("units más atajo: gana units",
     "stack:\n  src_path: otro\n  tests_path: otro-tests\n  units:\n    - name: A\n      src: apps/api\n",
     [Unit("A", "apps/api", None)], ["apps/api/"]),
    ("units con rutas repetidas: sin duplicados y en orden",
     "stack:\n  units:\n    - name: A\n      src: apps/api\n      tests: tests\n"
     "    - name: B\n      src: apps/api/\n      tests: tests\n    - name: C\n      src: tests\n",
     [Unit("A", "apps/api", "tests"), Unit("B", "apps/api/", "tests"), Unit("C", "tests", None)],
     ["apps/api/", "tests/"]),
    ("units vacía", "stack:\n  units: []\n", UNREADABLE, UNREADABLE),
    ("units nula", "stack:\n  units:\n", UNREADABLE, UNREADABLE),
    ("units no es lista (texto)", "stack:\n  units: apps/api\n", UNREADABLE, UNREADABLE),
    ("units no es lista (mapa)", "stack:\n  units:\n    src: apps/api\n", UNREADABLE, UNREADABLE),
    ("unidad que no es mapa (texto)", "stack:\n  units:\n    - apps/api\n", UNREADABLE, UNREADABLE),
    ("unidad que no es mapa (nula)", "stack:\n  units:\n    -\n", UNREADABLE, UNREADABLE),
    ("unidad sin src", "stack:\n  units:\n    - name: A\n      tests: t\n", UNREADABLE, UNREADABLE),
    ("unidad con src numérico", "stack:\n  units:\n    - name: A\n      src: 3\n", UNREADABLE, UNREADABLE),
    ("unidad con src en lista", "stack:\n  units:\n    - name: A\n      src: [a]\n", UNREADABLE, UNREADABLE),
    ("unidad con src vacío", "stack:\n  units:\n    - name: A\n      src: ''\n", UNREADABLE, UNREADABLE),
    ("unidad con src nulo", "stack:\n  units:\n    - name: A\n      src:\n", UNREADABLE, UNREADABLE),
    ("unidad con tests que no es texto",
     "stack:\n  units:\n    - name: A\n      src: a\n      tests: [t]\n", UNREADABLE, UNREADABLE),
    ("una unidad mala entre buenas",
     "stack:\n  units:\n    - src: a\n    - 7\n", UNREADABLE, UNREADABLE),
    ("YAML roto", "stack: [sin cerrar\n", UNREADABLE, UNREADABLE),
    ("no es UTF-8", "stack:\n  src_path: caf\xe9\n".encode("latin-1"), UNREADABLE, UNREADABLE),
    ("raíz que es lista", "- stack\n- otro\n", UNREADABLE, UNREADABLE),
    ("raíz que es texto", "solo texto\n", UNREADABLE, UNREADABLE),
    ("stack que es lista", "stack:\n  - src_path\n", UNREADABLE, UNREADABLE),
    ("stack que es texto", "stack: texto\n", UNREADABLE, UNREADABLE),
]


@contextmanager
def consumer(config: str | bytes | None) -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        if isinstance(config, bytes):
            (root / "sdaf.config.yaml").write_bytes(config)
        elif config is not None:
            (root / "sdaf.config.yaml").write_text(config, encoding="utf-8", newline="\n")
        yield root


def outcome(fn: Any, root: Path) -> Any:
    """Resultado de la función, UNREADABLE si lanza ConfigUnreadable con motivo, o la excepción inesperada."""
    try:
        return fn(root)
    except ConfigUnreadable as exc:
        return UNREADABLE if str(exc).strip() else f"ConfigUnreadable sin motivo: {exc!r}"
    except Exception as exc:  # noqa: BLE001 - se informa como fallo del caso
        return f"{type(exc).__name__}: {exc}"


def expect(label: str, got: Any, want: Any) -> bool:
    if got != want:
        print(f"FAIL {label}: se obtuvo {got!r} (se esperaba {want!r})")
        return False
    print(f"OK {label}")
    return True


def test_cases() -> bool:
    ok = True
    for label, config, want_units, want_prefixes in CASES:
        with consumer(config) as root:
            ok &= expect(f"load_units: {label}", outcome(load_units, root), want_units)
            ok &= expect(f"load_product_prefixes: {label}", outcome(load_product_prefixes, root), want_prefixes)
    return ok


def test_unreadable_file() -> bool:
    """Un fichero que existe pero no se puede leer es ConfigUnreadable, no OSError."""
    with consumer("stack:\n  src_path: a\n") as root:
        with mock.patch.object(Path, "read_text", side_effect=PermissionError("denegado")):
            got = outcome(load_units, root)
    return expect("load_units: fichero ilegible (OSError)", got, UNREADABLE)


def test_directory_is_not_config() -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "sdaf.config.yaml").mkdir()
        return expect("load_units: sdaf.config.yaml que es un directorio = sin config",
                      outcome(load_units, root), DEFAULT_UNITS)


def test_reason_is_short() -> bool:
    ok = True
    for label, config in (("YAML roto", "stack: [sin cerrar\n"), ("stack lista", "stack:\n  - a\n"),
                          ("units vacía", "stack:\n  units: []\n")):
        with consumer(config) as root:
            try:
                load_units(root)
                ok &= expect(f"motivo de {label}", "sin excepción", "ConfigUnreadable")
            except ConfigUnreadable as exc:
                reason = str(exc)
                ok &= expect(f"motivo de {label}: una línea y breve", "\n" not in reason and 0 < len(reason) <= 120,
                             True)
    return ok


def test_is_product() -> bool:
    ok = True
    units = ("stack:\n  units:\n    - name: A\n      src: apps/api\n      tests: tests/api\n"
             "    - name: B\n      src: libs/core\n")
    with consumer(units) as root:
        prefixes = load_product_prefixes(root)
    for path, want in (
        ("apps/api/x.py", True),
        ("apps/api", True),
        ("apps\\api\\x.py", True),
        ("tests/api/t.py", True),
        ("libs/core/lib.py", True),
        ("apps/api2/x.py", False),
        ("apps/apix", False),
        ("libs/core2/lib.py", False),
        ("src/Foo.cs", False),
        ("tests/otro/t.py", False),
        ("worklogs/PBI-1/Iteration-001.md", False),
    ):
        ok &= expect(f"is_product con varias unidades: {path}", is_product(path, prefixes), want)
    ok &= expect("is_product con prefijos por defecto: src/Foo.cs", is_product("src/Foo.cs", DEFAULT_PREFIXES), True)
    ok &= expect("is_product con prefijos por defecto: src2/Foo.cs", is_product("src2/Foo.cs", DEFAULT_PREFIXES), False)
    return ok


def test_public_surface() -> bool:
    """El contrato que otros scripts importan sigue ahí."""
    return expect("sdaf_diff expone lo que importan los comprobadores",
                  all(hasattr(sdaf_diff, n) for n in ("DiffUnavailable", "git_changed", "is_product",
                                                       "load_product_prefixes", "load_units", "ConfigUnreadable")),
                  True) and expect("ConfigUnreadable es un ValueError", issubclass(ConfigUnreadable, ValueError), True)


def main() -> int:
    results = [test_cases(), test_unreadable_file(), test_directory_is_not_config(), test_reason_is_short(),
               test_is_product(), test_public_surface()]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
