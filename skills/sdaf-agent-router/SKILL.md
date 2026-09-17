---
name: sdaf-agent-router
description: Resuelve qué agente SDAF debe actuar leyendo AGENTS.md y el contrato. Usar ante ambigüedad de rol o al iniciar una tarea multi-agente.
---

# sdaf-agent-router

| Campo | Valor |
|--------|--------|
| ID | sdaf-agent-router |
| Versión | 0.2.1 |
| Estado | Approved |
| Prioridad | alta |
| Fecha | 2026-09-13 |
| Norma | [AGENTS.md.template](../../AGENTS.md.template), [handbook/06](../../handbook/06-ai-agent-framework.md) |

## Disparadores

- “¿Quién hace esto?”, mezcla de specs + código + UI en un solo pedido.
- Antes de producir artefactos fuera del rol actual.

## Pasos

1. Leer `AGENTS.md` del consumidor (o la plantilla) y `sdaf.config.yaml`: activos vs stubs.
2. Elegir agente por tipo de salida:
   - Specs/acceptance → Specification
   - ADR/boundaries/stack → Architecture
   - Tests/dictamen PR → Testing+Review
   - Implementación de dominio/UI/infra → agente declarado por config o pack de stack
3. Abrir contrato `agents/<nombre>.md` + prompt `prompts/agents/<nombre>.md`.
4. Leer **contexto autorizado** del contrato (índice de capas). Abrir esos artefactos; **no** concatenarlos en un mega-prompt ni en un mega-resumen de todos los agentes.
5. Si el trabajo cruza agentes → secuenciar handoffs; no fusionar salidas en un mega-diff sin worklog.
6. Invocar `sdaf-gate0` si hay implementación de producto.

## Definition of Done

- [ ] Agente (o secuencia) elegido y justificado.
- [ ] Contrato/prompt citados en worklog (`id@version`).
- [ ] Contexto autorizado leído como índice, no volcado.
- [ ] Sin salidas Outside del contrato sin handoff.

## Restricciones

- Stubs: no activar alcance Out; solo contrato/prompt listos.
- No aprobar norma Approved.
- El resumen de una línea no sustituye al prompt versionado.

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.2.1 | 2026-09-13 | Leer contexto autorizado; no mega-prompt |

## Relacionado

| Destino | Por qué |
|---------|---------|
| [AGENTS.md.template](../../AGENTS.md.template) | Inventario de agentes |
| [H07](../../handbook/07-prompt-engineering-standard.md) | No mega-prompt |
| [skills/README.md](../README.md) | Catálogo |
