# SDAF Core

Núcleo reutilizable del **Spec-Driven AI Development Framework** (SDAF): constitución del método, agentes, prompts, skills y plantillas.

Versión de release: **0.2.0**. No contiene código ni specs de un producto concreto.

## Qué es

SDAF gobierna cómo un proyecto produce software con humanos y agentes IA:

1. El **knowledge** de expertos es fuente primaria de dominio (`knowledge/`, inmutable).
2. El **handbook** de este core es la constitución del **método**.
3. Las **especificaciones** en `specs/` del **repo consumidor** son la única verdad operativa para implementar.
4. Código y tests se derivan de esas specs.
5. Los agentes ejecutan el pipeline con trazabilidad (worklogs).

## Qué no es

- No es un producto (no hay `src/` de aplicación).
- No impone stack (.NET, Blazor, etc.). El stack se decide por ADR en el consumidor; un pack opcional (`sdaf-stack-*`) puede añadir playbooks técnicos (ver [`docs/contrato-pack-stack.md`](docs/contrato-pack-stack.md)).
- No rellena `specs/`: exige que existan y estén Approved antes de implementar.

## Contenido (v0.2)

| Ruta | Rol |
|------|-----|
| `handbook/` | Constitución del método (00, Parte I 01–05, Parte II 06–08, apéndice A) |
| `docs/` | HOWTO adopción/upgrade y contrato de pack |
| `templates/` | Spec, ADR, worklog, agente, prompt, skill, handbook de producto |
| `agents/` + `prompts/` | Contratos y prompts genéricos |
| `skills/` | Playbooks `sdaf-*`, `spec-draft-pbi`, `adr-propose` |
| `AGENTS.md.template` | Router a materializar en el consumidor |
| `sdaf.config.schema.yaml` | Catálogo humano de claves |
| `sdaf.config.schema.json` | Schema validable |
| `sdaf.config.example.yaml` | Copia de la config recomendada (escenario 01) |
| `examples/` | Escenarios YAML + explicación de cada clave |
| `.cursor/rules/idioma-castellano.mdc` | Regla IDE de idioma |

## Cómo adoptar (consumidor)

Guía completa: [`docs/adopcion-y-upgrade.md`](docs/adopcion-y-upgrade.md). Resumen:

1. Referenciar este repo (submodule en `.sdaf/` pinneado a tag `v0.2.0` recomendado; subtree o copia también documentados).
2. Crear `sdaf.config.yaml` copiando un escenario de [`examples/`](examples/README.md). Claves: [`sdaf.config.schema.yaml`](sdaf.config.schema.yaml) / [`sdaf.config.schema.json`](sdaf.config.schema.json).
3. Ejecutar skill `sdaf-bootstrap` (o materializar `AGENTS.md` y el árbol a mano).
4. Añadir handbook de **producto** (plantilla `templates/handbook-product.md`).
5. Gate 0 (`skills/sdaf-gate0`) antes de código de producto.

## Estado

- Handbook del método: **Approved** (v0.2.0)
- Agentes, prompts y skills: **Approved** (v0.2.0)
- Release del árbol: **v0.2.0**

## Origen

Extraído como núcleo reutilizable (ADR-008) desde un laboratorio de gobernanza. El primer producto que lo inspiró no forma parte de este repositorio.
