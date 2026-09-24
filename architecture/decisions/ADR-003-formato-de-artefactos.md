# ADR-003 — Formato de andamiaje y worklog

| Campo | Valor |
|--------|--------|
| Estado | Aceptado |
| Fecha | 2026-09-23T15:32+02:00 |
| Decisores | Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS) |
| Aceptación | 2026-09-24T18:21+02:00, por Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS). El agente transcribe la aceptación dada en el encargo; no la autodeclara ([H00 §3.3](../../handbook/00-preface.md)). Enmendado por orden humana en el mismo encargo: `inicio`/`fin`, `tiempo` y `coste` del worklog, y fechas con hora. Forma final registrada: 2026-09-24T18:54+02:00. |
| Relacionado | [H07 §4 y §7](../../handbook/07-prompt-engineering-standard.md), [H08 §4 y §6](../../handbook/08-agent-traceability.md) |

## Contexto

Un Gate 2 carga andamiaje humano (cabecera, TOC, Relacionado, Historial) que H07 §7 no quiere concatenar. La cadena H08 §6 (commit, PR, rama, SHA) no tiene campos en el worklog. Un único cambio de formato cubre ambos: el parser de metadatos se sustituye a la vez.

## Decisión

1. **Dónde vive el andamiaje humano.** Cabecera, TOC «En esta página», Relacionado e Historial de los capítulos del handbook salen del cuerpo y viven en `handbook/_meta/<stem>.yaml`. El catálogo está en [`handbook/index.yaml`](../../handbook/index.yaml). El cuerpo conserva un puntero al sidecar. Los prompts y skills **no** extraen el historial: H07 §4 sigue exigiendo historial en el artefacto del prompt.
2. **Cómo se versiona un artefacto tras el cambio.** La cabecera de versión es el campo `version` del sidecar (capítulos) o de la tabla del cuerpo (prompts, skills, contratos). Debe coincidir con la máxima del historial, y su fecha con la de la fila más reciente de esa versión. Desde la línea 0.4.0 las fechas nuevas llevan hora y zona (ISO 8601); las publicadas hasta `v0.3.3` conservan el día ([H13 §9](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md)). Lo comprueban `scripts/check-version-metadata.py` y `scripts/check-history-append-only.py` vía `scripts/sdaf_meta.py`.
3. **Contrato del worklog nuevo.** Frontmatter YAML validado por [`worklog.schema.json`](../../worklog.schema.json). Campos de trazabilidad `commit`, `pr`, `rama`, `sha` (cada uno `null` declara ausencia). `inicio` y `fin` con hora y zona horaria (ISO 8601); `tiempo` como duración ISO 8601 no mayor que `fin − inicio`; `coste` como objeto (modalidad, importe, moneda, tokens, fuente). `N/D` solo con motivo (`N/D: <motivo>`). `resumen_acumulado` es un **índice de una línea** al estilo H07 §7 (`id@version` más refs git si existen). No sustituye al prompt versionado ni a la tabla Historial de un capítulo. Los worklogs en tabla markdown vigente siguen válidos; no hay backfill (H08 §4.1 y §4.3).

## Alternativas consideradas

- Dejar el andamiaje en el cuerpo y medir tokens. No reduce la carga de un Gate 2.
- Extraer también el historial de prompts. Rompe H07 §4 sin necesidad: el agente ya abre un prompt, no doce capítulos.
- `resumen_acumulado` como volcado de commit/PR/SHA. Duplica los campos de trazabilidad.

## Consecuencias

- Quien parsee tablas de historial en el cuerpo de un capítulo se rompe al subir el pin.
- El schema de worklog acepta el formato nuevo; el validador acepta además la tabla vieja.
- Aceptado por humano el 2026-09-24; forma parte de la línea `0.4.0`.
