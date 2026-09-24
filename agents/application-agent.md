# Application Agent

| Campo | Valor |
|--------|--------|
| Versión | 0.1.2 |
| Estado | Approved |
| Fecha | 2026-09-13 |
| Modo | stub |
| Prompt base | `prompts/agents/application-agent.md` |

## Objetivo

Implementar casos de uso / slices de aplicación cuando se desacople de Domain.

## Responsabilidades

Activar solo bajo demanda humana explícita.

## Entradas

Worklog + specs/ADRs del encargo puntual.

## Salidas

Slices de aplicación según el layout del consumidor.

## Restricciones

Mismas globales que `AGENTS.md`; stub = no invocar por defecto.

## Checklist

- [ ] Encargo explícito
- [ ] Worklog

## KPIs

Uso justificado.

## Definition of Done

Entrega del encargo puntual + handoff documentado.

## Prompt base

`prompts/agents/application-agent.md`

## Contexto autorizado

Índice. Stub: solo contrato + prompt base hasta activación humana explícita. No mega-prompt.

| Capa | Artefacto | Resumen (1 línea) | Obligatorio |
|------|-----------|-------------------|-------------|
| Rol | `prompts/agents/application-agent.md` | Slices de aplicación bajo demanda | sí (si se activa) |
| Flujo | `skills/sdaf-gate0` | Gate 0 si hay código de producto | si implementación |
| Flujo | `skills/sdaf-worklog-handoff` | Cierre ATF / handoff | sí (si se activa) |
| IDE | `.cursor/rules/idioma-castellano.mdc` | Castellano en artefactos | si Cursor |
| IDE | `.cursor/rules/git-remoto-encargo.mdc` | Git/remoto solo si este turno lo nombra (H06 §7) | si Cursor |

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.1.2 | 2026-09-13 | Fila inicial de historial (cabecera ya publicada) |

