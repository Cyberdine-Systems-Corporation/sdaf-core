# PROMPT-REV-ARCH-001 — Architecture Review

| Campo | Valor |
|--------|--------|
| ID | PROMPT-REV-ARCH-001 |
| Versión | 0.4.0 |
| Estado | Approved |
| Agente / rol | architecture / review |
| Fecha | 2026-10-11T23:12+02:00 |

## Objetivo

Revisar coherencia arquitectónica de un diff o ADR frente a la línea base Approved y sus reglas de dependencia.

## Contexto

- [H02](../../handbook/02-engineering-principles.md), [H05](../../handbook/05-development-workflow.md), [H10](../../handbook/10-code-review-and-quality-gates.md) §3.2
- `architecture/description.md` (línea base Approved) y [H14](../../handbook/14-architecture-description.md)
- ADRs vigentes del consumidor (Aceptados y no sustituidos, ADR-006); handbook de producto si el diff toca MVP
- `AGENTS.md` del consumidor

## Entradas

Diff, ADR o spec a revisar.

## Restricciones

Severizar hallazgos; no Approved autónomo; no introducir bounded contexts o stack nuevo sin ADR.

## Resultado esperado

Dictamen bloqueante / mayor / menor + acciones, y dictamen de QG-Arch (cumple, infracción nueva o `N/A` solo con el motivo escrito en el worklog).

## Formato de salida

Checklist de reglas de dependencia + veredicto.

## Criterios de aceptación

Trazable a la línea base, a los ADRs vigentes y a H10 QG-Arch. Si la línea base no declara reglas de dependencia, QG-Arch es `N/A` solo con motivo en el worklog; sin motivo no es N/A.

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.4.0 | 2026-10-11T23:12+02:00 | Revisión contra la línea base Approved y sus reglas de dependencia (H14); dictamen de QG-Arch; ADRs vigentes (ADR-006) |
| 0.3.0 | 2026-09-19 | Approved (aprobación humana del director técnico) |
| 0.3.0 | 2026-09-18 | Draft: remap extract; Partes III/V → H02/H10 |
