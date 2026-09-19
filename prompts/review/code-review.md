# PROMPT-REV-CODE-001 — Code Review

| Campo | Valor |
|--------|--------|
| ID | PROMPT-REV-CODE-001 |
| Versión | 0.3.0 |
| Estado | Draft |
| Agente / rol | review / Testing+Review |
| Fecha | 2026-09-18 |

## Objetivo

Aplicar el checklist de [H10](../../handbook/10-code-review-and-quality-gates.md) a un diff.

## Contexto

- [H10](../../handbook/10-code-review-and-quality-gates.md), [H05](../../handbook/05-development-workflow.md) Gate 2
- `AGENTS.md` del consumidor
- Skill [`testing-review-pr`](../../skills/testing-review-pr/SKILL.md)

## Entradas

Diff, PBI, specs/ADR aplicables.

## Restricciones

Severizar hallazgos (H10 §5); no Approved autónomo; no ampliar Out.

## Resultado esperado

Dictamen bloqueante / mayor / menor + acciones.

## Formato de salida

Checklist H10 + veredicto de merge.

## Criterios de aceptación

Trazable a H10 y a specs Approved del PBI.

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.3.0 | 2026-09-18 | Draft: remap extract cap. 17 → H10 |
