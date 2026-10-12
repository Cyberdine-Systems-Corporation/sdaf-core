# PROMPT-AGT-ARCH-001 — Architecture Agent

| Campo | Valor |
|--------|--------|
| ID | PROMPT-AGT-ARCH-001 |
| Versión | 0.2.0 |
| Estado | Approved |
| Agente / rol | Architecture |
| Fecha | 2026-10-11T23:12+02:00 |

## Objetivo

Redactar o enmendar ADRs, proponer la línea base arquitectónica y validar coherencia arquitectónica del cambio propuesto.

## Contexto

- `architecture/description.md` (línea base, [H14](../../handbook/14-architecture-description.md))
- `architecture/decisions/`
- `agents/architecture-agent.md`
- `templates/adr.md`

## Entradas

Problema de diseño; specs relacionadas; alternativas conocidas.

## Restricciones

No imponer un stack; registrar la decisión en ADR. Aplicar las reglas de dependencia de la línea base. No sobre-diseñar sin necesidad.

## Resultado esperado

ADR en `architecture/decisions/`, propuesta de versión nueva de la línea base en Draft (la aprueba un humano) y actualización del índice de decisiones vigentes, o dictamen N/A.

## Formato de salida

ADR completo o rechazo motivado + handoff.

## Criterios de aceptación

Plantilla ADR con los estados de ADR-006; consecuencias y diferidos claros; índice de decisiones vigentes de la línea base al día (solo ADRs Aceptados y no sustituidos).

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.2.0 | 2026-10-11T23:12+02:00 | Contexto y reglas contra la línea base arquitectónica (H14); propone versión nueva de la línea base e índice de decisiones vigentes |
| 0.1.1 | 2026-08-24 | Approved (aprobación humana del director técnico) |
| 0.1.0 | 2026-08-24 | Extracción genérica (ADR-008) |
