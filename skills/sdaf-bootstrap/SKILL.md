---
name: sdaf-bootstrap
description: Inicializa un repo consumidor SDAF (config, AGENTS.md, árbol vacío, worklog). Usar al adoptar sdaf-core o al abrir un producto nuevo sin estructura.
---

# sdaf-bootstrap

| Campo | Valor |
|--------|--------|
| ID | sdaf-bootstrap |
| Versión | 0.2.1 |
| Estado | Approved |
| Prioridad | alta |
| Fecha | 2026-09-19 |
| Norma | [handbook/03](../../handbook/03-repository-organization.md), [handbook/05](../../handbook/05-development-workflow.md) §2, [docs/adopcion-y-upgrade.md](../../docs/adopcion-y-upgrade.md) |

## Disparadores

- “Adoptar SDAF”, “bootstrap del repo”, “inicializar consumidor”.
- Repo sin `sdaf.config.yaml` / sin árbol normativo.

## Pasos

1. Elegir escenario de [`examples/`](../../examples/README.md) (default [`01-default-core.yaml`](../../examples/01-default-core.yaml)).
2. Escribir `sdaf.config.yaml` en la raíz del consumidor (`project.name`, `sdaf.version` = versión del core pinneada).
3. Materializar `AGENTS.md` desde [`AGENTS.md.template`](../../AGENTS.md.template): sustituir `{{PROJECT_NAME}}` y alinear active/stubs/fusions con la config.
4. Crear árbol vacío según [H03](../../handbook/03-repository-organization.md): `knowledge/raw`, `knowledge/curated`, `specs/{product,domain,application,acceptance}`, `architecture/decisions`, `backlog`, `worklogs`, `agents`, `prompts`, `skills`, `templates`, `docs`; stub de handbook de producto desde [`templates/handbook-product.md`](../../templates/handbook-product.md).
5. Si `stack.pack` ≠ `null`, verificar [`docs/contrato-pack-stack.md`](../../docs/contrato-pack-stack.md) y materializar aportes del pack + core con symlinks relativos en el consumidor (script documentado `scripts/materialize-submodules.ps1` o manual según [`docs/adopcion-y-upgrade.md`](../../docs/adopcion-y-upgrade.md)); opcional `.cursor/skills/` → submodule.
6. Copiar reglas IDE si aplica (`.cursor/rules/idioma-castellano.mdc` y `.cursor/rules/git-remoto-encargo.mdc` vía materialización). **No** crear código de producto en `src/` sin Gate 0. Bootstrap **no** incluye commit ni remoto salvo que este turno lo nombre (H06 §7).
7. Ejecutar checklist Gate 0 en vacío → **STOP** esperado (sin specs Approved). Abrir worklog de bootstrap y citar `sdaf-bootstrap@0.2.1`.

## Definition of Done

- [ ] `sdaf.config.yaml` y `AGENTS.md` presentes y coherentes.
- [ ] Árbol H03 creado (carpetas vacías o con `.gitkeep` según convención del consumidor).
- [ ] Worklog de bootstrap con STOP de Gate 0 documentado.
- [ ] Sin implementación de producto.

## Restricciones

- No aprobar handbook/specs/ADR.
- No saltar Gate 0 “para empezar ya el código”.
- Castellano en artefactos de ingeniería.
- No commit ni escritura al remoto sin petición **en este turno** (H06 §7).

## Relacionado

| Destino | Por qué |
|---------|---------|
| [docs/adopcion-y-upgrade.md](../../docs/adopcion-y-upgrade.md) | Pin y pasos canónicos |
| [sdaf-gate0](../sdaf-gate0/SKILL.md) | STOP esperado en repo vacío |

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.2.1 | 2026-09-19 | Materializar `git-remoto-encargo`; bootstrap no implica git (H06 §7) |
| 0.2.0 | 2026-08-25 | Primera versión en el core |
