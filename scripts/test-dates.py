#!/usr/bin/env python3
"""Autocomprobación de los checkers de fechas (H13 §9) y de ADRs.

Crea árboles temporales, incluido un repo git para el historial, y comprueba
que cada checker sale 0 en el caso válido y 1, con el mensaje esperado, en
cada caso inválido.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "scripts" / "check-version-metadata.py"
HIST = ROOT / "scripts" / "check-history-append-only.py"
ADRS = ROOT / "scripts" / "check-adrs.py"


def run(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def agent(version: str, fecha: str, rows: list[tuple[str, str]]) -> str:
    body = "\n".join(f"| {v} | {f} | cambio {v} |" for v, f in rows)
    return (
        "# Agente de prueba\n\n| Campo | Valor |\n|--------|--------|\n"
        f"| Versión | {version} |\n| Fecha | {fecha} |\n\n"
        "## Historial\n\n| Versión | Fecha | Cambio |\n|---------|--------|--------|\n"
        f"{body}\n"
    )


def expect(label: str, proc: subprocess.CompletedProcess[str], code: int, needle: str = "") -> bool:
    if proc.returncode != code or (needle and needle not in proc.stdout):
        print(f"FAIL {label}: exit {proc.returncode} (se esperaba {code}), falta «{needle}»")
        print(proc.stdout + proc.stderr)
        return False
    print(f"OK {label}")
    return True


def test_metadata() -> bool:
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        target = root / "agents" / "x-agent.md"
        write(target, agent("0.2.0", "2026-09-24T10:00+02:00",
                            [("0.2.0", "2026-09-24T10:00+02:00"), ("0.1.0", "2026-09-01")]))
        ok &= expect("metadatos: cabecera = fila más reciente", run(META, "--root", tmp), 0)
        write(target, agent("0.2.0", "24/09/2026", [("0.2.0", "24/09/2026")]))
        ok &= expect("metadatos: fecha fuera de ISO 8601", run(META, "--root", tmp), 1, "ISO 8601")
        write(target, agent("0.2.0", "2026-09-01",
                            [("0.2.0", "2026-09-24T10:00+02:00"), ("0.1.0", "2026-09-01")]))
        ok &= expect("metadatos: cabecera ≠ fila más reciente", run(META, "--root", tmp), 1, "fila más reciente")
        target.unlink()
        write(root / "handbook" / "99-prueba.md", "# 99 — Prueba\n")
        write(root / "handbook" / "_meta" / "99-prueba.yaml",
              'archivo: 99-prueba.md\nversion: 0.2.0\nfecha: "2026-09-24T10:00+02:00"\n'
              'historial:\n  - version: 0.2.0\n    fecha: "2026-09-24T10:00+02:00"\n    cambio: prueba\n')
        ok &= expect("metadatos: sidecar con hora", run(META, "--root", tmp), 0)
    return ok


def git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid", *args],
        cwd=root, check=True, capture_output=True,
    )


def test_history() -> bool:
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        git(root, "init", "-q")
        write(root / "agents" / "a-agent.md", agent("0.1.0", "2026-09-01", [("0.1.0", "2026-09-01")]))
        # Publicado con versión y sin historial (caso de las filas iniciales).
        write(root / "agents" / "b-agent.md",
              "# B\n\n| Campo | Valor |\n|--------|--------|\n| Versión | 0.1.0 |\n| Fecha | 2026-09-01 |\n")
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "base")

        a = root / "agents" / "a-agent.md"
        write(a, agent("0.2.0", "2026-09-24", [("0.2.0", "2026-09-24"), ("0.1.0", "2026-09-01")]))
        ok &= expect("historial: versión nueva sin hora", run(HIST, "--root", tmp, "--base", "HEAD"), 1, "no lleva hora")
        write(a, agent("0.2.0", "2026-09-24T10:00+02:00",
                       [("0.2.0", "2026-09-24T10:00+02:00"), ("0.1.0", "2026-09-01")]))
        ok &= expect("historial: versión nueva con hora", run(HIST, "--root", tmp, "--base", "HEAD"), 0)
        write(root / "agents" / "b-agent.md", agent("0.1.0", "2026-09-01", [("0.1.0", "2026-09-01")]))
        ok &= expect("historial: fila inicial de versión publicada con día", run(HIST, "--root", tmp, "--base", "HEAD"), 0)
        write(a, agent("0.2.0", "2026-09-24T10:00+02:00", [("0.2.0", "2026-09-24T10:00+02:00")]))
        ok &= expect("historial: fila publicada borrada", run(HIST, "--root", tmp, "--base", "HEAD"), 1, "falta la fila")
    return ok


def adr(num: str, estado: str, fecha: str, aceptacion: str | None, titulo_num: str | None = None) -> str:
    extra = f"| Aceptación | {aceptacion}, por Persona de prueba. |\n" if aceptacion else ""
    return (
        f"# ADR-{titulo_num or num} — Prueba\n\n| Campo | Valor |\n|--------|--------|\n"
        f"| Estado | {estado} |\n| Fecha | {fecha} |\n{extra}\n## Decisión\n\nPrueba.\n"
    )


def adr_tree(root: Path, adrs: dict[str, str], index: dict[str, str]) -> None:
    folder = root / "architecture" / "decisions"
    for old in folder.glob("*.md") if folder.is_dir() else []:
        old.unlink()
    for name, text in adrs.items():
        write(folder / name, text)
    rows = "\n".join(f"| [ADR-{n}](ADR-{n}-prueba.md) | {e} | Prueba |" for n, e in index.items())
    write(folder / "README.md", f"# ADRs\n\n| ADR | Estado | Título |\n|-----|--------|--------|\n{rows}\n")


def test_adrs() -> bool:
    ok = True
    good = adr("001", "Aceptado", "2026-09-23T15:32+02:00", "2026-09-24T18:21+02:00")
    prop = adr("002", "Propuesto", "2026-09-24T10:00+02:00", None)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        adr_tree(root, {"ADR-001-prueba.md": good, "ADR-002-prueba.md": prop}, {"001": "Aceptado", "002": "Propuesto"})
        ok &= expect("ADRs: válidos", run(ADRS, "--root", tmp), 0)
        adr_tree(root, {"ADR-001-prueba.md": adr("001", "Aceptado", "2026-09-23", "2026-09-24T18:21+02:00")},
                 {"001": "Aceptado"})
        ok &= expect("ADRs: Fecha sin hora", run(ADRS, "--root", tmp), 1, "hora y zona")
        adr_tree(root, {"ADR-001-prueba.md": adr("001", "Aceptado", "2026-09-23T15:32+02:00", None)},
                 {"001": "Aceptado"})
        ok &= expect("ADRs: Aceptado sin Aceptación", run(ADRS, "--root", tmp), 1, "sin fila Aceptación")
        adr_tree(root, {"ADR-001-prueba.md": adr("001", "Aceptado", "2026-09-24T18:21+02:00", "2026-09-23T15:32+02:00")},
                 {"001": "Aceptado"})
        ok &= expect("ADRs: Aceptación anterior a Fecha", run(ADRS, "--root", tmp), 1, "anterior a Fecha")
        adr_tree(root, {"ADR-001-prueba.md": adr("001", "Propuesto", "2026-09-24T10:00+02:00", "2026-09-24T11:00+02:00")},
                 {"001": "Propuesto"})
        ok &= expect("ADRs: Propuesto con Aceptación", run(ADRS, "--root", tmp), 1, "Propuesto con fila Aceptación")
        adr_tree(root, {"ADR-001-prueba.md": adr("001", "Aceptado", "2026-09-23T15:32+02:00",
                                                   "2026-09-24T18:21+02:00", titulo_num="008")},
                 {"001": "Aceptado"})
        ok &= expect("ADRs: título ≠ número de fichero", run(ADRS, "--root", tmp), 1, "el título dice ADR-008")
        adr_tree(root, {"ADR-001-prueba.md": good, "ADR-003-prueba.md": adr("003", "Propuesto", "2026-09-24T10:00+02:00", None)},
                 {"001": "Aceptado", "003": "Propuesto"})
        ok &= expect("ADRs: numeración con huecos", run(ADRS, "--root", tmp), 1, "huecos")
        adr_tree(root, {"ADR-001-prueba.md": good}, {"001": "Propuesto"})
        ok &= expect("ADRs: README con estado distinto", run(ADRS, "--root", tmp), 1, "README.md dice Propuesto")
    return ok


def main() -> int:
    results = [test_metadata(), test_history(), test_adrs()]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
