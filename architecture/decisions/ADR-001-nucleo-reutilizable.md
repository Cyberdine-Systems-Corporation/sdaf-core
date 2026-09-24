# ADR-001 — Extracción del núcleo reutilizable

| Campo | Valor |
|--------|--------|
| Estado | Aceptado |
| Fecha | 2026-09-23T15:32+02:00 |
| Decisores | Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS) |
| Aceptación | 2026-09-24T18:21+02:00, por Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS). El agente transcribe la aceptación dada en el encargo; no la autodeclara ([H00 §3.3](../../handbook/00-preface.md)). Enmendado por orden humana en el mismo encargo: numeración desde 001 (antes ADR-008). Forma final registrada: 2026-09-24T18:54+02:00. |
| Relacionado | [H00](../../handbook/00-preface.md), [H01](../../handbook/01-sdaf-framework.md), [H03](../../handbook/03-repository-organization.md) |

## Contexto

Diez capítulos (00–09), el apéndice A, el CHANGELOG, el README y cuatro prompts citan «ADR-008» como origen de la extracción genérica. Ese número venía del laboratorio del que salió el core, y el fichero nunca existió aquí. Este repo numera sus ADRs desde 001; «ADR-008» en historiales hasta `v0.3.3` equivale a este ADR-001.

## Decisión

sdaf-core es el núcleo reutilizable del método: handbook, contratos, prompts, skills, plantillas y esquema de config. No contiene código ni specs de un producto. El stack concreto lo decide el consumidor por ADR (pack opcional). Aceptado por humano el 2026-09-24.

## Alternativas consideradas

- Conservar el número 008. Obliga a explicar un hueco 001–007 que no pertenece a este repo.
- Dejar la cita huérfana. La cadena de decisiones del método sigue rota.

## Consecuencias

- Las citas vigentes apuntan a este fichero como ADR-001. Las filas de historial que dicen «(ADR-008)» no se reescriben (criterio de H08 §7) y equivalen a este ADR.
- Aceptarlo es un acto humano. Un agente no cambia el estado.
