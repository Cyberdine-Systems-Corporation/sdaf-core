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

ROOT = Path(__file__).resolve().parents[1]
ADRS = ROOT / "scripts" / "check-adrs.py"
FIXTURE = ROOT / "scripts" / "testdata" / "adrs-ciclo-valido"

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


def invalid(label: str, adrs: list[Adr], needle: str, columna: dict[str, str] | None = None) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        adr_tree(Path(tmp), adrs, columna)
        return expect(f"ADRs: {label}", run("--root", tmp), 1, needle)


def valid(label: str, adrs: list[Adr], columna: dict[str, str] | None = None) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        adr_tree(Path(tmp), adrs, columna)
        return expect(f"ADRs: {label}", run("--root", tmp), 0, "OK ADRs")


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


def main() -> int:
    results = [test_fixture(), test_valid_variants(), test_invalid()]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
