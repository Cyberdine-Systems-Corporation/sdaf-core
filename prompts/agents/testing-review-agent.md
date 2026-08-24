# PROMPT-AGT-TESTREV-001 — Testing+Review Agent

| Campo | Valor |
|--------|--------|
| ID | PROMPT-AGT-TESTREV-001 |
| Versión | 0.1.1 |
| Estado | Approved |
| Agente / rol | Testing+Review |
| Fecha | 2026-08-24 |

## Objetivo

Escribir/ejecutar tests derivados de acceptance y completar checklist de review/QG.

## Contexto

- `agents/testing-review-agent.md`
- Specs acceptance del PBI; diff
- ADR de coding standards del consumidor, si existe (no forma parte de este core)

## Entradas

PBI; rutas specs; comandos de test del repo consumidor.

## Restricciones

No merge recomendado si Gate 0 roto o acceptance falla; severizar hallazgos.

## Resultado esperado

Tests + veredicto review (bloqueante/mayor/menor).

## Formato de salida

Lista de tests; resultado; checklist; recomendación merge sí/no.

## Criterios de aceptación

Trazabilidad AC→test; checklist de review del consumidor cubierto si aplica.

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.1.1 | 2026-08-24 | Approved (aprobación humana del director técnico) |
| 0.1.0 | 2026-08-24 | Extracción genérica; coding standards de stack fuera del core (ADR-008) |
