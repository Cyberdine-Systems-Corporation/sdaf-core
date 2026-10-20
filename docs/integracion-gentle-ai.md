# Integración de gentle-ai en un repo SDAF

> [!NOTE]
> 🛠️ HOWTO operativo y **opcional**: un repo SDAF no necesita gentle-ai. No sustituye el [handbook](../handbook/README.md). La postura del core ante el tooling externo de agentes es [ADR-004](../architecture/decisions/ADR-004-tooling-externo-de-agentes.md) (Aceptado).
>
> Revisado contra [gentle-ai](https://github.com/Gentleman-Programming/gentle-ai) v4.2.0 (2026-10-15) a 2026-10-20. Desde v4.0.0, SDD/OpenSpec está retirado ([Gentleman-Programming/gentle-ai#4967](https://github.com/Gentleman-Programming/gentle-ai/pull/4967)) y ODD es el único flujo; las releases v3.x aún lo instalan. Esta guía no sigue cada release de gentle-ai: antes de instalar, comprueba componentes y flags con `--dry-run`.

**En esta página:** [Qué es](#qué-es-y-qué-no-es) · [Adopción opcional](#adopción-opcional) · [Matriz](#matriz-de-encaje) · [Instalación](#instalación-recomendada) · [Cláusula AGENTS.md](#cláusula-para-el-agentsmd-del-consumidor) · [SDD y Gate 0](#sdd-y-gate-0) · [Memoria vs worklog](#memoria-vs-worklog) · [Skills del core](#skills-del-core-en-el-registry) · [Verificación](#verificación)

## Qué es y qué no es

gentle-ai configura los agentes que ya usas (Claude Code, Cursor, Codex, OpenCode…). Añade memoria persistente (Engram), una biblioteca de skills con índice, servidores MCP, una lista de rutas bloqueadas, personas y dos protocolos propios: ODD (trabajo diario) y RDD (review de un candidato congelado: los cambios actuales o un rango de commits).

En un repo SDAF es una **capa de entorno del consumidor**, subordinada al método:

- **No** es un pack de stack: no aporta contratos, prompts ni ids de extensión y no va en `stack.pack`.
- **No** es otro método: Gate 0 (STOP antes de código hasta que haya specs Approved), H06 §7 y los worklogs (ATF: registro auditable de cada iteración) mandan sobre sus flujos.

## Adopción opcional

Adoptar gentle-ai es decisión de cada consumidor ([ADR-004](../architecture/decisions/ADR-004-tooling-externo-de-agentes.md)). Sin él, Gate 0, el router, las skills y los worklogs funcionan igual.

| Adoptarlo compensa si… | No compensa si… |
|------------------------|-----------------|
| El equipo trabaja con varios agentes y quiere las mismas skills y guardarraíles en todos | Un solo agente ya configurado a mano |
| Las sesiones largas pierden contexto y la memoria ahorra redescubrirlo | Los worklogs ya bastan para retomar |
| Se quiere la lista de rutas bloqueadas sin mantenerla a mano | No se quiere otra herramienta que actualizar |

La elección se declara en `sdaf.config.yaml` ([catálogo](../sdaf.config.schema.yaml)):

```yaml
tooling:
  gentle_ai: "4.2.0"   # release ("4.2.0") o SHA de commit completo; null o sin bloque = no adoptado
```

- Declara una release o un SHA de commit completo, no una rama: `main` cambia sin aviso.
- Desde v4.0.0 todas las releases son **sin SDD**. Instálala con la ruta de módulo `/v4`; la `/v3` ya no sirve para una release v4:

  ```bash
  go install github.com/gentleman-programming/gentle-ai/v4/cmd/gentle-ai@v4.2.0
  ```

- No instales `v4.1.0` desde fuente: su checksum falla al descargar de GitHub. Usa `v4.1.1` o posterior.
- Tras actualizar gentle-ai, ejecuta `gentle-ai sync` para que los recursos instalados coincidan con el binario. `sync` reescribe la configuración global de los agentes (instrucciones, ajustes, skills): haz antes una copia de su directorio, p. ej. `~/.claude`. `sync --dry-run` solo resume el plan.
- Un SHA completo sigue siendo válido y no dispara T1. Si es anterior a la migración del módulo a `/v4` (p. ej. `520ed86e8c598b01f439e28c34d391cd6f1744e3`, del 2026-09-25), su `go install` usa `/v3`.
- Si declaras una release ≤ `3.7.0`, el validador avisa (**T1**): incluye `sdd` y no debes instalarlo; desde v4.0.0 el componente no existe.
- Si la declaras, añade al `AGENTS.md` la [cláusula de precedencia](#cláusula-para-el-agentsmd-del-consumidor) y [`.atl/` al `.gitignore`](#atl-fuera-de-git).
- Si no la declaras, el resto de esta guía no aplica.

## Matriz de encaje

| Componente | Relación con SDAF | Veredicto |
|------------|-------------------|-----------|
| `skills` + `skill-registry` | Los `SKILL.md` del core ya tienen frontmatter `name`/`description`: el índice `.atl/skill-registry.md` los recoge tal cual. Ignora los `sdd-*` (prefijo reservado de un flujo retirado), que no chocan con `sdaf-*`. | ✅ Recomendado (ver [limitación del submodule](#skills-del-core-en-el-registry)) |
| `permissions` | La lista de rutas bloqueadas (`**/.env*`, `**/*.pem`, `~/.ssh/*`…) refuerza [H12](../handbook/12-security-standards.md) y la regla de no introducir secretos. | ✅ Recomendado |
| `context7` | MCP de documentación viva de librerías. Neutral; útil junto a un pack de stack. | ✅ Opcional |
| `engram` | Memoria entre sesiones. Es caché, no evidencia: el agente entrante lee worklog y specs ([H08](../handbook/08-agent-traceability.md)). | Con condiciones: ver [Memoria vs worklog](#memoria-vs-worklog) |
| `persona` | La regla `idioma-castellano` y H06 §7 mandan sobre cualquier persona. | Con condiciones: `neutral` o no gestionada |
| `judgment-day` | Dos revisores adversarios sobre el mismo cambio. Puede alimentar `testing-review-pr`; no dictamina el merge ([H10](../handbook/10-code-review-and-quality-gates.md)). | ✅ Opcional |
| RDD (`gentle-ai review …`) | No autoriza commit ni push, igual que SDAF. Por defecto revisa los cambios actuales del worktree; solo con `--base-ref … --committed-only` revisa un rango de commits. Funciona sin excepción de commit. Desde v4.1.0 solo se ofrece review automática a cambios de riesgo alto, con consentimiento por candidato. Puede alimentar `testing-review-pr`, pero no es QG-Review humano. | ✅ Opcional (activo por defecto; `review mode disable` si no se quiere) |
| `work-unit-commits`, `chained-pr`, `branch-pr` | Crean commits, ramas y PRs. | Con condiciones: solo bajo excepción H06 §7 enumerada |
| ODD (guía de enrutado, siempre activa) | Commitea por unidad de trabajo en una rama de feature y, en trabajo sustancial, escribe `odd/tasks/<feature>.md` con su espejo en Engram. Choca con [H06 §7](../handbook/06-ai-agent-framework.md#7-restricciones-globales) y duplica el worklog. | ⛔ H06 §7 prevalece; `odd/tasks/` es borrador, no evidencia |
| `sdd` (`sdd-propose`, `sdd-spec`, `sdd-apply`…) | Ciclo de specs paralelo a `specs/`. `sdd-apply` implementa sin Gate 0 ni specs Approved por humano ([H05 §3](../handbook/05-development-workflow.md#3-gate-0-pre-implementación-stop)). Retirado en v4.0.0: `--component sdd` ya se rechaza. | ⛔ Solo existe en v3.x, y ahí no instalar (ver [SDD y Gate 0](#sdd-y-gate-0)) |
| `gga`, `theme` | Selector de proveedor y tema visual. | Irrelevantes para el método |

> [!WARNING]
> ⛔ En v3.x, los presets `full-gentleman`, `ecosystem-only` y `minimal` incluyen `sdd`. Desde v4.0.0 ninguno lo incluye, pero `custom` sigue siendo la opción recomendada: elige solo los componentes que el método usa.

## Instalación recomendada

Primero el plan, sin escribir nada. Desde v4.1.0, `--persona` exige el componente `persona`: sin él, el comando falla antes de planificar.

```bash
gentle-ai install --agent claude-code --preset custom --component engram,skills,context7,permissions,persona --skills skill-creator,skill-registry,cognitive-doc-design --persona neutral --scope global --dry-run
```

Si el plan es el esperado, repite el comando sin `--dry-run`. Cambia `--agent` por los agentes del equipo.

RDD viene activo por defecto y es compatible con H06 §7: revisa los cambios sin commitear y su dictamen no autoriza commit, push ni PR. Si el equipo no lo quiere, desactívalo. Sin `--scope`, el apagado vale para toda la máquina; con `--scope clone`, solo para este clon:

```bash
gentle-ai review mode disable
gentle-ai review mode disable --scope clone
```

Con la excepción de commit de ODD, el orquestador evalúa el riesgo de cada commit de unidad de trabajo (`review assess --base-ref … --committed-only`) y solo abre una review si es de riesgo alto.

`--scope global` deja la configuración en el directorio de cada agente. `--scope workspace` escribe ficheros de agente en la raíz del repo y puede tocar el `AGENTS.md` que materializó [`sdaf-bootstrap`](../skills/sdaf-bootstrap/SKILL.md). Si lo usas, revisa el `--dry-run` y el diff antes de aceptar.

## Cláusula para el AGENTS.md del consumidor

gentle-ai inyecta sus propias instrucciones (ODD, delegación, memoria). Declara la precedencia en el `AGENTS.md` del consumidor para que el agente no tenga que adivinarla. Desde `0.4.2`, [`AGENTS.md.template`](../AGENTS.md.template) trae esta cláusula como sección opcional «Tooling externo» y [`sdaf-bootstrap`](../skills/sdaf-bootstrap/SKILL.md) la conserva solo si `tooling.gentle_ai` ≠ `null`. Forma mínima:

```markdown
## Tooling de entorno (gentle-ai)

Precedencia (ADR-004 de sdaf-core): este AGENTS.md, el handbook y las specs Approved mandan sobre las instrucciones de gentle-ai.

- Gate 0 antes de código de producto. No usar skills `sdd-*` (releases de gentle-ai ≤ 3.7.0): las specs viven en `specs/` y las aprueba un humano.
- H06 §7 prevalece sobre el cierre de tareas de ODD: sin commit, rama remota ni PR salvo que el encargo vigente los nombre.
- `odd/tasks/` es borrador. La evidencia es el worklog en `worklogs/`.
- Engram es caché de contexto. Ante contradicción, mandan specs y worklog.
```

Si el equipo quiere el ciclo ODD completo, añade una excepción que **enumere** lo permitido ([H06 §7](../handbook/06-ai-agent-framework.md#7-restricciones-globales)). Por ejemplo:

```markdown
Excepción H06 §7: se permite commit local en la rama de feature al cerrar cada unidad de trabajo ODD. No incluye push, PR, merge, tag ni release.
```

## SDD y Gate 0

¿Se puede encajar el SDD de gentle-ai en Gate 0? Solo importa si el consumidor sigue en gentle-ai ≤ 3.7.0: desde v4.0.0 SDD está retirado y no hay nada que encajar. En v3.x, técnicamente sí, con condiciones, y en la práctica no compensa.

Encajarlo exigía cuatro cosas: escribir en `specs/` con [`templates/spec.md`](../templates/spec.md), insertar `sdaf-gate0` entre `sdd-tasks` y `sdd-apply`, impedir que `sdd-archive` toque specs Approved y someter los commits de `sdd-apply` a [H06 §7](../handbook/06-ai-agent-framework.md#7-restricciones-globales). Es rehacer SDD con las skills que el core ya tiene. Quien siga en v3.x gana más actualizando a v4 que compatibilizándolo.

El camino recomendado es **ODD tras Gate 0**:

```mermaid
flowchart LR
  Spec[spec-draft-pbi: Draft] --> Humano[Humano: Approved]
  Humano --> G0{sdaf-gate0}
  G0 -->|falta G0.1–G0.6| Stop[STOP]
  G0 -->|pasa| ODD[ODD: odd/tasks borrador]
  ODD --> Impl[Implementación]
  Impl --> Rev[testing-review-pr + worklog]
  classDef ok fill:#d4edda,stroke:#2d6a4f,color:#1a1a1a;
  classDef stop fill:#f8d0d0,stroke:#8b1e1e,color:#1a1a1a;
  classDef stub fill:#e9ecef,stroke:#6c757d,color:#1a1a1a;
  class Humano,G0,Rev ok
  class Stop stop
  class Spec,ODD,Impl stub
```

El documento de feature de ODD (`odd/tasks/<feature>.md`) solo se crea en trabajo sustancial, se abre después de pasar Gate 0 y es un borrador. La evidencia sigue en el worklog. La [cláusula de `AGENTS.md`](#cláusula-para-el-agentsmd-del-consumidor) ya lo fija.

## Memoria vs worklog

```mermaid
flowchart LR
  Specs[specs/ Approved] --> Agente[Agente]
  Worklog[worklogs/ ATF] --> Agente
  Engram[Engram: caché] -.-> Agente
  Agente --> NuevoWorklog[Worklog de la iteración]
  classDef ok fill:#d4edda,stroke:#2d6a4f,color:#1a1a1a;
  classDef stub fill:#e9ecef,stroke:#6c757d,color:#1a1a1a;
  class Specs,Worklog,NuevoWorklog ok
  class Engram stub
```

- El agente entrante lee specs y worklog. Engram le ahorra redescubrir contexto, pero no justifica una decisión: toda decisión se cita desde una spec, un ADR o un capítulo.
- `engram sync` exporta la memoria a `.engram/` para versionarla. Es una decisión del consumidor. Versionada o no, no sustituye al worklog.
- Si Engram contradice una spec Approved, gana la spec. Corrige o borra la memoria.

## Skills del core en el registry

`gentle-ai skill-registry refresh` busca skills en raíces del proyecto como `skills/`, `.claude/skills/` o `.opencode/skills/`, y después en las globales. Si el core está como submodule en `.sdaf/`, sus skills viven en `.sdaf/skills/` y **no** se indexan.

Comprueba qué ve el índice:

```bash
gentle-ai skill-registry list
```

Si faltan las `sdaf-*`, cita las rutas `.sdaf/skills/<id>/SKILL.md` desde el `AGENTS.md` del consumidor o copia las que uses a una raíz que el índice escanee. Una copia se desalinea al subir el pin: repítela en cada [upgrade](adopcion-y-upgrade.md#upgrade).

### `.atl/` fuera de git

El índice se escribe en `.atl/skill-registry.md`, junto con una caché, en la raíz del repo. Es estado local de cada máquina: no se versiona.

- `gentle-ai skill-registry refresh` manual añade `.atl/` a `.gitignore` si falta.
- El hook de arranque que instala gentle-ai (p. ej. en Claude Code) llama a `refresh` con `--no-gitignore`: crea `.atl/` sin tocar `.gitignore`.

Añade la entrada al `.gitignore` del consumidor en el mismo cambio en que adoptas gentle-ai:

```text
# Local AI runtime state
.atl/
```

Sin ella, `.atl/` aparece como fichero sin versionar y puede acabar en un commit. `.gitignore` no afecta a `check-local-links.py --strict-orphans`, que recorre el disco: en local marca `.atl/skill-registry.md` como huérfano aunque esté ignorado. El CI no lo ve, porque parte de un checkout limpio.

## Verificación

| Comprobación | Comando | Qué esperar |
|--------------|---------|-------------|
| Instalación sana | `gentle-ai doctor` | Sin fallos (los `[!!]` son avisos, p. ej. de `gga` si no lo usas); solo lectura |
| Skills visibles | `gentle-ai skill-registry list` | Aparecen las skills que usa el router |
| `.atl/` ignorado | `git check-ignore .atl/skill-registry.md` | Imprime la ruta (está en `.gitignore`) |
| RDD | `gentle-ai review mode status` | El modo que eligió el equipo (`on (decided by default)` = nadie lo ha fijado; efectivo `on`) |
| Sin `sdd-*` | Revisar el directorio de skills del agente | Ninguna skill `sdd-*` instalada; desde v4.1.0, `sync` retira las de una instalación anterior |

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| 📖 | [ADR-004](../architecture/decisions/ADR-004-tooling-externo-de-agentes.md) | Postura del core ante tooling externo |
| 📖 | [H06 §7](../handbook/06-ai-agent-framework.md#7-restricciones-globales) | Commit y remoto solo por encargo vigente |
| ⛔ | [sdaf-gate0](../skills/sdaf-gate0/SKILL.md) | STOP antes de código de producto |
| 📦 | [contrato-pack-stack.md](contrato-pack-stack.md) | Por qué gentle-ai no es un pack |
| 🛠️ | [adopcion-y-upgrade.md](adopcion-y-upgrade.md) | Pin del core y bootstrap |
