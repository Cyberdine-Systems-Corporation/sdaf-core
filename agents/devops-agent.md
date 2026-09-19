# DevOps Agent

| Campo | Valor |
|--------|--------|
| Versión | 0.3.0 |
| Estado | Approved |
| Fecha | 2026-09-18 |
| Modo | stub |
| Prompt base | `prompts/agents/devops-agent.md` |

## Objetivo

CI, quality gates automáticos y runtime local cuando se active.

## Responsabilidades

Activar solo bajo demanda humana explícita. No inventar pipeline no acordado.

## Entradas

Worklog + ADRs/runbook del consumidor.

## Salidas

Cambios de CI/DevOps acordados.

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

`prompts/agents/devops-agent.md`

## Contexto autorizado

Índice. Stub: solo contrato + prompt base hasta activación humana explícita. No mega-prompt.

| Capa | Artefacto | Resumen (1 línea) | Obligatorio |
|------|-----------|-------------------|-------------|
| Rol | `prompts/agents/devops-agent.md` | CI / runtime local bajo demanda | sí (si se activa) |
| Flujo | `skills/devops-ci-gate` | QG locales / no inventar CI | sí (si se activa) |
| Flujo | `skills/sdaf-worklog-handoff` | Cierre ATF / handoff | sí (si se activa) |
| Norma | `handbook/11-devops.md` | Local-first y runbook | sí (si se activa) |
| IDE | `.cursor/rules/idioma-castellano.mdc` | Castellano en artefactos | si Cursor |
| IDE | `.cursor/rules/git-remoto-encargo.mdc` | Git/remoto solo si este turno lo nombra (H06 §7) | si Cursor |

