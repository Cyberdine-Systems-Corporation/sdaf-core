#!/usr/bin/env python3
"""Comprueba los ADRs de architecture/decisions/ (ADR-006).

Dos modos. Por defecto es el modo core, estricto, para los ADRs del core.
Con `--consumer` se aplican las mismas reglas con las relajaciones de formato
de un proyecto que adopta SDAF con ADRs previos; `--legacy-up-to N` (solo con
`--consumer`, entero >= 0, por defecto 0 = ninguno) marca como heredados los
ADRs de número <= N, a los que además se aplican las relajaciones de contenido.

Modo core (las reglas siguientes; sin `--consumer` nada de lo demás cambia):

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

Modo consumidor (`--consumer`), para todos los ADRs:

- Formato: nombre ADR-NNN-slug.md o ADR-NNNN-slug.md (3 o 4 dígitos), título
  «# ADR-N» seguido de «—», «-» o «:», referencias de 3 o 4 dígitos. El número
  se normaliza a entero: ADR-001 y ADR-0001 son el mismo y no pueden coexistir.
  Se permiten huecos en la numeración.
- Lectura: se tolera el BOM; un fichero que no es UTF-8 da `FAIL <fichero>: no
  es UTF-8` y no oculta los demás.
- Índice: las columnas «Estado» y «Sustituido por» se localizan por el nombre
  de la cabecera (sin distinguir mayúsculas); sin cabecera que las nombre
  valen la 2.ª y la 4.ª. Se tolera «./» en el enlace. Sin README o sin columna
  «Estado» se imprime una línea `AVISO ...` (no cambia el código de salida) y
  no se compara. Un ADR no listado, un ADR listado que no existe o un
  estado/sucesor que contradice al ADR siguen siendo FAIL.

Solo en ADRs heredados (número <= `--legacy-up-to`):

- Fecha: ISO 8601 con hora y zona o solo YYYY-MM-DD; las comparaciones con
  Aceptación, Rechazo y Caducidad usan el día si algún lado no trae hora.
- Estado: por tabla cerrada, sin distinguir mayúsculas: proposed/propuesto/
  propuesta, accepted/aceptado/aceptada, rejected/rechazado/rechazada,
  superseded/sustituido/sustituida, deprecated/deprecado/deprecada. Cualquier
  otro valor es FAIL. El estado del índice pasa por la misma tabla.
- Aceptación: opcional en Aceptado, Sustituido y Deprecado; si existe empieza
  por fecha (con o sin hora) y no es anterior a Fecha.

Siguen estrictas siempre, heredados incluidos: Propuesto y Rechazado sin
Aceptación, Rechazo completo, reciprocidad Sustituye / Sustituido por, Tipo y
Caducidad con hora y zona. Los ADRs nuevos (número > N) cumplen las reglas del
modo core íntegras, con solo las relajaciones de formato de arriba.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sdaf_adrs import DIGITS, adr_label, adr_num, fields, file_re, index_rows, index_table, refs, title_re  # noqa: E402
from sdaf_meta import fecha_key, has_time  # noqa: E402

ESTADOS = {"Propuesto", "Aceptado", "Rechazado", "Sustituido", "Deprecado"}
TIPO_EXCEPCION = "Excepción"
# Modo consumidor: ancho del número y equivalencias de estado de los ADRs heredados.
CONSUMER_DIGITS = (3, 4)
ESTADOS_HEREDADOS = {
    "proposed": "Propuesto", "propuesto": "Propuesto", "propuesta": "Propuesto",
    "accepted": "Aceptado", "aceptado": "Aceptado", "aceptada": "Aceptado",
    "rejected": "Rechazado", "rechazado": "Rechazado", "rechazada": "Rechazado",
    "superseded": "Sustituido", "sustituido": "Sustituido", "sustituida": "Sustituido",
    "deprecated": "Deprecado", "deprecado": "Deprecado", "deprecada": "Deprecado",
}
SIN_SUCESOR = {"", "—", "–", "-", "n/a"}  # celdas de «Sustituido por» del índice que significan «ninguno»
LEADING_DATE_RE = re.compile(r"^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]+(?:Z|[+-][0-9]{2}:[0-9]{2}))")
LEADING_ANY_DATE_RE = re.compile(
    r"^([0-9]{4}-[0-9]{2}-[0-9]{2}(?:T[0-9:]+(?:Z|[+-][0-9]{2}:[0-9]{2}))?)(?![0-9T])"
)
DATE_ONLY_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")


def fecha_inicial(
    nombre: str, valor: str | None, fecha: str, errs: list[str], dia: bool = False, sin_hora: bool = False
) -> re.Match[str] | None:
    """Comprueba que `valor` empiece por fecha con hora y zona no anterior a Fecha.

    Devuelve el match si el formato es válido y None si no lo es (el llamador
    informa del formato); el orden respecto a Fecha se informa aquí. Con `dia`
    se compara solo el día si algún lado no trae hora; con `sin_hora` el valor
    puede ser YYYY-MM-DD (ADRs heredados).
    """
    match = (LEADING_ANY_DATE_RE if sin_hora else LEADING_DATE_RE).match(valor or "")
    if not match or fecha_key(match.group(1)) is None:
        return None
    desde = fecha_key(fecha)
    if desde is not None:
        if dia and not (has_time(match.group(1)) and has_time(fecha)):
            antes = match.group(1)[:10] < fecha[:10]
        else:
            antes = fecha_key(match.group(1)) < desde
        if antes:
            errs.append(f"{nombre} {match.group(1)} anterior a Fecha {fecha}")
    return match


def leer(path: Path, consumer: bool) -> str | None:
    """Texto del fichero. En el modo consumidor tolera el BOM y da None si no es UTF-8."""
    if not consumer:
        return path.read_text(encoding="utf-8")
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return None


def check_adr(
    path: Path, text: str, consumer: bool = False, legacy_up_to: int = 0
) -> tuple[dict[str, str], list[str]]:
    """Devuelve (campos de cabecera, errores) de un ADR, sin mirar otros ADRs.

    En los heredados el Estado de `campos` ya va normalizado a su valor canónico.
    """
    errs: list[str] = []
    digits = CONSUMER_DIGITS if consumer else DIGITS
    num = adr_num(file_re(digits).match(path.name).group(1))
    legacy = consumer and num <= legacy_up_to
    title = title_re(digits, consumer).search(text)
    if not title:
        errs.append("falta el título «# ADR-NNN — …»" + (" (separador «—», «-» o «:»)" if consumer else ""))
    elif adr_num(title.group(1)) != num:
        errs.append(f"el título dice {adr_label(adr_num(title.group(1)))} y el fichero {adr_label(num)}")
    data = fields(text)
    estado = data.get("Estado")
    if legacy:
        canonico = ESTADOS_HEREDADOS.get((estado or "").casefold())
        if canonico:
            estado = data["Estado"] = canonico
        else:
            errs.append(f"Estado «{estado}» no es uno de {sorted(ESTADOS_HEREDADOS)} (ADR heredado, sin distinguir mayúsculas)")
    elif estado not in ESTADOS:
        errs.append(f"Estado «{estado}» no es uno de {sorted(ESTADOS)}")
    fecha = data.get("Fecha", "")
    if legacy:
        if not (has_time(fecha) or DATE_ONLY_RE.match(fecha)) or fecha_key(fecha) is None:
            errs.append(f"Fecha «{fecha}» no es ISO 8601 (YYYY-MM-DD, o con hora y zona) (ADR heredado)")
    elif not has_time(fecha) or fecha_key(fecha) is None:
        errs.append(f"Fecha «{fecha}» no es ISO 8601 con hora y zona (H13 §9)")

    # Aceptación
    aceptacion = data.get("Aceptación")
    if legacy and estado in {"Aceptado", "Sustituido", "Deprecado"}:
        if aceptacion is not None and not fecha_inicial("Aceptación", aceptacion, fecha, errs, dia=True, sin_hora=True):
            errs.append("Aceptación no empieza por fecha (YYYY-MM-DD, con o sin hora)")
    elif estado in {"Aceptado", "Sustituido"}:
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
        match = fecha_inicial("Rechazo", rechazo, fecha, errs, dia=legacy)
        if not match:
            errs.append("Rechazado sin fila Rechazo que empiece por fecha con hora y zona")
        elif not (rechazo or "")[match.end():].strip(" ,.;:—-"):
            errs.append("Rechazo sin motivo después de la fecha")
    elif rechazo is not None:
        errs.append(f"{estado} con fila Rechazo: solo se admite en Rechazado")

    # Sustituido por
    sustituido_por = data.get("Sustituido por")
    if estado == "Sustituido":
        sucesores = refs(sustituido_por or "", digits)
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
        lista = refs(sustituye, digits)
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
        if not fecha_inicial("Caducidad", caducidad, fecha, errs, dia=legacy):
            errs.append("Tipo Excepción sin Caducidad que empiece por fecha con hora y zona (H13 §3)")
    elif caducidad is not None:
        errs.append("Caducidad sin Tipo «Excepción»: solo se admite en ADRs de excepción (ADR-006 §2)")

    # Drivers
    if "Drivers" in data and not data["Drivers"]:
        errs.append("Drivers vacío: indica los drivers o «N/A»")
    return data, errs


def sustitucion(num: int, datos: dict[int, dict[str, str]], digits: tuple[int, int] = DIGITS) -> list[str]:
    """Errores de existencia y reciprocidad de Sustituye y Sustituido por en el ADR `num`."""
    errs: list[str] = []
    data = datos[num]
    estado = data.get("Estado")
    if estado == "Sustituido":
        sucesores = refs(data.get("Sustituido por", ""), digits)
        if len(sucesores) == 1 and sucesores[0] != num:
            sig = sucesores[0]
            if sig not in datos:
                errs.append(f"Sustituido por {adr_label(sig)}, que no existe")
            elif datos[sig].get("Estado") not in {"Aceptado", "Sustituido"}:
                errs.append(
                    f"Sustituido por {adr_label(sig)}, que está {datos[sig].get('Estado')}: "
                    "el sucesor debe estar Aceptado o Sustituido"
                )
            elif num not in refs(datos[sig].get("Sustituye", ""), digits):
                errs.append(f"Sustituido por {adr_label(sig)}, pero {adr_label(sig)} no declara «Sustituye» {adr_label(num)}")
    if estado == "Rechazado":
        return errs
    for ant in refs(data.get("Sustituye", ""), digits):
        if ant == num:
            continue
        if ant not in datos:
            errs.append(f"Sustituye {adr_label(ant)}, que no existe")
            continue
        estado_ant = datos[ant].get("Estado")
        if estado in {"Aceptado", "Sustituido"}:
            if estado_ant != "Sustituido":
                errs.append(f"Sustituye {adr_label(ant)}, que está {estado_ant}: debe estar Sustituido por {adr_label(num)}")
            elif refs(datos[ant].get("Sustituido por", ""), digits) != [num]:
                errs.append(f"Sustituye {adr_label(ant)}, pero {adr_label(ant)} no tiene «Sustituido por» {adr_label(num)}")
        elif estado == "Propuesto" and estado_ant != "Aceptado":
            errs.append(f"Sustituye {adr_label(ant)}, que está {estado_ant}: debe estar Aceptado hasta aceptar este ADR")
    return errs


def indice_core(folder: Path, files: dict[int, str], datos: dict[int, dict[str, str]]) -> int:
    """Compara el README con los ADRs en el modo core; devuelve los FAIL."""
    failed = 0
    readme = folder / "README.md"
    listed: dict[int, tuple[str, str, str | None]] = {}
    if readme.is_file():
        listed = index_rows(readme.read_text(encoding="utf-8"))
    for num, name in files.items():
        if num not in listed:
            print(f"FAIL README.md no lista {adr_label(num)}")
            failed += 1
            continue
        href, estado, col_sust = listed[num]
        if href != name:
            print(f"FAIL README.md enlaza {adr_label(num)} a {href}, no a {name}")
            failed += 1
        if estado != datos[num].get("Estado"):
            print(f"FAIL README.md dice {estado} para {adr_label(num)}; el ADR dice {datos[num].get('Estado')}")
            failed += 1
        if col_sust is not None:  # sin 4.ª columna no es error (índice anterior)
            sucesores = refs(datos[num].get("Sustituido por", ""))
            coherente = refs(col_sust) == sucesores if sucesores else col_sust == "—"
            if not coherente:
                esperado = adr_label(sucesores[0]) if sucesores else "—"
                print(f"FAIL README.md dice «{col_sust}» en Sustituido por de {adr_label(num)}; el ADR dice {esperado}")
                failed += 1
    for num in listed.keys() - files.keys():
        print(f"FAIL README.md lista {adr_label(num)}, que no existe")
        failed += 1
    return failed


def indice_consumidor(
    folder: Path, files: dict[int, str], datos: dict[int, dict[str, str]], legacy_up_to: int, ilegibles: set[int]
) -> int:
    """Compara el README con los ADRs en el modo consumidor; devuelve los FAIL.

    Sin README o sin columna Estado localizable solo avisa (AVISO, sin FAIL).
    """
    readme = folder / "README.md"
    if not readme.is_file():
        print("AVISO sin README.md de índice en architecture/decisions/: no se comprueba el índice")
        return 0
    text = leer(readme, True)
    if text is None:
        print("FAIL README.md: no es UTF-8")
        return 1
    table = index_table(text, CONSUMER_DIGITS)
    if "estado" not in table.cols:
        print("AVISO el índice README.md no tiene columna «Estado» reconocible: no se compara el estado")
    failed = 0
    for num, name in files.items():
        if num not in table.rows:
            print(f"FAIL README.md no lista {adr_label(num)}")
            failed += 1
            continue
        if table.rows[num][0] != name:
            print(f"FAIL README.md enlaza {adr_label(num)} a {table.rows[num][0]}, no a {name}")
            failed += 1
        if num in ilegibles:
            continue
        estado_adr = datos[num].get("Estado")
        estado_idx = table.cell(num, "estado")
        if estado_idx is not None and estado_adr in ESTADOS:  # un Estado inválido ya se ha informado
            visto = ESTADOS_HEREDADOS.get(estado_idx.casefold(), estado_idx) if num <= legacy_up_to else estado_idx
            if visto != estado_adr:
                print(
                    f"FAIL README.md dice «{estado_idx}» en la columna {table.column_name('estado')} "
                    f"para {adr_label(num)}; el ADR dice {estado_adr}"
                )
                failed += 1
        col_sust = table.cell(num, "sustituido por")
        if col_sust is not None:
            sucesores = refs(datos[num].get("Sustituido por", ""), CONSUMER_DIGITS)
            coherente = (
                refs(col_sust, CONSUMER_DIGITS) == sucesores if sucesores else col_sust.casefold() in SIN_SUCESOR
            )
            if not coherente:
                esperado = adr_label(sucesores[0]) if sucesores else "—"
                print(
                    f"FAIL README.md dice «{col_sust}» en la columna {table.column_name('sustituido por')} "
                    f"para {adr_label(num)}; el ADR dice {esperado}"
                )
                failed += 1
    for num in sorted(table.rows.keys() - files.keys()):
        print(f"FAIL README.md lista {adr_label(num)}, que no existe")
        failed += 1
    return failed


def entero_no_negativo(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"«{value}» no es un entero") from None
    if number < 0:
        raise argparse.ArgumentTypeError(f"«{value}» es negativo")
    return number


def main() -> int:
    parser = argparse.ArgumentParser(description="Comprueba los ADRs de architecture/decisions/.")
    parser.add_argument("--root", default=str(ROOT), help="Raíz del árbol a comprobar (fixtures).")
    parser.add_argument(
        "--consumer", action="store_true",
        help="Modo consumidor: relajaciones de formato (números de 3 o 4 dígitos, huecos, índice por cabeceras, BOM).",
    )
    parser.add_argument(
        "--legacy-up-to", type=entero_no_negativo, default=None, metavar="N",
        help="Con --consumer: los ADRs de número <= N son heredados (por defecto 0 = ninguno).",
    )
    args = parser.parse_args()
    if args.legacy_up_to is not None and not args.consumer:
        parser.error("--legacy-up-to solo se admite con --consumer")
    consumer = args.consumer
    legacy_up_to = args.legacy_up_to or 0
    digits = CONSUMER_DIGITS if consumer else DIGITS
    root = Path(args.root).resolve()
    folder = root / "architecture" / "decisions"
    if not folder.is_dir():
        print("OK sin architecture/decisions/")
        return 0

    failed = 0
    datos: dict[int, dict[str, str]] = {}
    files: dict[int, str] = {}
    ilegibles: set[int] = set()
    for path in sorted(folder.glob("ADR-*.md")):
        match = file_re(digits).match(path.name)
        if not match:
            print(f"FAIL {path.name}: nombre fuera de ADR-NNN-slug.md" + (" (3 o 4 dígitos)" if consumer else ""))
            failed += 1
            continue
        num = adr_num(match.group(1))
        if num in files:
            print(f"FAIL {adr_label(num)} repetido: {files[num]} y {path.name}")
            failed += 1
            continue
        files[num] = path.name
        text = leer(path, consumer)
        if text is None:
            print(f"FAIL {path.name}: no es UTF-8")
            failed += 1
            datos[num] = {}
            ilegibles.add(num)
            continue
        datos[num], errs = check_adr(path, text, consumer, legacy_up_to)
        for err in errs:
            print(f"FAIL {path.name}: {err}")
            failed += 1

    for num in files:
        if num in ilegibles:
            continue
        for err in sustitucion(num, datos, digits):
            print(f"FAIL {files[num]}: {err}")
            failed += 1

    if not consumer:  # el consumidor admite huecos en la numeración
        expected = [f"{i:03d}" for i in range(1, len(files) + 1)]
        found = [f"{n:03d}" for n in sorted(files)]
        if found != expected:
            print(f"FAIL numeración con huecos: {found} (se espera {expected})")
            failed += 1

    if consumer:
        failed += indice_consumidor(folder, files, datos, legacy_up_to, ilegibles)
    else:
        failed += indice_core(folder, files, datos)

    if failed:
        print(f"{failed} problema(s) en los ADRs")
        return 1
    print(f"OK ADRs ({len(files)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
