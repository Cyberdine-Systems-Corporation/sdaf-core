# Skills — playbooks SDAF (core)

| Campo | Valor |
|--------|--------|
| Versión | 0.1.1 |
| Estado | Approved |
| Fecha | 2026-08-24 |
| Norma | `handbook/07`, `handbook/13` §6, `handbook/14`, `AGENTS.md.template` |

Playbooks operativos reutilizables. Viven en **`skills/`**. **No** dependen de Cursor ni de `.cursor/skills/`.

Citar `skill-id@version` en worklogs del consumidor.

## Catálogo v0.1

| ID | Prioridad | Ruta |
|----|-----------|------|
| `sdaf-gate0` | alta | [sdaf-gate0/SKILL.md](sdaf-gate0/SKILL.md) |
| `sdaf-worklog-handoff` | alta | [sdaf-worklog-handoff/SKILL.md](sdaf-worklog-handoff/SKILL.md) |
| `sdaf-agent-router` | alta | [sdaf-agent-router/SKILL.md](sdaf-agent-router/SKILL.md) |
| `spec-draft-pbi` | media | [spec-draft-pbi/SKILL.md](spec-draft-pbi/SKILL.md) |
| `adr-propose` | media | [adr-propose/SKILL.md](adr-propose/SKILL.md) |

Skills de stack o dominio no forman parte de este core.

## Restricciones

- No aprobar handbook/specs/ADR.
- No saltar Gate 0.
- No secretos en el repo.
- Castellano en artefactos de ingeniería.
- Plantilla: [`templates/skill.md`](../templates/skill.md).
