# PROMPT-QUA-TEST-001 — Testing Strategy

| Campo | Valor |
|--------|--------|
| ID | PROMPT-QUA-TEST-001 |
| Versión | 0.3.0 |
| Estado | Draft |
| Agente / rol | quality / Testing+Review |
| Fecha | 2026-09-18 |

## Objetivo

Definir o ajustar la estrategia de tests de un PBI según [H09](../../handbook/09-testing-framework.md).

## Contexto

- [H09](../../handbook/09-testing-framework.md); specs de acceptance del PBI
- [H04](../../handbook/04-specification-standard.md)

## Entradas

PBI; riesgos; capas afectadas.

## Restricciones

Priorizar dominio + acceptance del flujo tocado; UI E2E no es bloqueante único. Herramientas = ADR/pack del consumidor.

## Resultado esperado

Plan de tests por nivel de la pirámide.

## Formato de salida

Tabla nivel → casos → prioridad.

## Criterios de aceptación

Trazable a ACs del PBI; no exige cobertura de líneas como KPI.

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.3.0 | 2026-09-18 | Draft: remap extract cap. 16 → H09; sin dominio de producto |
