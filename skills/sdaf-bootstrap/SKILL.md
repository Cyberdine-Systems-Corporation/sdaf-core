---
name: sdaf-bootstrap
description: Inicializa un repo consumidor SDAF (config, AGENTS.md, árbol vacío, worklog). Usar al adoptar sdaf-core o al abrir un producto nuevo sin estructura.
---

# sdaf-bootstrap

| Campo | Valor |
|--------|--------|
| ID | sdaf-bootstrap |
| Versión | 0.5.0 |
| Estado | Approved |
| Prioridad | alta |
| Fecha | 2026-10-12T18:23+02:00 |
| Norma | [handbook/03](../../handbook/03-repository-organization.md), [handbook/05](../../handbook/05-development-workflow.md) §2, [handbook/14](../../handbook/14-architecture-description.md), [ADR-005](../../architecture/decisions/ADR-005-linea-base-arquitectonica.md), [docs/adopcion-y-upgrade.md](../../docs/adopcion-y-upgrade.md) |

## Disparadores

- “Adoptar SDAF”, “bootstrap del repo”, “inicializar consumidor”.
- Repo sin `sdaf.config.yaml` / sin árbol normativo.

## Pasos

1. Elegir escenario de [`examples/`](../../examples/README.md) (default [`01-default-core.yaml`](../../examples/01-default-core.yaml)).
2. Escribir `sdaf.config.yaml` en la raíz del consumidor (`project.name`, `sdaf.version` = versión del core pinneada). `tooling` es opcional: declarar `tooling.gentle_ai` solo si el equipo adopta gentle-ai ([`docs/integracion-gentle-ai.md`](../../docs/integracion-gentle-ai.md)).
3. Materializar `AGENTS.md` desde [`AGENTS.md.template`](../../AGENTS.md.template): sustituir `{{PROJECT_NAME}}` y alinear active/stubs/fusions con la config. Conservar la sección «Tooling externo (opcional)» solo si `tooling.gentle_ai` ≠ `null`; si no, borrarla.
4. Crear árbol vacío según [H03](../../handbook/03-repository-organization.md): `knowledge/raw`, `knowledge/curated`, `specs/{product,domain,application,integration,acceptance}`, `architecture/decisions`, `backlog`, `worklogs`, `agents`, `prompts`, `skills`, `templates`, `docs`; stub de handbook de producto desde [`templates/handbook-product.md`](../../templates/handbook-product.md). Solo si `sdaf.version` es `0.5.0` o superior (la línea es opt-in: con una versión anterior, p. ej. `0.4.0`, no se crea), crear `architecture/description.md` copiando [`templates/architecture-description.md`](../../templates/architecture-description.md) ([H14](../../handbook/14-architecture-description.md)): Estado `Draft`, Fecha real (cabecera e historial), sin el aviso de uso, cada sección con `N/A: pendiente de redactar` y sin filas de ejemplo.
5. Si `stack.pack` ≠ `null`, verificar [`docs/contrato-pack-stack.md`](../../docs/contrato-pack-stack.md) y materializar aportes del pack + core con symlinks relativos en el consumidor (script documentado `scripts/materialize-submodules.ps1` o manual según [`docs/adopcion-y-upgrade.md`](../../docs/adopcion-y-upgrade.md)); opcional `.cursor/skills/` → submodule.
6. Copiar reglas IDE si aplica (`.cursor/rules/idioma-castellano.mdc` y `.cursor/rules/git-remoto-encargo.mdc` vía materialización). **No** crear código de producto en `src/` sin Gate 0. Bootstrap **no** incluye commit ni remoto salvo que este turno lo nombre (H06 §7).
7. Ejecutar checklist Gate 0 en vacío → **STOP** esperado por G0.1 (sin specs Approved) y, si `sdaf.version` es `0.5.0` o superior, también por G0.6 (línea base en Draft: la aprueba un humano; [H05 §3](../../handbook/05-development-workflow.md)). Abrir worklog de bootstrap, registrar cada motivo del STOP y citar `sdaf-bootstrap@0.5.0`.

## Definition of Done

- [ ] `sdaf.config.yaml` y `AGENTS.md` presentes y coherentes (sección de tooling externo solo si `tooling.gentle_ai` ≠ `null`).
- [ ] Árbol H03 creado (carpetas vacías o con `.gitkeep` según convención del consumidor).
- [ ] Si `sdaf.version` es `0.5.0` o superior: `architecture/description.md` creada en estado Draft desde la plantilla, sin aprobar.
- [ ] Worklog de bootstrap con el STOP de Gate 0 documentado y sus motivos (G0.1 y, en `0.5.0` o superior, G0.6).
- [ ] Sin implementación de producto.

## Restricciones

- No aprobar handbook/specs/ADR ni la línea base arquitectónica.
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
| 0.5.0 | 2026-10-12T18:23+02:00 | Con `sdaf.version` `0.5.0` o superior crea la línea base arquitectónica en Draft (H14), añade `specs/integration` al árbol y el STOP de Gate 0 cita G0.1 y G0.6 |
| 0.4.2 | 2026-09-26T17:27+02:00 | `tooling` opcional en la config y sección de tooling externo en `AGENTS.md` solo si se declara (ADR-004) |
| 0.2.1 | 2026-09-19 | Materializar `git-remoto-encargo`; bootstrap no implica git (H06 §7) |
| 0.2.0 | 2026-08-25 | Primera versión en el core |
