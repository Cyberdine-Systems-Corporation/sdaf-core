# Skills — playbooks SDAF (core)

| Campo | Valor |
|--------|--------|
| Versión | 0.3.1 |
| Estado | Approved |
| Fecha | 2026-09-19 |
| Norma | `handbook/03`, `handbook/06` §6, `handbook/07`, `AGENTS.md.template` |

Playbooks operativos reutilizables. Viven en **`skills/`**. **No** dependen de Cursor ni de `.cursor/skills/`.

Citar `skill-id@version` en worklogs del consumidor.

> [!CAUTION]
> ⛔ No saltar Gate 0. No aprobar handbook, specs ni ADR.

## Catálogo v0.3.x

| | ID | Prioridad | Estado | Ruta |
|--|----|-----------|--------|------|
| ⛔ | `sdaf-gate0` | alta | Approved | [sdaf-gate0/SKILL.md](sdaf-gate0/SKILL.md) |
| 📝 | `sdaf-worklog-handoff` | alta | Approved | [sdaf-worklog-handoff/SKILL.md](sdaf-worklog-handoff/SKILL.md) |
| 🧭 | `sdaf-agent-router` | alta | Approved | [sdaf-agent-router/SKILL.md](sdaf-agent-router/SKILL.md) |
| 🛠️ | `sdaf-bootstrap` | alta | Approved | [sdaf-bootstrap/SKILL.md](sdaf-bootstrap/SKILL.md) |
| 📝 | `testing-review-pr` | alta | Approved | [testing-review-pr/SKILL.md](testing-review-pr/SKILL.md) |
| 📝 | `spec-draft-pbi` | media | Approved | [spec-draft-pbi/SKILL.md](spec-draft-pbi/SKILL.md) |
| 📝 | `adr-propose` | media | Approved | [adr-propose/SKILL.md](adr-propose/SKILL.md) |
| 🛠️ | `sdaf-upgrade` | media | Approved | [sdaf-upgrade/SKILL.md](sdaf-upgrade/SKILL.md) |
| ⛔ | `security-review` | media | Approved | [security-review/SKILL.md](security-review/SKILL.md) |
| 🛠️ | `devops-ci-gate` | baja | Approved | [devops-ci-gate/SKILL.md](devops-ci-gate/SKILL.md) |

Skills de stack o dominio no forman parte de este core.

## Restricciones

- No aprobar handbook/specs/ADR.
- No saltar Gate 0.
- No secretos en el repo.
- Castellano en artefactos de ingeniería.
- No commit local ni escritura al remoto (push, tags, releases, merge, PR, APIs, CI que escriba el repo) sin petición humana explícita (H06 §7). La excepción del consumidor debe enumerar qué permite.
- Plantilla: [`templates/skill.md`](../templates/skill.md).

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| 📖 | [H06 §6](../handbook/06-ai-agent-framework.md#6-skills) | Skills vs contratos vs rules |
| ⛔ | [sdaf-gate0](sdaf-gate0/SKILL.md) | STOP antes de código de producto |
| 🛠️ | [sdaf-bootstrap](sdaf-bootstrap/SKILL.md) | Primera materialización |
| 🛠️ | [docs/adopcion-y-upgrade.md](../docs/adopcion-y-upgrade.md) | Pin y upgrade |
| 📖 | [H10](../handbook/10-code-review-and-quality-gates.md) | testing-review-pr / QG |
