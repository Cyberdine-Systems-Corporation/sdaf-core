# Product Agent

| Campo | Valor |
|--------|--------|
| Versión | 0.1.1 |
| Estado | Approved |
| Fecha | 2026-08-24 |
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
