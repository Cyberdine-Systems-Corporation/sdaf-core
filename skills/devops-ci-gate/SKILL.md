---
name: devops-ci-gate
description: Playbook stub-aware para quality gates locales y huecos de CI. Usar al preparar automatización o checklist pre-merge sin inventar pipeline sin ADR/PBI.
---

# devops-ci-gate

| Campo | Valor |
|--------|--------|
| ID | devops-ci-gate |
| Versión | 0.3.0 |
| Estado | Draft |
| Prioridad | baja |
| Nota | stub-aware (agente DevOps stub) |
| Fecha | 2026-09-18 |
| Norma | [handbook/11](../../handbook/11-devops.md), [handbook/10](../../handbook/10-code-review-and-quality-gates.md) |

## Disparadores

- “Añadir CI”, quality gate automático, checklist pre-merge reproducible.

## Pasos

1. Gate **local** mínimo: ejecutar los QG de H10 con los comandos del runbook del consumidor; registrar resultados.
2. Documentar en worklog comandos y resultados (`devops-ci-gate@0.3.0`).
3. Si se pide pipeline cloud: exigir **PBI + ADR/spec Approved** (Gate 0); no inventar YAML “de regalo”.
4. Huecos futuros a registrar (no implementar sin mandato): cache de dependencias, test en PR, fail on coding-standards del consumidor, artefactos de contrato API.
5. Coordinar con `testing-review-pr` para dictamen humano.

> [!NOTE]
> 🛠️ CI cloud es opcional. El camino canónico es local (H11).

## Definition of Done

- [ ] Checklist local ejecutado o bloqueo justificado.
- [ ] Sin CI inventada fuera de alcance Approved.
- [ ] Worklog + siguiente paso (humano / DevOps cuando deje de ser stub).

## Restricciones

- Agente DevOps es **stub** en el core: no ampliar plataforma sin decisión humana.
- No secretos en workflows.
- No sustituir el runbook local por “pruébalo en cloud”.

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| 📖 | [H11](../../handbook/11-devops.md) | Local-first y runbook |
| 📖 | [H10](../../handbook/10-code-review-and-quality-gates.md) | QG a ejecutar |
| 📝 | [devops-agent](../../agents/devops-agent.md) | Contrato stub |
