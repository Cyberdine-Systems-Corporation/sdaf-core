# PROMPT-REV-ARCH-001 — Architecture Review

| Campo | Valor |
|--------|--------|
| ID | PROMPT-REV-ARCH-001 |
| Versión | 0.3.0 |
| Estado | Approved |
| Agente / rol | architecture / review |
| Fecha | 2026-09-19 |

## Objetivo

Revisar coherencia arquitectónica de un diff o ADR frente a límites Approved.

## Contexto

- [H02](../../handbook/02-engineering-principles.md), [H05](../../handbook/05-development-workflow.md), [H10](../../handbook/10-code-review-and-quality-gates.md) §3.2
- ADRs del consumidor; handbook de producto si el diff toca MVP
- `AGENTS.md` del consumidor

## Entradas

Diff, ADR o spec a revisar.

## Restricciones

Severizar hallazgos; no Approved autónomo; no introducir bounded contexts o stack nuevo sin ADR.

## Resultado esperado

Dictamen bloqueante / mayor / menor + acciones (QG-Arch).

## Formato de salida

Checklist de límites + veredicto.

## Criterios de aceptación

Trazable a ADRs vigentes y a H10 QG-Arch.

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.3.0 | 2026-09-19 | Approved (aprobación humana del director técnico) |
| 0.3.0 | 2026-09-18 | Draft: remap extract; Partes III/V → H02/H10 |
