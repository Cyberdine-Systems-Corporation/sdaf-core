#!/usr/bin/env python3
"""Autocomprobación del ciclo de vida de ADRs (ADR-006).

Ejecuta check-adrs.py sobre un fixture estático válido y sobre árboles
temporales inválidos, y comprueba que sale 0 en el primero y 1, con el
mensaje esperado, en cada caso inválido.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import sdaf_adrs  # noqa: E402

ADRS = ROOT / "scripts" / "check-adrs.py"
FIXTURE = ROOT / "scripts" / "testdata" / "adrs-ciclo-valido"
FIXTURE_HEREDADO = ROOT / "scripts" / "testdata" / "adrs-consumidor-heredado"
CONSUMER = ("--consumer",)

FECHA = "2026-09-01T10:00+02:00"
ACEPTACION = "2026-09-02T10:00+02:00, por Persona de prueba."

Adr = tuple[str, str, dict[str, str]]  # (número, estado, filas extra)


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ADRS), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def expect(label: str, proc: subprocess.CompletedProcess[str], code: int, needle: str = "") -> bool:
    if proc.returncode != code or (needle and needle not in proc.stdout):
        print(f"FAIL {label}: exit {proc.returncode} (se esperaba {code}), falta «{needle}»")
        print(proc.stdout + proc.stderr)
        return False
    print(f"OK {label}")
    return True


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def adr_text(num: str, estado: str, extra: dict[str, str]) -> str:
    """ADR mínimo; añade Aceptación a Aceptado y Sustituido salvo que `extra` la fije."""
    rows = {"Estado": estado, "Fecha": FECHA, "Decisores": "Persona de prueba"}
    if estado in {"Aceptado", "Sustituido"}:
        rows["Aceptación"] = ACEPTACION
    rows.update(extra)
    body = "\n".join(f"| {k} | {v} |" for k, v in rows.items() if v is not None)
    return (
        f"# ADR-{num} — Prueba\n\n| Campo | Valor |\n|--------|--------|\n{body}\n\n"
        "## Decisión\n\nPrueba.\n"
    )


def adr_tree(root: Path, adrs: list[Adr], columna: dict[str, str] | None = None) -> None:
    """Escribe los ADRs y un README coherente; `columna` fuerza la 4.ª columna de algunas filas."""
    folder = root / "architecture" / "decisions"
    rows = []
    for num, estado, extra in adrs:
        write(folder / f"ADR-{num}-prueba.md", adr_text(num, estado, extra))
        sust = extra.get("Sustituido por", "—")
        rows.append(f"| [ADR-{num}](ADR-{num}-prueba.md) | {estado} | Prueba | {(columna or {}).get(num, sust)} |")
    write(
        folder / "README.md",
        "# ADRs\n\n| ADR | Estado | Título | Sustituido por |\n|-----|--------|--------|----------------|\n"
        + "\n".join(rows)
        + "\n",
    )


def invalid(label: str, adrs: list[Adr], needle: str, columna: dict[str, str] | None = None,
            args: tuple[str, ...] = ()) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        adr_tree(Path(tmp), adrs, columna)
        return expect(f"ADRs: {label}", run("--root", tmp, *args), 1, needle)


def valid(label: str, adrs: list[Adr], columna: dict[str, str] | None = None,
          args: tuple[str, ...] = ()) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        adr_tree(Path(tmp), adrs, columna)
        return expect(f"ADRs: {label}", run("--root", tmp, *args), 0, "OK ADRs")


def test_fixture() -> bool:
    return expect("ADRs: fixture del ciclo de vida válido", run("--root", str(FIXTURE)), 0, "OK ADRs (6)")


def test_valid_variants() -> bool:
    ok = True
    # Propuesto que sustituye: la reciprocidad queda pendiente de la aceptación.
    ok &= valid("Propuesto que sustituye a un Aceptado",
                [("001", "Aceptado", {}), ("002", "Propuesto", {"Sustituye": "ADR-001"})])
    # README de un consumidor anterior, sin la 4.ª columna.
    with tempfile.TemporaryDirectory() as tmp:
        adr_tree(Path(tmp), [("001", "Aceptado", {})])
        write(Path(tmp) / "architecture" / "decisions" / "README.md",
              "# ADRs\n\n| ADR | Estado | Título |\n|-----|--------|--------|\n"
              "| [ADR-001](ADR-001-prueba.md) | Aceptado | Prueba |\n")
        ok &= expect("ADRs: README sin 4.ª columna", run("--root", tmp), 0, "OK ADRs")
    return ok


def test_invalid() -> bool:
    ok = True
    ok &= invalid("Sustituido sin «Sustituido por»",
                  [("001", "Sustituido", {})], "Sustituido sin «Sustituido por»")
    ok &= invalid("sustitución no recíproca",
                  [("001", "Sustituido", {"Sustituido por": "ADR-002"}), ("002", "Aceptado", {})],
                  "no declara «Sustituye» ADR-001")
    ok &= invalid("sucesor Propuesto en un Sustituido",
                  [("001", "Sustituido", {"Sustituido por": "ADR-002"}),
                   ("002", "Propuesto", {"Sustituye": "ADR-001"})],
                  "el sucesor debe estar Aceptado o Sustituido")
    ok &= invalid("Aceptado con «Sustituido por»",
                  [("001", "Aceptado", {"Sustituido por": "ADR-002"}), ("002", "Aceptado", {"Sustituye": "ADR-001"})],
                  "el estado debe ser Sustituido")
    ok &= invalid("Deprecado con «Sustituido por»",
                  [("001", "Deprecado", {"Sustituido por": "ADR-002"}), ("002", "Aceptado", {"Sustituye": "ADR-001"})],
                  "Deprecado con «Sustituido por»")
    ok &= invalid("Rechazado sin Rechazo",
                  [("001", "Rechazado", {})], "Rechazado sin fila Rechazo")
    ok &= invalid("Rechazado con Aceptación",
                  [("001", "Rechazado", {"Rechazo": "2026-09-02T10:00+02:00, no encaja.", "Aceptación": ACEPTACION})],
                  "Rechazado con fila Aceptación")
    ok &= invalid("Rechazo sin motivo",
                  [("001", "Rechazado", {"Rechazo": "2026-09-02T10:00+02:00"})], "Rechazo sin motivo")
    ok &= invalid("«Sustituye» a un ADR inexistente",
                  [("001", "Propuesto", {"Sustituye": "ADR-009"})], "ADR-009, que no existe")
    ok &= invalid("Sustituye de un Aceptado sin reciprocidad",
                  [("001", "Aceptado", {}), ("002", "Aceptado", {"Sustituye": "ADR-001"})],
                  "debe estar Sustituido por ADR-002")
    ok &= invalid("Excepción sin Caducidad",
                  [("001", "Aceptado", {"Tipo": "Excepción"})], "Tipo Excepción sin Caducidad")
    ok &= invalid("Caducidad sin Tipo",
                  [("001", "Aceptado", {"Caducidad": "2026-12-31T23:59+01:00"})], "Caducidad sin Tipo")
    ok &= invalid("Tipo distinto de Excepción",
                  [("001", "Aceptado", {"Tipo": "Normal"})], "Tipo «Normal» no es válido")
    ok &= invalid("Drivers vacío",
                  [("001", "Aceptado", {"Drivers": ""})], "Drivers vacío")
    ok &= invalid("README con 4.ª columna incoherente",
                  [("001", "Sustituido", {"Sustituido por": "ADR-002"}), ("002", "Aceptado", {"Sustituye": "ADR-001"})],
                  "README.md dice «—» en Sustituido por de ADR-001", columna={"001": "—"})
    ok &= invalid("README con sucesor donde no lo hay",
                  [("001", "Aceptado", {})], "README.md dice «ADR-002» en Sustituido por de ADR-001",
                  columna={"001": "ADR-002"})
    return ok


def consumer_invalid(label: str, adrs: list[Adr], needle: str, legacy_up_to: str = "0") -> bool:
    return invalid(f"consumidor: {label}", adrs, needle, args=(*CONSUMER, "--legacy-up-to", legacy_up_to))


def test_consumer_valid() -> bool:
    ok = expect("ADRs: consumidor, fixture de heredados",
                run("--consumer", "--legacy-up-to", "3", "--root", str(FIXTURE_HEREDADO)), 0, "OK ADRs (5)")
    # Sin índice no es un error: solo un AVISO que no cambia el código de salida.
    with tempfile.TemporaryDirectory() as tmp:
        adr_tree(Path(tmp), [("0001", "Aceptado", {})])
        (Path(tmp) / "architecture" / "decisions" / "README.md").unlink()
        proc = run("--root", tmp, *CONSUMER)
        ok &= expect("ADRs: consumidor sin README de índice", proc, 0, "AVISO ") and "OK ADRs (1)" in proc.stdout
    # Un índice sin columna Estado avisa y no compara el estado.
    with tempfile.TemporaryDirectory() as tmp:
        adr_tree(Path(tmp), [("0001", "Aceptado", {})])
        write(Path(tmp) / "architecture" / "decisions" / "README.md",
              "# ADRs\n\n| ADR | Título | Sustituido por |\n|---|---|---|\n| [ADR-0001](ADR-0001-prueba.md) | Prueba | — |\n")
        proc = run("--root", tmp, *CONSUMER)
        ok &= expect("ADRs: consumidor con índice sin columna Estado", proc, 0, "AVISO ") and "OK ADRs (1)" in proc.stdout
    # El BOM inicial se tolera.
    with tempfile.TemporaryDirectory() as tmp:
        adr_tree(Path(tmp), [("001", "Aceptado", {})])
        path = Path(tmp) / "architecture" / "decisions" / "ADR-001-prueba.md"
        write(path, "﻿" + path.read_text(encoding="utf-8"))
        ok &= expect("ADRs: consumidor con BOM", run("--root", tmp, *CONSUMER), 0, "OK ADRs (1)")
    return ok


def test_consumer_invalid() -> bool:
    ok = True
    # El modo core no cambia: el nombre de 4 dígitos sigue fuera del patrón.
    ok &= invalid("nombre de 4 dígitos sin --consumer", [("0001", "Aceptado", {})],
                  "nombre fuera de ADR-NNN-slug.md")
    ok &= consumer_invalid("heredado sin fecha con hora, sin --legacy-up-to",
                           [("0001", "Aceptado", {"Fecha": "2026-09-01", "Aceptación": None})],
                           "Fecha «2026-09-01» no es ISO 8601 con hora y zona")
    ok &= consumer_invalid("ADR nuevo con fecha sin hora",
                           [("0001", "Aceptado", {}), ("0002", "Aceptado", {"Fecha": "2026-09-01"})],
                           "ADR-0002-prueba.md: Fecha «2026-09-01» no es ISO 8601 con hora y zona", "1")
    ok &= consumer_invalid("ADR nuevo Aceptado sin Aceptación",
                           [("0001", "Aceptado", {}), ("0002", "Aceptado", {"Aceptación": None})],
                           "Aceptado sin fila Aceptación", "1")
    ok &= consumer_invalid("heredado Propuesto con Aceptación",
                           [("0001", "Propuesto", {"Aceptación": ACEPTACION})],
                           "Propuesto con fila Aceptación", "1")
    ok &= consumer_invalid("heredado con estado fuera de la tabla",
                           [("0001", "Aceptado (enmendado)", {"Aceptación": None})],
                           "Estado «Aceptado (enmendado)» no es uno de [", "1")
    ok &= consumer_invalid("número repetido tras normalizar",
                           [("001", "Aceptado", {}), ("0001", "Aceptado", {})],
                           "ADR-001 repetido: ADR-0001-prueba.md y ADR-001-prueba.md")
    ok &= consumer_invalid("heredado con Aceptación anterior a Fecha (por día)",
                           [("0001", "Aceptado", {"Fecha": "2026-09-02", "Aceptación": "2026-09-01T23:00+02:00, por Persona de prueba."})],
                           "Aceptación 2026-09-01T23:00+02:00 anterior a Fecha 2026-09-02", "1")
    ok &= consumer_invalid("sustitución no recíproca entre heredados",
                           [("0001", "Sustituido", {"Sustituido por": "ADR-0002", "Aceptación": None}),
                            ("0002", "Aceptado", {"Aceptación": None})],
                           "no declara «Sustituye» ADR-001", "2")
    ok &= consumer_invalid("excepción heredada con Caducidad sin hora",
                           [("0001", "Aceptado", {"Tipo": "Excepción", "Caducidad": "2026-12-31", "Aceptación": None})],
                           "Tipo Excepción sin Caducidad que empiece por fecha con hora y zona", "1")
    with tempfile.TemporaryDirectory() as tmp:
        adr_tree(Path(tmp), [("0001", "Aceptado", {})])
        write(Path(tmp) / "architecture" / "decisions" / "README.md",
              "# ADRs\n\n| ADR | Título | Fecha | Estado | Sustituido por |\n|---|---|---|---|---|\n"
              "| [ADR-0001](ADR-0001-prueba.md) | Prueba | 2026-09-01 | Deprecado | — |\n")
        ok &= expect("ADRs: consumidor, el índice nombra la columna Estado",
                     run("--root", tmp, *CONSUMER), 1,
                     "README.md dice «Deprecado» en la columna «Estado» (4.ª) para ADR-001; el ADR dice Aceptado")
        write(Path(tmp) / "architecture" / "decisions" / "README.md",
              "# ADRs\n\n| ADR | Estado | Título | Sustituido por |\n|---|---|---|---|\n"
              "| [ADR-0001](ADR-0001-prueba.md) | Aceptado | Prueba | — |\n"
              "| [ADR-0009](ADR-0009-prueba.md) | Aceptado | Prueba | — |\n")
        ok &= expect("ADRs: consumidor, el índice lista un ADR inexistente",
                     run("--root", tmp, *CONSUMER), 1, "README.md lista ADR-009, que no existe")
    # Los flags de heredados solo valen con --consumer; el valor debe ser un entero >= 0.
    for label, args in (("--legacy-up-to sin --consumer", ("--legacy-up-to", "3")),
                        ("--legacy-up-to negativo", ("--consumer", "--legacy-up-to", "-1")),
                        ("--legacy-up-to no entero", ("--consumer", "--legacy-up-to", "tres"))):
        ok &= expect(f"ADRs: {label}", run("--root", str(FIXTURE_HEREDADO), *args), 2)
    # Un fichero que no es UTF-8 se informa sin traceback y no oculta los demás.
    with tempfile.TemporaryDirectory() as tmp:
        adr_tree(Path(tmp), [("0001", "Aceptado", {}), ("0002", "Propuesto", {"Aceptación": ACEPTACION})])
        (Path(tmp) / "architecture" / "decisions" / "ADR-0001-prueba.md").write_bytes(
            adr_text("0001", "Aceptado", {}).replace("Prueba", "Pruebá").encode("cp1252"))
        proc = run("--root", tmp, *CONSUMER)
        ok &= expect("ADRs: consumidor con fichero en cp1252", proc, 1, "FAIL ADR-0001-prueba.md: no es UTF-8")
        ok &= expect("ADRs: el FAIL de codificación no oculta los demás", proc, 1, "Propuesto con fila Aceptación")
        if "Traceback" in proc.stderr:
            print("FAIL ADRs: consumidor con fichero en cp1252: traceback")
            ok = False
    return ok


def expect_value(label: str, got: Any, want: Any) -> bool:
    if got != want:
        print(f"FAIL {label}: se obtuvo {got!r} (se esperaba {want!r})")
        return False
    print(f"OK {label}")
    return True


def test_adr_index() -> bool:
    """`adr_index` (movida desde check-gate0) lee el Estado crudo del fichero, con 3 o 4 dígitos."""
    ok = expect_value("adr_index: fixture del ciclo de vida",
                      sdaf_adrs.adr_index(FIXTURE),
                      {1: ("ADR-001-aceptado.md", "Aceptado"), 2: ("ADR-002-sustituido.md", "Sustituido"),
                       3: ("ADR-003-sucesor.md", "Aceptado"), 4: ("ADR-004-rechazado.md", "Rechazado"),
                       5: ("ADR-005-deprecado.md", "Deprecado"), 6: ("ADR-006-excepcion.md", "Aceptado")})
    ok &= expect_value("adr_index: fixture heredado, estado crudo y 4 dígitos",
                       sdaf_adrs.adr_index(FIXTURE_HEREDADO),
                       {1: ("ADR-0001-primera-decision.md", "Accepted"), 2: ("ADR-0002-segunda-decision.md", "Superseded"),
                        3: ("ADR-0003-tercera-decision.md", "Deprecated"), 5: ("ADR-0005-quinta-decision.md", "Aceptado"),
                        6: ("ADR-0006-sexta-decision.md", "Propuesto")})
    with tempfile.TemporaryDirectory() as tmp:
        ok &= expect_value("adr_index: sin carpeta de ADRs", sdaf_adrs.adr_index(Path(tmp)), {})
        folder = Path(tmp) / "architecture" / "decisions"
        write(folder / "ADR-001-uno.md", adr_text("001", "Aceptado", {}))
        write(folder / "ADR-0001-repetido.md", adr_text("0001", "Rechazado", {}))
        write(folder / "ADR-12345-largo.md", adr_text("123", "Aceptado", {}))
        write(folder / "ADR-002-Mayusculas.md", adr_text("002", "Aceptado", {}))
        write(folder / "README.md", "# ADRs\n")
        (folder / "ADR-003-ilegible.md").write_bytes(adr_text("003", "Aceptado", {}).replace("Prueba", "Pruebá").encode("cp1252"))
        ok &= expect_value("adr_index: ADR-001 y ADR-0001 chocan (gana el primero), nombres ajenos fuera, ilegible sin Estado",
                           sdaf_adrs.adr_index(Path(tmp)),
                           {1: ("ADR-0001-repetido.md", "Rechazado"), 3: ("ADR-003-ilegible.md", None)})
    return ok


def vigencia_tree(root: Path, adrs: list[tuple[str, str, dict[str, str | None]]]) -> None:
    for num, estado, extra in adrs:
        write(root / "architecture" / "decisions" / f"ADR-{num}-prueba.md", adr_text(num, estado, extra))


def test_adr_vigencia() -> bool:
    ok = expect_value("adr_vigencia: fixture del ciclo de vida",
                      sdaf_adrs.adr_vigencia(FIXTURE),
                      {1: ("ADR-001-aceptado.md", "Aceptado", [], True, True),
                       2: ("ADR-002-sustituido.md", "Sustituido", [3], True, False),
                       3: ("ADR-003-sucesor.md", "Aceptado", [], True, True),
                       4: ("ADR-004-rechazado.md", "Rechazado", [], True, False),
                       5: ("ADR-005-deprecado.md", "Deprecado", [], True, False),
                       6: ("ADR-006-excepcion.md", "Aceptado", [], True, True)})
    ok &= expect_value("adr_vigencia: fixture heredado (Accepted/Superseded/Deprecated → canónico)",
                       sdaf_adrs.adr_vigencia(FIXTURE_HEREDADO),
                       {1: ("ADR-0001-primera-decision.md", "Aceptado", [], True, True),
                        2: ("ADR-0002-segunda-decision.md", "Sustituido", [5], True, False),
                        3: ("ADR-0003-tercera-decision.md", "Deprecado", [], True, False),
                        5: ("ADR-0005-quinta-decision.md", "Aceptado", [], True, True),
                        6: ("ADR-0006-sexta-decision.md", "Propuesto", [], True, False)})
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        ok &= expect_value("adr_vigencia: sin carpeta de ADRs", sdaf_adrs.adr_vigencia(root), {})
        vigencia_tree(root, [
            ("001", "Aceptado", {"Sustituido por": "[ADR-002](ADR-002-prueba.md)"}),  # incoherente, pero no vigente
            ("002", "Aceptado", {"Sustituido por": "—"}),
            ("003", "Aceptado", {"Sustituido por": "-"}),
            ("004", "Aceptado", {"Sustituido por": "N/A"}),
            ("005", "Propuesto", {"Aceptación": None}),
            ("006", "Aceptado", {"Tipo": "Excepción", "Caducidad": "2020-01-01T00:00+01:00"}),
        ])
        vigencia_tree(root, [("0007", "accepted", {}), ("0008", "SUPERSEDED", {"Sustituido por": "ADR-0009"}),
                             ("0009", "Rechazada", {"Aceptación": None})])
        (root / "architecture" / "decisions" / "ADR-010-ilegible.md").write_bytes(
            adr_text("010", "Aceptado", {}).replace("Prueba", "Pruebá").encode("cp1252"))
        got = sdaf_adrs.adr_vigencia(root)
        ok &= expect_value("adr_vigencia: Aceptado con «Sustituido por» no es vigente",
                           got[1], ("ADR-001-prueba.md", "Aceptado", [2], True, False))
        ok &= expect_value("adr_vigencia: «—», «-» y «N/A» en «Sustituido por» = ninguno",
                           [got[n] for n in (2, 3, 4)],
                           [(f"ADR-00{n}-prueba.md", "Aceptado", [], True, True) for n in (2, 3, 4)])
        ok &= expect_value("adr_vigencia: Propuesto no es vigente", got[5], ("ADR-005-prueba.md", "Propuesto", [], True, False))
        ok &= expect_value("adr_vigencia: la excepción Aceptada sigue vigente mientras no se depreque",
                           got[6], ("ADR-006-prueba.md", "Aceptado", [], True, True))
        ok &= expect_value("adr_vigencia: estado heredado «accepted» (4 dígitos) es Aceptado",
                           got[7], ("ADR-0007-prueba.md", "Aceptado", [], True, True))
        ok &= expect_value("adr_vigencia: «SUPERSEDED» con «Sustituido por» no es vigente",
                           got[8], ("ADR-0008-prueba.md", "Sustituido", [9], True, False))
        ok &= expect_value("adr_vigencia: estado heredado «Rechazada» = Rechazado, no vigente",
                           got[9], ("ADR-0009-prueba.md", "Rechazado", [], True, False))
        ok &= expect_value("adr_vigencia: ADR no UTF-8 = ilegible sin excepción",
                           got[10], ("ADR-010-ilegible.md", None, [], False, False))
        write(root / "architecture" / "decisions" / "ADR-011-raro.md", adr_text("011", "Estado inventado", {}))
        ok &= expect_value("adr_vigencia: estado fuera de la tabla = None y no vigente",
                           sdaf_adrs.adr_vigencia(root)[11], ("ADR-011-raro.md", None, [], True, False))
    return ok


def main() -> int:
    results = [test_fixture(), test_valid_variants(), test_invalid(), test_consumer_valid(), test_consumer_invalid(),
               test_adr_index(), test_adr_vigencia()]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
