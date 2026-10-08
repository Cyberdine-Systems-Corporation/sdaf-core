#!/usr/bin/env python3
"""Comprueba los ADRs del core en architecture/decisions/ (ADR-006).

- Numeración: ADR-001, ADR-002… sin huecos ni repetidos; el título coincide
  con el número del fichero (ADR-001, H13 §8).
- Estado: Propuesto, Aceptado, Rechazado, Sustituido o Deprecado
  (templates/adr.md).
- Fecha: ISO 8601 con hora y zona (H13 §9); todos los ADRs del core son de la
  línea 0.4.0 o posteriores.
- Aceptación (fecha con hora y zona al inicio, no anterior a Fecha):
  obligatoria en Aceptado y Sustituido, opcional en Deprecado y prohibida en
  Propuesto y Rechazado: un agente no la escribe (H00 §3.3).
- Rechazo: obligatorio solo en Rechazado, con fecha con hora y zona (no
  anterior a Fecha) y el motivo después de la fecha.
- Sustituido por (un solo ADR): obligatorio en Sustituido y prohibido en el
  resto. El sucesor existe, es otro ADR, está Aceptado o Sustituido y su
  Sustituye incluye este ADR.
- Sustituye (uno o varios ADRs): no se admite en Rechazado. Cada ADR
  sustituido existe y no es el propio. Si el declarante está Aceptado o
  Sustituido, cada sustituido está Sustituido por él (reciprocidad). Si está
  Propuesto, el sustituido sigue Aceptado a la espera de la aceptación.
- Tipo: solo vale «Excepción»; con ese tipo Caducidad (fecha con hora y zona,
  no anterior a Fecha) es obligatoria, y sin él está prohibida (ADR-006 §2).
- Drivers: opcional; si aparece no puede estar vacío («N/A» vale).
- El README de la carpeta lista cada ADR con su mismo estado. Si el índice
  tiene la 4.ª columna «Sustituido por», es «—» o el ADR sucesor.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sdaf_meta import fecha_key, has_time  # noqa: E402

ESTADOS = {"Propuesto", "Aceptado", "Rechazado", "Sustituido", "Deprecado"}
TIPO_EXCEPCION = "Excepción"
FILE_RE = re.compile(r"^ADR-([0-9]{3})-[a-z0-9-]+\.md$")
TITLE_RE = re.compile(r"^# ADR-([0-9]{3}) — .+$", re.MULTILINE)
FIELD_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$", re.MULTILINE)
LEADING_DATE_RE = re.compile(r"^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]+(?:Z|[+-][0-9]{2}:[0-9]{2}))")
ADR_REF_RE = re.compile(r"ADR-([0-9]{3})")
# Columnas: ADR | Estado | Título | [Sustituido por]. La 4.ª es opcional
# (consumidores con el índice anterior); el grupo 4 es None si falta.
INDEX_ROW_RE = re.compile(
    r"^\|\s*\[ADR-([0-9]{3})\]\(([^)]+)\)\s*\|\s*([^|]+?)\s*\|"
    r"(?:[ \t]*[^|\n]*?[ \t]*\|[ \t]*([^|\n]*?)[ \t]*\|)?",
    re.MULTILINE,
)


def fields(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, value in FIELD_RE.findall(text):
        key = key.strip("* ")
        if key in {"Campo", "ADR"} or set(key) <= {"-"}:
            continue
        out.setdefault(key, value.strip())
    return out


def refs(value: str) -> list[str]:
    """Números de ADR citados en un valor, sin repetidos y en orden."""
    return list(dict.fromkeys(ADR_REF_RE.findall(value)))


def fecha_inicial(nombre: str, valor: str | None, fecha: str, errs: list[str]) -> re.Match[str] | None:
    """Comprueba que `valor` empiece por fecha con hora y zona no anterior a Fecha.

    Devuelve el match si el formato es válido y None si no lo es (el llamador
    informa del formato); el orden respecto a Fecha se informa aquí.
    """
    match = LEADING_DATE_RE.match(valor or "")
    if not match or fecha_key(match.group(1)) is None:
        return None
    desde = fecha_key(fecha)
    if desde is not None and fecha_key(match.group(1)) < desde:
        errs.append(f"{nombre} {match.group(1)} anterior a Fecha {fecha}")
    return match


def check_adr(path: Path) -> tuple[dict[str, str], list[str]]:
    """Devuelve (campos de cabecera, errores) de un ADR, sin mirar otros ADRs."""
    errs: list[str] = []
    num = FILE_RE.match(path.name).group(1)
    text = path.read_text(encoding="utf-8")
    title = TITLE_RE.search(text)
    if not title:
        errs.append("falta el título «# ADR-NNN — …»")
    elif title.group(1) != num:
        errs.append(f"el título dice ADR-{title.group(1)} y el fichero ADR-{num}")
    data = fields(text)
    estado = data.get("Estado")
    if estado not in ESTADOS:
        errs.append(f"Estado «{estado}» no es uno de {sorted(ESTADOS)}")
    fecha = data.get("Fecha", "")
    if not has_time(fecha) or fecha_key(fecha) is None:
        errs.append(f"Fecha «{fecha}» no es ISO 8601 con hora y zona (H13 §9)")

    # Aceptación
    aceptacion = data.get("Aceptación")
    if estado in {"Aceptado", "Sustituido"}:
        if not fecha_inicial("Aceptación", aceptacion, fecha, errs):
            errs.append(f"{estado} sin fila Aceptación que empiece por fecha con hora y zona")
    elif estado == "Propuesto" and aceptacion:
        errs.append("Propuesto con fila Aceptación: aceptar es un acto humano que cambia el Estado")
    elif estado == "Rechazado" and aceptacion:
        errs.append("Rechazado con fila Aceptación: un ADR rechazado no se acepta")
    elif estado == "Deprecado" and aceptacion:
        if not fecha_inicial("Aceptación", aceptacion, fecha, errs):
            errs.append("Aceptación no empieza por fecha con hora y zona")

    # Rechazo
    rechazo = data.get("Rechazo")
    if estado == "Rechazado":
        match = fecha_inicial("Rechazo", rechazo, fecha, errs)
        if not match:
            errs.append("Rechazado sin fila Rechazo que empiece por fecha con hora y zona")
        elif not (rechazo or "")[match.end():].strip(" ,.;:—-"):
            errs.append("Rechazo sin motivo después de la fecha")
    elif rechazo is not None:
        errs.append(f"{estado} con fila Rechazo: solo se admite en Rechazado")

    # Sustituido por
    sustituido_por = data.get("Sustituido por")
    if estado == "Sustituido":
        sucesores = refs(sustituido_por or "")
        if len(sucesores) != 1:
            errs.append("Sustituido sin «Sustituido por» que indique un único ADR (ADR-NNN)")
        elif sucesores[0] == num:
            errs.append("Sustituido por sí mismo")
    elif estado == "Aceptado" and sustituido_por is not None:
        errs.append("Aceptado con «Sustituido por»: el estado debe ser Sustituido")
    elif sustituido_por is not None:
        errs.append(f"{estado} con «Sustituido por»: solo se admite en Sustituido")

    # Sustituye
    sustituye = data.get("Sustituye")
    if sustituye is not None:
        if estado == "Rechazado":
            errs.append("Rechazado con «Sustituye»: un ADR rechazado no sustituye a otro")
        lista = refs(sustituye)
        if not lista:
            errs.append("«Sustituye» no indica ningún ADR (ADR-NNN)")
        if num in lista:
            errs.append("«Sustituye» a sí mismo")

    # Tipo y Caducidad
    tipo = data.get("Tipo")
    if tipo is not None and tipo != TIPO_EXCEPCION:
        errs.append(f"Tipo «{tipo}» no es válido: el único valor es «{TIPO_EXCEPCION}»")
    caducidad = data.get("Caducidad")
    if tipo == TIPO_EXCEPCION:
        if not fecha_inicial("Caducidad", caducidad, fecha, errs):
            errs.append("Tipo Excepción sin Caducidad que empiece por fecha con hora y zona (H13 §3)")
    elif caducidad is not None:
        errs.append("Caducidad sin Tipo «Excepción»: solo se admite en ADRs de excepción (ADR-006 §2)")

    # Drivers
    if "Drivers" in data and not data["Drivers"]:
        errs.append("Drivers vacío: indica los drivers o «N/A»")
    return data, errs


def sustitucion(num: str, datos: dict[str, dict[str, str]]) -> list[str]:
    """Errores de existencia y reciprocidad de Sustituye y Sustituido por en el ADR `num`."""
    errs: list[str] = []
    data = datos[num]
    estado = data.get("Estado")
    if estado == "Sustituido":
        sucesores = refs(data.get("Sustituido por", ""))
        if len(sucesores) == 1 and sucesores[0] != num:
            sig = sucesores[0]
            if sig not in datos:
                errs.append(f"Sustituido por ADR-{sig}, que no existe")
            elif datos[sig].get("Estado") not in {"Aceptado", "Sustituido"}:
                errs.append(
                    f"Sustituido por ADR-{sig}, que está {datos[sig].get('Estado')}: "
                    "el sucesor debe estar Aceptado o Sustituido"
                )
            elif num not in refs(datos[sig].get("Sustituye", "")):
                errs.append(f"Sustituido por ADR-{sig}, pero ADR-{sig} no declara «Sustituye» ADR-{num}")
    if estado == "Rechazado":
        return errs
    for ant in refs(data.get("Sustituye", "")):
        if ant == num:
            continue
        if ant not in datos:
            errs.append(f"Sustituye ADR-{ant}, que no existe")
            continue
        estado_ant = datos[ant].get("Estado")
        if estado in {"Aceptado", "Sustituido"}:
            if estado_ant != "Sustituido":
                errs.append(f"Sustituye ADR-{ant}, que está {estado_ant}: debe estar Sustituido por ADR-{num}")
            elif refs(datos[ant].get("Sustituido por", "")) != [num]:
                errs.append(f"Sustituye ADR-{ant}, pero ADR-{ant} no tiene «Sustituido por» ADR-{num}")
        elif estado == "Propuesto" and estado_ant != "Aceptado":
            errs.append(f"Sustituye ADR-{ant}, que está {estado_ant}: debe estar Aceptado hasta aceptar este ADR")
    return errs


def main() -> int:
    parser = argparse.ArgumentParser(description="Comprueba los ADRs del core.")
    parser.add_argument("--root", default=str(ROOT), help="Raíz del árbol a comprobar (fixtures).")
    root = Path(parser.parse_args().root).resolve()
    folder = root / "architecture" / "decisions"
    if not folder.is_dir():
        print("OK sin architecture/decisions/")
        return 0

    failed = 0
    datos: dict[str, dict[str, str]] = {}
    files: dict[str, str] = {}
    for path in sorted(folder.glob("ADR-*.md")):
        match = FILE_RE.match(path.name)
        if not match:
            print(f"FAIL {path.name}: nombre fuera de ADR-NNN-slug.md")
            failed += 1
            continue
        num = match.group(1)
        if num in files:
            print(f"FAIL ADR-{num} repetido: {files[num]} y {path.name}")
            failed += 1
            continue
        files[num] = path.name
        datos[num], errs = check_adr(path)
        for err in errs:
            print(f"FAIL {path.name}: {err}")
            failed += 1

    for num in files:
        for err in sustitucion(num, datos):
            print(f"FAIL {files[num]}: {err}")
            failed += 1

    expected = [f"{i:03d}" for i in range(1, len(files) + 1)]
    if sorted(files) != expected:
        print(f"FAIL numeración con huecos: {sorted(files)} (se espera {expected})")
        failed += 1

    readme = folder / "README.md"
    listed: dict[str, tuple[str, str, str | None]] = {}
    if readme.is_file():
        for m in INDEX_ROW_RE.finditer(readme.read_text(encoding="utf-8")):
            listed[m.group(1)] = (m.group(2), m.group(3), m.group(4))
    for num, name in files.items():
        if num not in listed:
            print(f"FAIL README.md no lista ADR-{num}")
            failed += 1
            continue
        href, estado, col_sust = listed[num]
        if href != name:
            print(f"FAIL README.md enlaza ADR-{num} a {href}, no a {name}")
            failed += 1
        if estado != datos[num].get("Estado"):
            print(f"FAIL README.md dice {estado} para ADR-{num}; el ADR dice {datos[num].get('Estado')}")
            failed += 1
        if col_sust is not None:  # sin 4.ª columna no es error (índice anterior)
            sucesores = refs(datos[num].get("Sustituido por", ""))
            coherente = refs(col_sust) == sucesores if sucesores else col_sust == "—"
            if not coherente:
                esperado = f"ADR-{sucesores[0]}" if sucesores else "—"
                print(f"FAIL README.md dice «{col_sust}» en Sustituido por de ADR-{num}; el ADR dice {esperado}")
                failed += 1
    for num in listed.keys() - files.keys():
        print(f"FAIL README.md lista ADR-{num}, que no existe")
        failed += 1

    if failed:
        print(f"{failed} problema(s) en los ADRs")
        return 1
    print(f"OK ADRs ({len(files)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
