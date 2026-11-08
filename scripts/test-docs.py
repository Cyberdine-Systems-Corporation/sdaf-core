#!/usr/bin/env python3
"""Autocomprobación de la lectura de documentos (sdaf_docs.py).

Ejercita la API pura de sdaf_docs.py con textos en memoria, con las plantillas
reales del repo y con árboles temporales, e imprime OK/FAIL por comprobación.
Sale 0 si todas pasan y 1 si alguna falla.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import sdaf_docs  # noqa: E402

TEMPLATES = ROOT / "templates"
PBI_TEMPLATE = (TEMPLATES / "pbi.md").read_text(encoding="utf-8")
SPEC_TEMPLATE = (TEMPLATES / "spec.md").read_text(encoding="utf-8")
DESCRIPTION_TEMPLATE = (TEMPLATES / "architecture-description.md").read_text(encoding="utf-8")


def expect(label: str, got: Any, want: Any) -> bool:
    if got != want:
        print(f"FAIL {label}: se obtuvo {got!r} (se esperaba {want!r})")
        return False
    print(f"OK {label}")
    return True


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def doc(doc_id: str | None, estado: str = "Approved", extra: str = "") -> str:
    """Documento mínimo con cabecera `Campo | Valor`; sin `doc_id` no lleva fila ID."""
    rows = ([f"| ID | {doc_id} |"] if doc_id else []) + [f"| Estado | {estado} |"]
    return "# Prueba\n\n| Campo | Valor |\n|--------|--------|\n" + "\n".join(rows) + "\n" + extra


def test_read() -> bool:
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        write(base / "a.md", "# Año\n")
        (base / "bom.md").write_bytes("﻿# Con BOM\n".encode("utf-8"))
        (base / "latin.md").write_bytes("# Año\n".encode("latin-1"))
        ok &= expect("read: fichero UTF-8", sdaf_docs.read(base / "a.md"), "# Año\n")
        ok &= expect("read: BOM tolerado", sdaf_docs.read(base / "bom.md"), "# Con BOM\n")
        ok &= expect("read: latin-1 no decodifica", sdaf_docs.read(base / "latin.md"), None)
        ok &= expect("read: fichero inexistente", sdaf_docs.read(base / "no.md"), None)
    return ok


def test_header_fields() -> bool:
    ok = True
    pbi = sdaf_docs.header_fields(PBI_TEMPLATE)
    ok &= expect("header_fields: plantilla de PBI, campos",
                 list(pbi), ["ID", "Versión", "Estado", "Fecha", "Specs", "Acceptance",
                             "Unidades", "ADRs", "Worklogs"])
    ok &= expect("header_fields: plantilla de PBI, valores",
                 (pbi["ID"], pbi["Estado"], pbi["Specs"]), ("PBI-XXX-000", "Draft", "SPEC-XXX-000 (Approved)"))
    ok &= expect("header_fields: plantilla de spec, fila vacía y ADRs relacionados",
                 (sdaf_docs.header_fields(SPEC_TEMPLATE)["Fuentes"],
                  "ADRs relacionados" in sdaf_docs.header_fields(SPEC_TEMPLATE)), ("", True))
    ok &= expect("header_fields: ignora una segunda tabla con fila ID",
                 sdaf_docs.header_fields(doc("SPEC-001", extra="\n| Campo | Valor |\n|---|---|\n| ID | OTRO |\n")
                                         + "\n| ID | Estado |\n|---|---|\n| X | Y |\n")["ID"], "SPEC-001")
    ok &= expect("header_fields: ignora tablas anteriores a la de campos",
                 sdaf_docs.header_fields("# T\n\n| ID | Nombre |\n|---|---|\n| A | B |\n\n"
                                         "| Campo | Valor |\n|---|---|\n| ID | SPEC-002 |\n"),
                 {"ID": "SPEC-002"})
    ok &= expect("header_fields: clave repetida, gana la primera",
                 sdaf_docs.header_fields("# T\n\n| Campo | Valor |\n|---|---|\n| ID | A |\n| ID | B |\n"),
                 {"ID": "A"})
    ok &= expect("header_fields: sin asteriscos ni espacios sobrantes",
                 sdaf_docs.header_fields("# T\n\n| Campo | Valor |\n|---|---|\n| **ID**  |   SPEC-003   |\n"),
                 {"ID": "SPEC-003"})
    ok &= expect("header_fields: sin tabla de campos", sdaf_docs.header_fields("# T\n\nSolo texto.\n"), {})
    return ok


def test_section() -> bool:
    ok = True
    text = ("# T\n\n## 1. Contexto\n\nUno.\n\n### Detalle\n\nDos.\n\n## 2. Unidades\n\n"
            "| A | B |\n|---|---|\n| x | y |\n\n## 3. Final\n\nTres.\n")
    ok &= expect("section: cuerpo hasta el siguiente «## » (los «###» siguen dentro)",
                 sdaf_docs.section(text, r"Contexto").strip(), "Uno.\n\n### Detalle\n\nDos.")
    ok &= expect("section: la regex casa con el título completo",
                 sdaf_docs.section(text, r"Unidades\s*$").startswith("\n| A | B |"), True)
    ok &= expect("section: última sección hasta el final", sdaf_docs.section(text, r"Final").strip(), "Tres.")
    ok &= expect("section: inexistente", sdaf_docs.section(text, r"Riesgos"), "")
    return ok


def test_table_rows() -> bool:
    ok = True
    block = "Texto previo.\n\n| Unidad | Tipo | Responsabilidad |\n|---|:-:|---|\n| Unidad A |  Tipo libre | Hace x |\n| Unidad B | | |\n\nFin.\n"
    ok &= expect("table_rows: filas de datos, celdas recortadas y vacías",
                 sdaf_docs.table_rows(block), [["Unidad A", "Tipo libre", "Hace x"], ["Unidad B", "", ""]])
    ok &= expect("table_rows: solo la primera tabla",
                 sdaf_docs.table_rows("| A |\n|---|\n| 1 |\n\n| B |\n|---|\n| 2 |\n"), [["1"]])
    ok &= expect("table_rows: sin tabla", sdaf_docs.table_rows("Solo texto.\n"), [])
    ok &= expect("table_rows: tabla de la plantilla de descripción",
                 sdaf_docs.table_rows(sdaf_docs.section(DESCRIPTION_TEMPLATE, r"Unidades\s*$"))[0][0], "Unidad A")
    return ok


def test_split_list() -> bool:
    ok = True
    ok &= expect("split_list: coma y «;»", sdaf_docs.split_list("Unidad A, Unidad B; Unidad C"),
                 ["Unidad A", "Unidad B", "Unidad C"])
    ok &= expect("split_list: backticks", sdaf_docs.split_list("`worklogs/a/Iteration-001.md`, `b.md`"),
                 ["worklogs/a/Iteration-001.md", "b.md"])
    ok &= expect("split_list: paréntesis finales y vacíos",
                 sdaf_docs.split_list("SPEC-PRD-001 (Approved), , SPEC-PRD-002 (Approved, v2);"),
                 ["SPEC-PRD-001", "SPEC-PRD-002"])
    ok &= expect("split_list: valor vacío", sdaf_docs.split_list("  "), [])
    return ok


def test_is_placeholder() -> bool:
    ok = True
    pbi = sdaf_docs.header_fields(PBI_TEMPLATE)
    spec = sdaf_docs.header_fields(SPEC_TEMPLATE)
    ok &= expect("is_placeholder: valores de la plantilla de PBI",
                 [sdaf_docs.is_placeholder(pbi[k]) for k in ("ID", "Fecha", "Specs", "Acceptance", "Unidades", "ADRs", "Worklogs")],
                 [True] * 7)
    ok &= expect("is_placeholder: valores de la plantilla de spec",
                 [sdaf_docs.is_placeholder(spec[k]) for k in ("ID", "Fecha", "Fuentes", "PBIs / backlog", "Unidades")],
                 [True] * 5)
    ok &= expect("is_placeholder: vacío y puntos suspensivos",
                 [sdaf_docs.is_placeholder(v) for v in ("", "   ", "…")], [True] * 3)
    ok &= expect("is_placeholder: valores rellenos",
                 [sdaf_docs.is_placeholder(v) for v in ("PBI-PRD-001", "2026-10-24T10:00+02:00",
                                                        "`worklogs/a/Iteration-001.md`", "N/A: sin impacto")],
                 [False] * 4)
    ok &= expect("is_placeholder: nombres neutros de unidad",
                 [sdaf_docs.is_placeholder(v) for v in ("Unidad A", "Unidad A, Unidad B", "Persona de prueba")],
                 [False] * 3)
    return ok


def test_frontmatter() -> bool:
    ok = True
    ok &= expect("frontmatter: bloque válido",
                 sdaf_docs.frontmatter("---\nestado: abortado\npbi: PBI-001\n---\n# Cuerpo\n"),
                 {"estado": "abortado", "pbi": "PBI-001"})
    ok &= expect("frontmatter: sin bloque", sdaf_docs.frontmatter("# Cuerpo\n---\na: 1\n---\n"), None)
    ok &= expect("frontmatter: YAML roto", sdaf_docs.frontmatter("---\na: [sin cerrar\n---\n"), None)
    ok &= expect("frontmatter: no es un mapa", sdaf_docs.frontmatter("---\n- uno\n- dos\n---\n"), None)
    ok &= expect("frontmatter: bloque sin cerrar", sdaf_docs.frontmatter("---\na: 1\n# Cuerpo\n"), None)
    return ok


def test_indexes() -> bool:
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        write(base / "specs" / "product" / "SPEC-001.md", doc("SPEC-001"))
        write(base / "specs" / "product" / "SPEC-002.md", doc("SPEC-002", "Draft"))
        write(base / "specs" / "acceptance" / "otro.md", doc("SPEC-002"))
        write(base / "specs" / "sin-id.md", doc(None))
        (base / "specs" / "latin.md").write_bytes(doc("SPEC-009").replace("Prueba", "Año").encode("latin-1"))
        write(base / "backlog" / "PBI-001.md", doc("PBI-001", "Draft"))
        write(base / "backlog" / "nested" / "PBI-002.md", doc("PBI-002", "Draft"))
        specs = sdaf_docs.spec_index(base)
        pbis = sdaf_docs.find_pbis(base)
        ok &= expect("spec_index: IDs leídos, sin ID ni ilegibles", sorted(specs), ["SPEC-001", "SPEC-002"])
        ok &= expect("spec_index: ID duplicado lista ambas rutas",
                     sorted(p.name for p in specs["SPEC-002"]), ["SPEC-002.md", "otro.md"])
        ok &= expect("spec_index: ruta única", [p.name for p in specs["SPEC-001"]], ["SPEC-001.md"])
        ok &= expect("find_pbis: recorre backlog en profundidad", sorted(pbis), ["PBI-001", "PBI-002"])
        ok &= expect("find_pbis: no mira specs/",
                     "SPEC-001" in pbis, False)
    with tempfile.TemporaryDirectory() as tmp:
        ok &= expect("spec_index y find_pbis: raíz sin carpetas",
                     (sdaf_docs.spec_index(Path(tmp)), sdaf_docs.find_pbis(Path(tmp))), ({}, {}))
    return ok


def description(estado: str, units: str) -> str:
    return f"# Descripción de arquitectura\n\n| Campo | Valor |\n|---|---|\n| Estado | {estado} |\n\n## 2. Unidades\n\n{units}\n\n## 3. Reglas\n\nTexto.\n"


TABLE = ("| Unidad | Tipo | Responsabilidad |\n|---|---|---|\n"
         "| Unidad A | Tipo libre | Hace x |\n| Unidad B | Tipo libre | Módulo heredada del sistema anterior |\n")


def test_baseline() -> bool:
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        target = base / "architecture" / "description.md"
        ok &= expect("baseline: ausente", sdaf_docs.baseline(base), None)
        write(target, description("Approved", TABLE))
        ok &= expect("baseline: Approved con dos unidades y una heredada",
                     sdaf_docs.baseline(base), ("Approved", ["Unidad A", "Unidad B"], ["Unidad B"]))
        write(target, description("Draft", TABLE.replace("heredada", "HEREDADA")))
        ok &= expect("baseline: Draft, «heredada» sin distinguir mayúsculas",
                     sdaf_docs.baseline(base), ("Draft", ["Unidad A", "Unidad B"], ["Unidad B"]))
        write(target, description("Approved", "`N/A: sin unidades`"))
        ok &= expect("baseline: unidades N/A", sdaf_docs.baseline(base), ("Approved", [], []))
        write(target, DESCRIPTION_TEMPLATE)
        ok &= expect("baseline: plantilla sin rellenar", sdaf_docs.baseline(base), ("Draft", [], []))
        write(target, "# Sin cabecera\n\n## 2. Unidades\n\n" + TABLE)
        ok &= expect("baseline: sin campo Estado",
                     sdaf_docs.baseline(base), (None, ["Unidad A", "Unidad B"], ["Unidad B"]))
        target.write_bytes(description("Approved", TABLE).replace("Hace", "Hacé").encode("latin-1"))
        ok &= expect("baseline: fichero ilegible", sdaf_docs.baseline(base), None)
    return ok


def description_adrs(decisiones: str | None) -> str:
    """Línea base con la sección 6; sin `decisiones` la sección no existe."""
    sec = "" if decisiones is None else f"## 6. Decisiones vigentes\n\nIntro.\n\n{decisiones}\n\n"
    return (f"# Descripción de arquitectura\n\n| Campo | Valor |\n|---|---|\n| Estado | Approved |\n\n"
            f"## 2. Unidades\n\n{TABLE}\n## 5. Calidad\n\nTexto.\n\n{sec}## 7. Riesgos\n\nTexto.\n")


ADR_TABLE = ("| ADR | Decisión | Unidades afectadas |\n|-----|----------|--------------------|\n"
             "| ADR-004 | Una frase | Unidad A |\n| [ADR-002](ADR-002-x.md) | Otra | Unidad A, Unidad B |\n"
             "|  |  |  |")


def test_baseline_adrs() -> bool:
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        target = base / "architecture" / "description.md"
        ok &= expect("baseline_adrs: fichero ausente", sdaf_docs.baseline_adrs(base), None)
        write(target, description_adrs(ADR_TABLE))
        ok &= expect("baseline_adrs: varias filas, ordenadas, enlace y fila vacía",
                     sdaf_docs.baseline_adrs(base), (True, False, [2, 4]))
        write(target, description_adrs(ADR_TABLE + "\n| ADR-NNN | Una frase | Unidad A |"))
        ok &= expect("baseline_adrs: la fila de plantilla ADR-NNN se ignora",
                     sdaf_docs.baseline_adrs(base), (True, False, [2, 4]))
        write(target, description_adrs("| ADR | Decisión |\n|---|---|\n| ADR-0001 | a |\n| ADR-001 | repetida |\n| ADR-0012 | b |"))
        ok &= expect("baseline_adrs: ADR-001 y ADR-0001 son el mismo y no se repite",
                     sdaf_docs.baseline_adrs(base), (True, False, [1, 12]))
        write(target, description_adrs("| Decisión | ADR |\n|---|---|\n| Una frase | ADR-007 |"))
        ok &= expect("baseline_adrs: la columna ADR se localiza por la cabecera",
                     sdaf_docs.baseline_adrs(base), (True, False, [7]))
        write(target, description_adrs("`N/A: sin decisiones todavía`"))
        ok &= expect("baseline_adrs: sección N/A sin tabla", sdaf_docs.baseline_adrs(base), (True, True, []))
        write(target, description_adrs(None))
        ok &= expect("baseline_adrs: sin sección 6", sdaf_docs.baseline_adrs(base), (False, False, []))
        write(target, DESCRIPTION_TEMPLATE)
        ok &= expect("baseline_adrs: plantilla sin rellenar (solo filas ADR-NNN)",
                     sdaf_docs.baseline_adrs(base), (True, False, []))
        target.write_bytes(description_adrs(ADR_TABLE).replace("Intro", "Introducción é").encode("latin-1"))
        ok &= expect("baseline_adrs: fichero no UTF-8", sdaf_docs.baseline_adrs(base), None)
    return ok


def spec_doc(doc_id: str, unidades: str | None) -> str:
    row = "" if unidades is None else f"| Unidades | {unidades} |\n"
    return f"# Spec\n\n| Campo | Valor |\n|---|---|\n| ID | {doc_id} |\n| Estado | Approved |\n{row}\n## Contexto\n\nTexto.\n"


def test_spec_units() -> bool:
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        ok &= expect("spec_units: sin carpeta specs", sdaf_docs.spec_units(base), [])
        write(base / "specs" / "product" / "SPEC-B.md", spec_doc("SPEC-B", "Unidad A, `Unidad B` (nueva)"))
        write(base / "specs" / "SPEC-A.md", spec_doc("SPEC-A", "Unidad A"))
        write(base / "specs" / "acceptance" / "deep" / "SPEC-C.md", spec_doc("SPEC-C", "Unidad B; Unidad C"))
        write(base / "specs" / "SPEC-D.md", spec_doc("SPEC-D", "Unidad A, <nombre de la unidad>"))
        write(base / "specs" / "SPEC-E.md", spec_doc("SPEC-E", "Unidad A, XXX, …"))
        write(base / "specs" / "SPEC-F.md", spec_doc("SPEC-F", None))
        write(base / "specs" / "README.md", "# Índice\n\nSin cabecera.\n")
        write(base / "specs" / "notas.txt", "no es markdown")
        ok &= expect("spec_units: varios niveles, orden por ruta, placeholders y campo ausente",
                     sdaf_docs.spec_units(base),
                     [("SPEC-A", "specs/SPEC-A.md", ["Unidad A"], True),
                      ("SPEC-D", "specs/SPEC-D.md", ["Unidad A"], True),
                      ("SPEC-E", "specs/SPEC-E.md", ["Unidad A"], True),
                      ("SPEC-F", "specs/SPEC-F.md", None, True),
                      ("SPEC-C", "specs/acceptance/deep/SPEC-C.md", ["Unidad B", "Unidad C"], True),
                      ("SPEC-B", "specs/product/SPEC-B.md", ["Unidad A", "Unidad B"], True)])
        write(base / "specs" / "SPEC-G.md", spec_doc("SPEC-G", "…"))
        ok &= expect("spec_units: campo solo con placeholders = lista vacía, no None",
                     [r for r in sdaf_docs.spec_units(base) if r[0] == "SPEC-G"],
                     [("SPEC-G", "specs/SPEC-G.md", [], True)])
        (base / "specs" / "SPEC-H.md").write_bytes(spec_doc("SPEC-H", "Unidad A").replace("Texto", "Textó").encode("latin-1"))
        ok &= expect("spec_units: un .md no UTF-8 se marca ilegible y no oculta los demás",
                     [r for r in sdaf_docs.spec_units(base) if r.path == "specs/SPEC-H.md"],
                     [(None, "specs/SPEC-H.md", None, False)])
        ok &= expect("spec_units: spec_index no cambia (README y SPEC-H fuera)",
                     sorted(sdaf_docs.spec_index(base)), ["SPEC-A", "SPEC-B", "SPEC-C", "SPEC-D", "SPEC-E", "SPEC-F", "SPEC-G"])
    return ok


def main() -> int:
    results = [test_read(), test_header_fields(), test_section(), test_table_rows(), test_split_list(),
               test_is_placeholder(), test_frontmatter(), test_indexes(), test_baseline(),
               test_baseline_adrs(), test_spec_units()]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
