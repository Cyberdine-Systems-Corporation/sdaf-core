# ADR-002 — Gobernanza del método (enmienda, excepciones, ciclo de vida)

| Campo | Valor |
|--------|--------|
| Estado | Aceptado |
| Fecha | 2026-09-23T15:32+02:00 |
| Decisores | Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS) |
| Aceptación | 2026-09-24T18:21+02:00, por Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS). El agente transcribe la aceptación dada en el encargo; no la autodeclara ([H00 §3.3](../../handbook/00-preface.md)). Enmendado por orden humana en el mismo encargo: numeración desde 001, worklogs del core y fechas con hora. Forma final registrada: 2026-09-24T18:54+02:00. |
| Relacionado | [H13](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md), [H00 §3](../../handbook/00-preface.md), [H10](../../handbook/10-code-review-and-quality-gates.md) |

## Contexto

H00 §3 resume el ciclo de vida en cuatro viñetas (Draft, Approved, el agente no aprueba, excepción temporal). Falta derogación, regla de breaking, definición del rol «director técnico» y cómo un solo mantenedor satisface QG-Review. El invariante I4 del catálogo de config no tiene severidad normativa.

## Decisión

Se adopta el capítulo [13](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md) (Approved, `0.4.0`) como constitución de enmienda, excepciones y ciclo de vida. Las cuatro viñetas de H00 §3 siguen vigentes; H13 las desarrolla. La línea del handbook pasa a `0.4.0`.

Decisiones cerradas por aceptación humana el 2026-09-24 (tabla en H13 §8):

- I4: aviso por defecto; `--strict-i4` es error. El core no ve contratos locales salvo `--consumer-root`.
- Artefactos con versión y sin historial: fila inicial que repite la cabecera.
- Tags `v0.3.0` y `v0.3.1`: no se crean; las entradas del CHANGELOG se conservan y declaran la ausencia de tag.
- QG-Review: «nominada» = la identidad en [`CODEOWNERS`](../../CODEOWNERS). Esa persona puede aprobar su propio PR. Auto-merge sigue prohibido sin orden humana (H06 §7). Cambio de significado de H10: bump minor (`0.4.0`).
- Numeración: los ADRs del core empiezan en 001 (ADR-001 núcleo, ADR-002 gobernanza, ADR-003 formato). «ADR-008» en historiales hasta `v0.3.3` equivale a ADR-001; esas filas no se reescriben. El capítulo de gobernanza es 13 (no el antiguo 13 de agentes, hoy H06).
- Chequeo de worklog: script en el core (solo código de producto) y en la action del consumidor. El core guarda en `worklogs/` los worklogs de sus cambios materiales de handbook o ADR (H08 §5); como no tiene código de producto, esa obligación la comprueba QG-Review y el CI valida el formato de los ficheros.

## Alternativas consideradas

Las opciones descartadas están en la tabla de H13 §8.

## Consecuencias

- H00 remite a H13 (Approved). Sigue abierta la definición del rol «director técnico».
- CODEOWNERS y CONTRIBUTING apuntan a este procedimiento, no lo duplican.
- Cambiar I4 a error duro, crear tags retroactivos o exigir un segundo revisor exige enmendar este ADR y H13.
