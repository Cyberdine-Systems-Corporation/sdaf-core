# Review Agent

| Campo | Valor |
|--------|--------|
| Versión | 0.1.1 |
| Estado | Approved |
| Fecha | 2026-08-24 |
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
