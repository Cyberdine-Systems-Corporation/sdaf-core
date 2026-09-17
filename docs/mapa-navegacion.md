# Mapa de navegación (sdaf-core)

> [!NOTE]
> 🧭 HOWTO de orientación. No sustituye el [handbook](../handbook/README.md).

## Vocabulario visual

Set cerrado. Si no encaja, no pongas icono. **Cero emoji en headings** de capítulos Approved.

| Icono | Rol |
|-------|-----|
| 📖 | Constitución / handbook |
| 🛠️ | HOWTO / playbook |
| ⛔ | STOP / Gate 0 |
| ✅ | Approved / DoD / proceed |
| 📝 | Draft / plantilla |
| 📦 | Pack de stack |
| 🧭 | Navegación / Relacionado |

En GitHub: alertas `NOTE` (HOWTO), `TIP` (pin recomendado), `WARNING` / `CAUTION` (STOP o prohibición). En Mermaid: rojo = STOP, verde = Approved/listo, gris = stub/derivado, azul = nivel constitucional.

## Ocho tareas y clics

Desde el [README](../README.md) del core:

| # | | Tarea | Destino | Clics |
|---|--|-----|---------|-------|
| 1 | 🛠️ | Adoptar SDAF en un repo nuevo | [adopcion-y-upgrade.md](adopcion-y-upgrade.md) | 1 |
| 2 | 📖 | Leer la constitución del método | [handbook/README.md](../handbook/README.md) | 1 |
| 3 | ⛔ | Cerrar Gate 0 antes de código | [skills/sdaf-gate0](../skills/sdaf-gate0/SKILL.md) | 1 |
| 4 | 🛠️ | Elegir escenario de `sdaf.config.yaml` | [examples/README.md](../examples/README.md) | 1 |
| 5 | 📦 | Publicar o consumir un pack de stack | [contrato-pack-stack.md](contrato-pack-stack.md) | 1 |
| 6 | 🛠️ | Subir de versión del core | [sdaf-upgrade](../skills/sdaf-upgrade/SKILL.md) (vía adopción) | 2 |
| 7 | 📝 | Registrar una iteración (ATF) | [H08](../handbook/08-agent-traceability.md) | 2 |
| 8 | 📖 | Enmendar un capítulo del handbook | [handbook-author](../prompts/documentation/handbook-author.md) | 2 |

Ninguna tarea de adopción o constitución exige más de **tres** clics desde el README.

## Roles de carpeta

| Carpeta | Rol | Libertad editorial |
|---------|-----|--------------------|
| `handbook/` | Constitución del método | Claridad y navegación; **sin** cambiar el significado normativo |
| `docs/` | HOWTO (adopción, pack, este mapa) | Alta |
| `README.md` | Puerta de entrada | Alta |
| `skills/`, `examples/` | Playbooks y escenarios | Alta |
| `templates/`, `prompts/`, `agents/` | Contratos operativos | Claridad; no contradecir H06–H08 |

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| 🧭 | [README.md](../README.md) | Tres puertas de entrada |
| 🛠️ | [docs/README.md](README.md) | Índice HOWTO |
| 🛠️ | [adopcion-y-upgrade.md](adopcion-y-upgrade.md) | Pin, bootstrap, upgrade |
| 📝 | [checklist-pagina-docs.md](checklist-pagina-docs.md) | DoD de una página markdown |
| 📝 | [Plantilla de PR](../.github/pull_request_template.md) | Checklist en el DoD del PR |
