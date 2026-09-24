<p align="center">
  <img src="docs/assets/sdaf-core-icon-build.gif" alt="SDAF Core — construcción del mark" width="160" height="160" />
</p>

# SDAF Core

Núcleo reutilizable del **Spec-Driven AI Development Framework** (SDAF): constitución del método, agentes, prompts, skills y plantillas.

![release](https://img.shields.io/badge/release-v0.4.0-2d6a4f) ![handbook](https://img.shields.io/badge/handbook-Approved-2d6a4f)

No contiene código ni specs de un producto concreto.

## Tres puertas

| | Si quieres… | Empieza aquí |
|--|-------------|--------------|
| 🛠️ | **Adoptar** el método en un repo | [Adopción y upgrade](docs/adopcion-y-upgrade.md) — pin a tag, `sdaf.config.yaml`, bootstrap |
| 📖 | **Entender la constitución** | [Handbook del método](handbook/README.md) — capítulos Approved 00–12 y apéndices A–B (0.3.3) |
| ⛔ | **Operar un PBI** | [Gate 0](skills/sdaf-gate0/SKILL.md) antes de código; [worklog / ATF](handbook/08-agent-traceability.md) para dejar evidencia |

🧭 Mapa de las ocho tareas: [`docs/mapa-navegacion.md`](docs/mapa-navegacion.md). Índice HOWTO: [`docs/README.md`](docs/README.md). Identidad visual: [`docs/branding.md`](docs/branding.md).

Contribuir: [`CONTRIBUTING.md`](CONTRIBUTING.md). Avisos de seguridad de **este** repo: [`SECURITY.md`](SECURITY.md). Historial del método: [`CHANGELOG.md`](CHANGELOG.md) (apunta a [`handbook/CHANGELOG.md`](handbook/CHANGELOG.md)). ADRs del core: [`architecture/decisions/`](architecture/decisions/README.md). Action de validación para consumidores: [`.github/actions/validate-sdaf/`](.github/actions/validate-sdaf/README.md).

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

## Contenido (v0.4.0)

| | Ruta | Rol |
|--|------|-----|
| 📖 | `handbook/` | Constitución del método (00, Parte I 01–05, Parte II 06–08, Parte III 09–12, apéndices A–B) |
| 🛠️ | `docs/` | HOWTO adopción/upgrade, contrato de pack, mapa, [branding](docs/branding.md) |
| 📝 | `templates/` | Spec, ADR, worklog, agente, prompt, skill, handbook de producto |
| | `agents/` + `prompts/` | Contratos y prompts genéricos |
| 🛠️ | `skills/` | Playbooks `sdaf-*`, `spec-draft-pbi`, `adr-propose`, `testing-review-pr`, `security-review`, `devops-ci-gate` |
| | `AGENTS.md.template` | Router a materializar en el consumidor |
| | `sdaf.config.schema.yaml` | Catálogo humano de claves |
| | `sdaf.config.schema.json` | Schema validable |
| | `sdaf.config.example.yaml` | Copia de la config recomendada (escenario 01) |
| | `examples/` | Escenarios YAML + explicación de cada clave |
| | `.cursor/rules/idioma-castellano.mdc` | Regla IDE de idioma |
| | `.cursor/rules/git-remoto-encargo.mdc` | Git/remoto solo si este turno lo nombra (H06 §7) |

## Cómo adoptar (consumidor)

Guía completa: [`docs/adopcion-y-upgrade.md`](docs/adopcion-y-upgrade.md). Resumen:

1. Referenciar este repo (submodule en `.sdaf/` pinneado a tag `v0.4.0` recomendado; subtree o copia también documentados).
2. Crear `sdaf.config.yaml` copiando un escenario de [`examples/`](examples/README.md). Claves: [`sdaf.config.schema.yaml`](sdaf.config.schema.yaml) / [`sdaf.config.schema.json`](sdaf.config.schema.json).
3. Ejecutar skill `sdaf-bootstrap` (o materializar `AGENTS.md` y el árbol a mano).
4. Añadir handbook de **producto** (plantilla `templates/handbook-product.md`).
5. ⛔ Gate 0 (`skills/sdaf-gate0`) antes de código de producto.

`sdaf.version` en el YAML nombra la línea de constitución: `0.4.0` con pin `v0.4.0`, `0.3.0` con pin `v0.3.3`. No existe el tag `v0.3.0`. Quien se quede en `v0.3.3` o `v0.2.1` no está obligado.

## Estado

| | Artefacto | Estado |
|--|-----------|--------|
| ✅ | Handbook del método | **Approved** 00–13 y A–B (línea 0.4.0) |
| ✅ | Agentes, prompts y skills | **Approved** (v0.4.0; contratos 0.2 siguen vigentes) |
| 📝 | Plantillas de consumidor | `templates/spec.md` y `handbook-product.md` permanecen Draft (se copian al consumidor) |
| | Release del árbol (tag) | **v0.4.0** |

## Origen

Extraído como núcleo reutilizable ([ADR-001](architecture/decisions/ADR-001-nucleo-reutilizable.md), Aceptado) desde un laboratorio de gobernanza. El primer producto que lo inspiró no forma parte de este repositorio.
