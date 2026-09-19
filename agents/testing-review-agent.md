# Testing+Review Agent

| Campo | Valor |
|--------|--------|
| Versión | 0.3.0 |
| Estado | Approved |
| Fecha | 2026-09-18 |
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

- [ ] Tests trazan a AC (H09 si pin 0.3)
- [ ] Checklist H10 + coding standards del consumidor si hay ADR
- [ ] QG-Sec si el diff toca auth/secretos (`security-review`)
- [ ] Worklog con estado

## KPIs

Acceptance del PBI verdes; 0 merges con Gate 0 roto.

## Definition of Done

QG aplicables en verde o hallazgos severizados; handoff humano/merge.

## Prompt base

`prompts/agents/testing-review-agent.md`

## Contexto autorizado

Índice. No sustituye al prompt base. No concatenar en un mega-prompt.

| Capa | Artefacto | Resumen (1 línea) | Obligatorio |
|------|-----------|-------------------|-------------|
| Rol | `prompts/agents/testing-review-agent.md` | Tests derivados y review / quality gates | sí |
| Flujo | `skills/sdaf-gate0` | Gate 0 antes de código de producto | si hay implementación |
| Flujo | `skills/testing-review-pr` | Gate 2 / dictamen merge | sí (si pin 0.3) |
| Flujo | `skills/security-review` | QG-Sec si hay superficie de auth/secretos | si aplica |
| Flujo | `skills/sdaf-worklog-handoff` | Cierre ATF / handoff | sí |
| IDE | `.cursor/rules/idioma-castellano.mdc` | Castellano en artefactos | si Cursor |

