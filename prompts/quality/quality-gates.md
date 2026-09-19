# PROMPT-QUA-QG-001 — Quality Gates

| Campo | Valor |
|--------|--------|
| ID | PROMPT-QUA-QG-001 |
| Versión | 0.3.2 |
| Estado | Approved |
| Agente / rol | quality / Testing+Review |
| Fecha | 2026-09-19 |

## Objetivo

Evaluar quality gates locales (build / unit / accept / review / sec) de un cambio.

## Contexto

- [H05](../../handbook/05-development-workflow.md), [H10](../../handbook/10-code-review-and-quality-gates.md)
- Runbook local del consumidor ([H11](../../handbook/11-devops.md))
- Skills `testing-review-pr`, `security-review` si aplica

## Entradas

Resultados de test; diff; evidencia de Gate 0.

## Restricciones

Dictamen de agente ≠ merge. QG-Review exige humano nominado (H10 §2). Local-first; no exigir cloud CI; comandos = runbook del consumidor. Overlays H12 §3 = N/A salvo ADR.

## Resultado esperado

Pass/fail por QG + acciones.

## Formato de salida

Tabla QG → estado → evidencia.

## Criterios de aceptación

G0–G2 y QG coherentes con H05 y H10.

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.3.2 | 2026-09-19 | QG-Review HITL; QG-Sec H12 §5.2; overlays N/A salvo ADR |
| 0.3.0 | 2026-09-19 | Approved (aprobación humana del director técnico) |
| 0.3.0 | 2026-09-18 | Draft: remap extract caps. 09/17 → H05/H10 |
