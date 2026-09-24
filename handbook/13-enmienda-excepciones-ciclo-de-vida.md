# 13 — Enmienda, excepciones y ciclo de vida

> Andamiaje (cabecera, TOC, Relacionado, Historial): `_meta/13-enmienda-excepciones-ciclo-de-vida.yaml`.

## 1. Propósito

Definir cómo se enmienda la constitución, cómo se exceptúa con caducidad, cómo se deroga un capítulo y qué cambio es breaking.

Approved el 2026-09-24 por aceptación humana ([ADR-002](../architecture/decisions/ADR-002-gobernanza-del-metodo.md), Aceptado). Ningún agente declara Approved ([H00 §3.3](00-preface.md), [H10 §2](10-code-review-and-quality-gates.md)). Las cuatro viñetas de [H00 §3](00-preface.md) siguen vigentes; este capítulo las desarrolla.

## 2. Quién propone y quién acepta

1. Cualquier humano o agente puede **proponer** una enmienda (PR + fila de CHANGELOG propuesta + bump declarado).
2. Solo un humano **acepta**: pasa el capítulo de Draft a Approved, o acepta un ADR, o fusiona un cambio de significado de un capítulo Approved.
3. El rol «director técnico» aparece en historiales y en [H05 §7](05-development-workflow.md). **No está definido** (§8). Hasta que se defina, «quien acepta» es la identidad nombrada en [`CODEOWNERS`](../CODEOWNERS).
4. Ningún agente aprueba enmiendas constitucionales ([H10 §2](10-code-review-and-quality-gates.md)).

## 3. Excepciones temporales

La excepción que [H00 §3.4](00-preface.md) ya exige se registra como ADR con:

- alcance (qué viñeta se exceptúa);
- fecha de **caducidad**;
- plan de retorno a la norma.

Caducada sin prórroga humana, la excepción deja de aplicar. Force-push, reescritura de historia y auto-merge no se exceptúan ([H06 §7](06-ai-agent-framework.md)).

## 4. Estados de capítulo

| Estado | Significado |
|--------|-------------|
| Draft | Orienta; se corrige sin ceremonia |
| Approved | Norma vigente; cambio con enmienda, revisión humana, versión y CHANGELOG |
| Derogado | Dejó de aplicar; el archivo permanece con puntero al sucesor o a la fecha de derogación |

No se borra un capítulo Approved para ocultar el pasado ([H08 §7](08-agent-traceability.md) aplica el mismo criterio a la norma publicada).

## 5. Qué es breaking

Es **breaking** un cambio que obliga al consumidor a reescribir citas o configs para seguir siendo conforme:

- renumerar capítulos (precedente 0.1 → 0.2);
- retirar o renombrar un id de agente del núcleo;
- cambiar el significado de un invariante o de un gate de forma incompatible.

No es breaking, según el precedente ya publicado (0.2.1–0.3.3):

- parche que el CHANGELOG llama «no breaking de citas `H00`–`H08`»;
- fila de historial «sin cambio de norma»;
- añadir un capítulo sin renumerar los existentes.

Esta regla **no se aplica hacia atrás** a los tags `v0.2.1`–`v0.3.3`.

## 6. Regla de bump y commits

Clase **significado** (capítulo Approved cambia de obligación):

- Ejemplo: H06 §7 pasa a exigir petición explícita para commit. Bump **minor** del capítulo; fila en `handbook/CHANGELOG.md`; semver de línea patch o minor según §5 (si no rompe citas, no es major de línea).
- Ejemplo: renumerar H00–H08. Bump **major** de línea (precedente 0.2.0).

Clase **redacción** (el historial dice «sin cambio de norma»):

- Ejemplo: TOC y Relacionado en 0.2.2. Bump **patch** del capítulo; fila de CHANGELOG opcional si no hay cambio de obligación.
- Ejemplo: alinear cabecera de A a `0.3.2` porque el historial ya lo decía. Bump **patch**; no exige major.

La plantilla de PR marca la clase. No hay linter de commits. Prefijo admitido (`docs:`, `fix:`, `feat:`) + prosa en castellano.

## 7. Mantenedor único y QG-Review

Pregunta: ¿este merge con un solo humano cumple QG-Review?

**Sí**, si ese humano es la identidad de [`CODEOWNERS`](../CODEOWNERS) y el merge no es auto-merge de un agente. «Aprobación humana nominada» ([H10 §3.1](10-code-review-and-quality-gates.md)) nombra a esa persona; no exige un segundo humano. Auto-merge sigue prohibido sin orden humana ([H06 §7](06-ai-agent-framework.md)).

Vías descartadas el 2026-09-24: segunda cuenta, segundo revisor solo en cambios de significado, excepción con caducidad (§8).

## 8. Decisiones humanas

Cerradas el 2026-09-24 por aceptación humana ([ADR-002](../architecture/decisions/ADR-002-gobernanza-del-metodo.md), [ADR-003](../architecture/decisions/ADR-003-formato-de-artefactos.md)). Cambiarlas exige enmendar este capítulo y el ADR.

| Decisión | Elegida | Descartadas |
|----------|---------|-------------|
| Severidad de I4 | Aviso por defecto; `--strict-i4` es error | Error duro siempre; error solo sin contrato local |
| Artefactos con versión y sin historial | Fila inicial que repite la cabecera | Excluir del checker; retirar `Versión` |
| Tags `v0.3.0` / `v0.3.1` | No se crean; el CHANGELOG declara la ausencia | Tags retroactivos; retirar las entradas |
| QG-Review con un solo mantenedor | La lectura de §7 | Segunda cuenta; segundo revisor en cambios de significado; excepción con caducidad |
| Numeración de ADRs del core | Desde 001; «ADR-008» en historiales hasta `v0.3.3` = ADR-001 | Conservar 008 |
| Hora en las fechas | ISO 8601 con hora y zona desde la línea 0.4.0 (§9) | Completar la hora de fechas ya publicadas |
| `resumen_acumulado` | Índice de una línea ([ADR-003](../architecture/decisions/ADR-003-formato-de-artefactos.md)) | Sustituir la tabla Historial; volcado de commit/PR/SHA |

Sigue **abierta**: la definición del rol «director técnico» (§2).

## 9. Fechas

Desde la línea `0.4.0`, toda fecha **nueva** de cabecera, fila de historial, ADR, entrada del CHANGELOG o worklog se escribe en ISO 8601 con hora y zona horaria: `AAAA-MM-DDThh:mm±hh:mm`. La hora es la del registro de esa versión o decisión en el artefacto, medida, no estimada.

- La fecha de cabecera de un artefacto es la de la fila más reciente de su versión máxima.
- Las fechas de versiones publicadas hasta `v0.3.3` conservan solo el día. No se completan: la hora no consta y añadirla sería reescribir historial ([H08 §7](08-agent-traceability.md)). Una fila nueva que describe una versión ya publicada puede quedarse con el día.
- Lo comprueban `scripts/check-version-metadata.py` (formato y cabecera = fila más reciente), `scripts/check-history-append-only.py` (fila nueva de una versión nueva lleva hora) y `scripts/check-adrs.py` (Fecha y Aceptación de los ADRs con hora y zona; Aceptación no anterior a Fecha). `scripts/test-dates.py` los prueba con fixtures.
