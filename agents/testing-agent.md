# Testing Agent

| Campo | Valor |
|--------|--------|
| Versión | 0.1.2 |
| Estado | Approved |
| Fecha | 2026-09-13 |
| Modo | stub |
| Prompt base | `prompts/agents/testing-agent.md` |

## Objetivo

Tests derivados de specs cuando se desacople de Testing+Review.

## Responsabilidades

Activar solo bajo demanda humana explícita.

## Entradas

Specs acceptance, diff.

## Salidas

`tests/**`.

## Restricciones

Mismas globales que `AGENTS.md`; stub = no invocar por defecto.

## Checklist

- [ ] Encargo explícito
- [ ] Worklog

## KPIs

Uso justificado.

## Definition of Done

Tests trazables + handoff documentado.

## Prompt base

`prompts/agents/testing-agent.md`

## Contexto autorizado

Índice. Stub: solo contrato + prompt base hasta activación humana explícita. No mega-prompt.

| Capa | Artefacto | Resumen (1 línea) | Obligatorio |
|------|-----------|-------------------|-------------|
| Rol | `prompts/agents/testing-agent.md` | Tests derivados bajo demanda | sí (si se activa) |
| Norma | `handbook/09-testing-framework.md` | Pirámide y tests desde specs | sí (si se activa y pin 0.3) |
| Flujo | `skills/sdaf-worklog-handoff` | Cierre ATF / handoff | sí (si se activa) |
| IDE | `.cursor/rules/idioma-castellano.mdc` | Castellano en artefactos | si Cursor |
| IDE | `.cursor/rules/git-remoto-encargo.mdc` | Git/remoto solo si este turno lo nombra (H06 §7) | si Cursor |

