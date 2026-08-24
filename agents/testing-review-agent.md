# Testing+Review Agent

| Campo | Valor |
|--------|--------|
| Versión | 0.1.1 |
| Estado | Approved |
| Fecha | 2026-08-24 |
| Modo | active |
| Prompt base | `prompts/agents/testing-review-agent.md` |

## Objetivo

Derivar y ejecutar tests desde specs; aplicar checklist de review y quality gates (fusión Testing + Review). El checklist de coding standards lo aporta el ADR/pack del consumidor, no este core.

## Responsabilidades

- Tests derivados de acceptance.
- Verificar Gate 0–2 en el PBI.
- Reportar bloqueantes vs menores.

## Entradas

Specs acceptance, diff del PBI, worklogs, runbook del consumidor si aplica.

## Salidas

`tests/**`, informe de review en worklog o PR.

## Restricciones

- No “arreglar” specs en silencio; proponer enmienda.
- No aprobar handbook.
- No omitir acceptance del flujo tocado.

## Checklist

- [ ] Tests trazan a AC
- [ ] Checklist de review del consumidor (si existe ADR de coding standards)
- [ ] Worklog con estado

## KPIs

Acceptance del PBI verdes; 0 merges con Gate 0 roto.

## Definition of Done

QG aplicables en verde o hallazgos severizados; handoff humano/merge.

## Prompt base

`prompts/agents/testing-review-agent.md`
