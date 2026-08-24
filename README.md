# SDAF Core

Núcleo reutilizable del **Spec-Driven AI Development Framework** (SDAF): constitución del método, agentes, prompts, skills y plantillas.

Versión de release: **0.1.0**. No contiene código ni specs de un producto concreto.

## Qué es

SDAF gobierna cómo un proyecto produce software con humanos y agentes IA:

1. El **knowledge** de expertos es fuente primaria de dominio (`knowledge/`, inmutable).
2. El **handbook** de este core es la constitución del **método**.
3. Las **especificaciones** en `specs/` del **repo consumidor** son la única verdad operativa para implementar.
4. Código y tests se derivan de esas specs.
5. Los agentes ejecutan el pipeline con trazabilidad (worklogs).

## Qué no es

- No es un producto (no hay `src/` de aplicación).
- No impone stack (.NET, Blazor, etc.). El stack se decide por ADR en el consumidor; un pack opcional (`sdaf-stack-*`) puede añadir playbooks técnicos.
- No rellena `specs/`: exige que existan y estén Approved antes de implementar.

## Contenido (v0.1)

| Ruta | Rol |
|------|-----|
| `handbook/` | Constitución del método (preface, Parte II, Parte IV, apéndice B) |
| `templates/` | Spec, ADR, worklog, agente, prompt, skill |
| `agents/` + `prompts/` | Contratos y prompts genéricos |
| `skills/` | Playbooks `sdaf-*`, `spec-draft-pbi`, `adr-propose` |
| `AGENTS.md.template` | Router a materializar en el consumidor |
| `sdaf.config.schema.yaml` | Catálogo de claves de `sdaf.config.yaml` |
| `sdaf.config.example.yaml` | Copia de la config recomendada (escenario 01) |
| `examples/` | Escenarios YAML + explicación de cada clave |
| `.cursor/rules/idioma-castellano.mdc` | Regla IDE de idioma |

## Cómo adoptar (consumidor)

1. Copiar o referenciar este repo (submodule / subtree / template; el mecanismo de upgrade se documentará en v0.2).
2. Crear `sdaf.config.yaml` copiando un escenario de [`examples/`](examples/README.md) (por defecto [`examples/01-default-core.yaml`](examples/01-default-core.yaml)). Claves: [`sdaf.config.schema.yaml`](sdaf.config.schema.yaml).
3. Materializar `AGENTS.md` desde la plantilla (sustituir `{{PROJECT_NAME}}` y la lista de agentes activos).
4. Añadir handbook de **producto** (charter, MVP, arquitectura de solución) en el repo consumidor.
5. Crear `knowledge/`, `specs/`, `architecture/decisions/`, `backlog/`, `worklogs/` vacíos o con el contenido del producto.
6. Gate 0 (`skills/sdaf-gate0`) antes de código de producto.

## Estado

- Handbook del método: **Approved** (v0.1.1)
- Agentes, prompts y skills: **Approved** (v0.1.1)
- Release del árbol: **v0.1.0**

## Origen

Extraído como núcleo reutilizable (ADR-008) desde un laboratorio de gobernanza. El primer producto que lo inspiró no forma parte de este repositorio.
