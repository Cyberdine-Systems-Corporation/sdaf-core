# Domain Agent

| Campo | Valor |
|--------|--------|
| Versión | 0.1.1 |
| Estado | Approved |
| Fecha | 2026-08-24 |
| Modo | stub |
| Prompt base | `prompts/agents/domain-agent.md` |

## Objetivo

Modelar dominio (aggregates, invariantes) cuando se desacople de Application.

## Responsabilidades

Activar solo bajo demanda humana explícita.

## Entradas

Worklog + specs/ADRs del encargo puntual.

## Salidas

Código/modelo de dominio según el layout del consumidor.

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

`prompts/agents/domain-agent.md`
