# SDAF Core

Núcleo reutilizable del **Spec-Driven AI Development Framework** (SDAF): constitución del método, agentes, prompts, skills y plantillas.

![release](https://img.shields.io/badge/release-v0.2.1-2d6a4f) ![handbook](https://img.shields.io/badge/handbook-Approved-2d6a4f)

No contiene código ni specs de un producto concreto.

## Tres puertas

| | Si quieres… | Empieza aquí |
|--|-------------|--------------|
| 🛠️ | **Adoptar** el método en un repo | [Adopción y upgrade](docs/adopcion-y-upgrade.md) — pin a tag, `sdaf.config.yaml`, bootstrap |
| 📖 | **Entender la constitución** | [Handbook del método](handbook/README.md) — capítulos Approved 00–08 y apéndice A; Parte III 09–12 y B en Draft (0.3.0) |
| ⛔ | **Operar un PBI** | [Gate 0](skills/sdaf-gate0/SKILL.md) antes de código; [worklog / ATF](handbook/08-agent-traceability.md) para dejar evidencia |

🧭 Mapa de las ocho tareas: [`docs/mapa-navegacion.md`](docs/mapa-navegacion.md). Índice HOWTO: [`docs/README.md`](docs/README.md).

## Qué es

SDAF gobierna cómo un proyecto produce software con humanos y agentes IA:

1. El **knowledge** de expertos es fuente primaria de dominio (`knowledge/`, inmutable).
2. El **handbook** de este core es la constitución del **método**.
3. Las **especificaciones** en `specs/` del **repo consumidor** son la única verdad operativa para implementar.
4. Código y tests se derivan de esas specs.
5. Los agentes ejecutan el pipeline con trazabilidad (worklogs / ATF: registro auditable de cada iteración).

## Qué no es

- No es un producto (no hay `src/` de aplicación).
- No impone stack (.NET, Blazor, etc.). El stack se decide por ADR en el consumidor; un pack opcional (`sdaf-stack-*`) puede añadir playbooks técnicos (ver [`docs/contrato-pack-stack.md`](docs/contrato-pack-stack.md)). Pack de referencia: [`sdaf-stack-dotnet`](https://github.com/Cyberdine-Systems-Corporation/sdaf-stack-dotnet).
- No rellena `specs/`: exige que existan y estén Approved antes de implementar.

## Contenido (v0.2.x)

| | Ruta | Rol |
|--|------|-----|
| 📖 | `handbook/` | Constitución del método (00, Parte I 01–05, Parte II 06–08, Parte III 09–12 Draft, apéndices A–B) |
| 🛠️ | `docs/` | HOWTO adopción/upgrade, contrato de pack, mapa de navegación |
| 📝 | `templates/` | Spec, ADR, worklog, agente, prompt, skill, handbook de producto |
| | `agents/` + `prompts/` | Contratos y prompts genéricos |
| 🛠️ | `skills/` | Playbooks `sdaf-*`, `spec-draft-pbi`, `adr-propose` |
| | `AGENTS.md.template` | Router a materializar en el consumidor |
| | `sdaf.config.schema.yaml` | Catálogo humano de claves |
| | `sdaf.config.schema.json` | Schema validable |
| | `sdaf.config.example.yaml` | Copia de la config recomendada (escenario 01) |
| | `examples/` | Escenarios YAML + explicación de cada clave |
| | `.cursor/rules/idioma-castellano.mdc` | Regla IDE de idioma |

## Cómo adoptar (consumidor)

Guía completa: [`docs/adopcion-y-upgrade.md`](docs/adopcion-y-upgrade.md). Resumen:

1. Referenciar este repo (submodule en `.sdaf/` pinneado a tag `v0.2.1` recomendado; subtree o copia también documentados).
2. Crear `sdaf.config.yaml` copiando un escenario de [`examples/`](examples/README.md). Claves: [`sdaf.config.schema.yaml`](sdaf.config.schema.yaml) / [`sdaf.config.schema.json`](sdaf.config.schema.json).
3. Ejecutar skill `sdaf-bootstrap` (o materializar `AGENTS.md` y el árbol a mano).
4. Añadir handbook de **producto** (plantilla `templates/handbook-product.md`).
5. ⛔ Gate 0 (`skills/sdaf-gate0`) antes de código de producto.

`sdaf.version` en el YAML puede seguir en `0.2.0` hasta que el consumidor pinnee `v0.2.1`.

## Estado

| | Artefacto | Estado |
|--|-----------|--------|
| ✅ | Handbook del método | **Approved** 00–08 y A (v0.2.2); Parte III 09–12 y B **Draft** (v0.3.0) |
| ✅ | Agentes, prompts y skills 0.2 | **Approved** (v0.2.1) |
| 📝 | Skills/prompts Parte III | **Draft** (`testing-review-pr`, `security-review`, `devops-ci-gate`, review/quality/planning) |
| | Release del árbol (tag) | **v0.2.1** hasta Approve 0.3.0 y tag |

## Origen

Extraído como núcleo reutilizable (ADR-008) desde un laboratorio de gobernanza. El primer producto que lo inspiró no forma parte de este repositorio.
