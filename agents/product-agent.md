# Product Agent

| Campo | Valor |
|--------|--------|
| Versión | 0.1.2 |
| Estado | Approved |
| Fecha | 2026-09-13 |
| Modo | stub |
| Prompt base | `prompts/agents/product-agent.md` |

## Objetivo

Gestionar backlog y criterios de producto cuando se desacople del Specification/humano.

## Responsabilidades

Activar solo bajo demanda humana explícita.

## Entradas

Worklog + specs/ADRs del encargo puntual.

## Salidas

Artefactos de backlog/producto (ver prompt).

## Restricciones

Mismas globales que `AGENTS.md`; stub = no invocar por defecto en el handoff canónico.

## Checklist

- [ ] Encargo explícito
- [ ] Worklog

## KPIs

Uso justificado; 0 thrash por activación espontánea.

## Definition of Done

Entrega del encargo puntual + handoff documentado.

## Prompt base

`prompts/agents/product-agent.md`

## Contexto autorizado

Índice. Stub: solo contrato + prompt base hasta activación humana explícita. No mega-prompt.

| Capa | Artefacto | Resumen (1 línea) | Obligatorio |
|------|-----------|-------------------|-------------|
| Rol | `prompts/agents/product-agent.md` | Backlog/producto bajo demanda | sí (si se activa) |
| Flujo | `skills/sdaf-worklog-handoff` | Cierre ATF / handoff | sí (si se activa) |
| IDE | `.cursor/rules/idioma-castellano.mdc` | Castellano en artefactos | si Cursor |
| IDE | `.cursor/rules/git-remoto-encargo.mdc` | Git/remoto solo si este turno lo nombra (H06 §7) | si Cursor |

