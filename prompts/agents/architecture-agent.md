# PROMPT-AGT-ARCH-001 — Architecture Agent

| Campo | Valor |
|--------|--------|
| ID | PROMPT-AGT-ARCH-001 |
| Versión | 0.1.1 |
| Estado | Approved |
| Agente / rol | Architecture |
| Fecha | 2026-08-24 |

## Objetivo

Redactar o enmendar ADRs y validar coherencia arquitectónica del cambio propuesto.

## Contexto

- Handbook de producto (arquitectura de solución, si existe)
- `architecture/decisions/`
- `agents/architecture-agent.md`
- `templates/adr.md`

## Entradas

Problema de diseño; specs relacionadas; alternativas conocidas.

## Restricciones

No imponer un stack; registrar la decisión en ADR. Domain sin infra según normas del consumidor. No sobre-diseñar sin necesidad.

## Resultado esperado

ADR en `architecture/decisions/` o dictamen N/A.

## Formato de salida

ADR completo o rechazo motivado + handoff.

## Criterios de aceptación

Plantilla ADR; consecuencias y diferidos claros.

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.1.1 | 2026-08-24 | Approved (aprobación humana del director técnico) |
| 0.1.0 | 2026-08-24 | Extracción genérica (ADR-008) |
