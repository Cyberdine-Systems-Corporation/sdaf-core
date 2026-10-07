# ADR-006 — Ciclo de vida y sustitución de ADRs

| Campo | Valor |
|--------|--------|
| Estado | Aceptado |
| Fecha | 2026-09-28T18:08+02:00 |
| Decisores | Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS) |
| Aceptación | 2026-10-07T15:28+02:00, por Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS). El agente transcribe la aceptación dada en el encargo; no la autodeclara ([H00 §3.3](../../handbook/00-preface.md)). |
| Relacionado | [H13](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md), [H00 §3](../../handbook/00-preface.md), [plantilla ADR](../../templates/adr.md), [ADR-002](ADR-002-gobernanza-del-metodo.md), [ADR-005](ADR-005-linea-base-arquitectonica.md), [worklog](../../worklogs/INIT-arquitectura/Iteration-001.md) |

## Contexto

La plantilla de ADR ([`templates/adr.md`](../../templates/adr.md)) solo tiene Contexto, Decisión, Alternativas y Consecuencias, y tres estados: Propuesto, Aceptado y Deprecado. `scripts/check-adrs.py` fija esos tres estados.

Faltan piezas que el propio core ya exige en otros artefactos:

- **Sustitución.** H13 §4 define «Derogado, con puntero al sucesor» para capítulos; un ADR no tiene forma de decir qué ADR lo sustituye ni a cuál sustituye. Sin ese puntero no se puede calcular qué decisiones están vigentes, que es lo que necesita el índice de la línea base ([ADR-005](ADR-005-linea-base-arquitectonica.md)).
- **Rechazo.** Un ADR Propuesto que el humano no acepta no tiene estado: o se borra (se pierde la alternativa estudiada) o queda Propuesto indefinidamente.
- **Drivers.** No hay campo que enlace la decisión con los atributos de calidad o las specs que la motivan.
- **Caducidad.** Las excepciones temporales de H13 §3 son ADRs con fecha de caducidad, pero la plantilla no tiene ese campo.
- **Enmienda tras aceptar.** ADR-001 a 003 se enmendaron «por orden humana en el mismo encargo». No hay regla para lo que ocurre después: corregir redacción o cambiar la decisión.

## Decisión

1. **Estados.** `Propuesto`, `Aceptado`, `Rechazado`, `Sustituido`, `Deprecado`.
   - `Rechazado`: el humano no lo acepta. El fichero se conserva con el motivo.
   - `Sustituido`: otro ADR Aceptado lo reemplaza. Exige el campo «Sustituido por».
   - `Deprecado`: deja de aplicar sin sucesor.
   - Aceptar, rechazar o marcar como sustituido es un acto humano ([H00 §3.3](../../handbook/00-preface.md)).
2. **Campos nuevos de cabecera.**
   - `Sustituye` y `Sustituido por`: enlaces recíprocos; ambos extremos deben coincidir.
   - `Drivers`: specs, atributos de calidad de la línea base o capítulos que motivan la decisión (`N/A` si no hay).
   - `Caducidad`: obligatorio en ADRs de excepción (H13 §3); ausente en el resto.
3. **Enmienda después de aceptar.** Corregir redacción sin cambiar la decisión se permite y se anota en la fila Aceptación («Enmendado por orden humana…», precedente de ADR-001 a 003). Cambiar la decisión exige un ADR nuevo que sustituya al anterior.
4. **Vigencia.** Un ADR está vigente si está Aceptado y no tiene «Sustituido por». El índice de decisiones de la línea base ([ADR-005](ADR-005-linea-base-arquitectonica.md)) lista solo los vigentes.
5. **Alcance.** La plantilla aplica a core y consumidor. `check-adrs.py` valida estados, reciprocidad de la sustitución y caducidad. Se ofrece al consumidor como paso opcional de la action `validate-sdaf`, con la misma raíz que ya usa `--consumer-root`.

## Alternativas consideradas

- **Mantener tres estados.** No permite calcular las decisiones vigentes ni conservar alternativas rechazadas.
- **Editar el ADR aceptado cuando cambia la decisión.** Reescribe historia publicada ([H08 §7](../../handbook/08-agent-traceability.md)).
- **Historial de versiones dentro de cada ADR.** Duplica el mecanismo de sustitución y añade andamiaje que un agente tendría que leer (ADR-003).

## Consecuencias

- Cambian `templates/adr.md`, `scripts/check-adrs.py` (con fixtures), el índice `architecture/decisions/README.md` (columna de sustitución) y la skill `adr-propose`.
- Los ADR-001 a 004 del core siguen conformes: no sustituyen a otro ni son sustituidos.
- Para el consumidor no es breaking mientras la validación de sus ADRs sea opt-in; entra en la línea `0.5.0` junto con [ADR-005](ADR-005-linea-base-arquitectonica.md), que depende de la noción de vigencia.
