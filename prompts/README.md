# Prompts — biblioteca versionada

Norma: [`handbook/07-prompt-engineering-standard.md`](../handbook/07-prompt-engineering-standard.md).  
Router: [`AGENTS.md.template`](../AGENTS.md.template).

## Catálogo v0.3

| Área | Contenido | Estado |
|------|-----------|--------|
| `system/` | [master-architect](system/master-architect.md) | Approved |
| `agents/` | [specification](agents/specification-agent.md), [architecture](agents/architecture-agent.md), [testing-review](agents/testing-review-agent.md), [product](agents/product-agent.md), [domain](agents/domain-agent.md), [application](agents/application-agent.md), [devops](agents/devops-agent.md), [review](agents/review-agent.md), [testing](agents/testing-agent.md) | Approved |
| `documentation/` | [handbook-author](documentation/handbook-author.md), [specification-author](documentation/specification-author.md), [adr-author](documentation/adr-author.md) | Approved |
| `review/` | [code-review](review/code-review.md), [architecture-review](review/architecture-review.md), [specification-review](review/specification-review.md) | Draft |
| `quality/` | [quality-gates](quality/quality-gates.md), [testing-strategy](quality/testing-strategy.md) | Draft |
| `planning/` | [sprint-planning](planning/sprint-planning.md), [backlog-refinement](planning/backlog-refinement.md), [roadmap-planning](planning/roadmap-planning.md) | Draft |

Citar `ID@version` en worklogs. Los Draft (Parte III) no son norma Approved.

## Relacionado

| Destino | Por qué |
|---------|---------|
| [H07](../handbook/07-prompt-engineering-standard.md) | Economía de tokens; no mega-prompt |
| [handbook-author](documentation/handbook-author.md) | Enmendar capítulos |
| [agents/README.md](../agents/README.md) | Contratos que apuntan a estos prompts |
| [H10](../handbook/10-code-review-and-quality-gates.md) | Prompts review/quality (Draft 0.3.0) |
