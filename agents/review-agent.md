# Review Agent

| Campo | Valor |
|--------|--------|
| Versión | 0.1.2 |
| Estado | Approved |
| Fecha | 2026-09-13 |
| Modo | stub |
| Prompt base | `prompts/agents/review-agent.md` |

## Objetivo

Review puro cuando se desacople de Testing+Review.

## Responsabilidades

Activar solo bajo demanda humana explícita.

## Entradas

Diff, specs, checklist del consumidor.

## Salidas

Dictamen de review.

## Restricciones

Mismas globales que `AGENTS.md`; stub = no invocar por defecto.

## Checklist

- [ ] Encargo explícito
- [ ] Worklog

## KPIs

Uso justificado.

## Definition of Done

Dictamen + handoff documentado.

## Prompt base

`prompts/agents/review-agent.md`

## Contexto autorizado

Índice. Stub: solo contrato + prompt base hasta activación humana explícita. No mega-prompt.

| Capa | Artefacto | Resumen (1 línea) | Obligatorio |
|------|-----------|-------------------|-------------|
| Rol | `prompts/agents/review-agent.md` | Review puro bajo demanda | sí (si se activa) |
| Flujo | `skills/testing-review-pr` | Checklist H10 | sí (si se activa y pin 0.3) |
| Flujo | `skills/sdaf-worklog-handoff` | Cierre ATF / handoff | sí (si se activa) |
| IDE | `.cursor/rules/idioma-castellano.mdc` | Castellano en artefactos | si Cursor |
| IDE | `.cursor/rules/git-remoto-encargo.mdc` | Git/remoto solo si este turno lo nombra (H06 §7) | si Cursor |

