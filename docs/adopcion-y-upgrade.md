# Adopción y upgrade de sdaf-core

> [!NOTE]
> 🛠️ HOWTO operativo. No sustituye el [handbook](../handbook/README.md).
>
> **Adoptar** es pinnear este core, copiar un escenario de config y ejecutar bootstrap. **Upgrade** es mover el pin y alinear `sdaf.version`.

**En esta página:** [Versionado](#versionado) · [Adopción](#adopción-canónica) · [Upgrade](#upgrade) · [Migración 0.1→0.2](#migración-de-citas-handbook-01x-020) · [Pack](#pack-de-stack)

## Versionado

| Concepto | Uso |
|----------|-----|
| Tag Git `vX.Y.Z` | Pin del **árbol** sdaf-core. Tags publicados: `v0.1.0`, `v0.2.0`, `v0.2.1`, `v0.3.2`, `v0.3.3`, `v0.4.0`, `v0.4.1`, `v0.4.2`, `v0.4.3`, `v0.5.0`, `v0.5.1`, `v0.5.2`. **No** existen `v0.3.0` ni `v0.3.1`. |
| `sdaf.version` en `sdaf.config.yaml` | Línea de **constitución** (semver **mayor.menor**). Con pin `v0.5.0`, `v0.5.1` o `v0.5.2`, `"0.5.0"`; con pin `v0.4.x`, `"0.4.0"`; con pin `v0.3.3`, `"0.3.0"`. No es un tag. |
| Capítulos / skills | Alineados a la misma línea (`0.2.x`, `0.3.x`, `0.4.x` o `0.5.x` según pin) |

> [!TIP]
> El pin recomendado del árbol es `v0.5.2`. `sdaf.version` nombra la línea (`"0.5.0"`, `"0.4.0"` o `"0.3.0"`), no un tag: `v0.3.0` no existe. Quien se quede en `v0.5.1`, `v0.5.0`, `v0.4.3`, `v0.3.3` o `v0.2.1` no está obligado.

Subir de `0.1.x` a `0.2.0` es un upgrade consciente (breaking de citas de handbook).

## Adopción (canónica)

```mermaid
flowchart TD
  P[Pin sdaf-core a un tag] --> C[Copiar escenario a sdaf.config.yaml]
  C --> B[Skill sdaf-bootstrap]
  B --> A[Materializar AGENTS.md]
  A --> G0[Gate 0 antes de código de producto]
  classDef stop fill:#f8d0d0,stroke:#8b1e1e,color:#1a1a1a;
  classDef ok fill:#d4edda,stroke:#2d6a4f,color:#1a1a1a;
  class G0 stop
  class P,C,B,A ok
```

1. Añadir sdaf-core como **submodule** pinneado a un tag, p. ej. en `.sdaf/`:

```text
git submodule add -b main <url-sdaf-core> .sdaf
cd .sdaf && git checkout v0.5.2
```

2. Copiar un escenario de [`examples/`](../examples/README.md) a `sdaf.config.yaml` en la raíz del consumidor (`sdaf.version` nombra la línea de constitución: `"0.5.0"` con pin `v0.5.0`, `v0.5.1` o `v0.5.2`, `"0.4.0"` con pin `v0.4.x`, `"0.3.0"` con pin `v0.3.3`).
3. Ejecutar la skill [`sdaf-bootstrap`](../skills/sdaf-bootstrap/SKILL.md) (o seguir sus pasos a mano).
4. Materializar `AGENTS.md` desde [`AGENTS.md.template`](../AGENTS.md.template).
5. Opcional: validar `sdaf.config.yaml` con la composite action [`.github/actions/validate-sdaf`](../.github/actions/validate-sdaf/README.md) (disponible desde `v0.4.0`).

### Alternativas

| Enfoque | Pros | Contras |
|---------|------|---------|
| Submodule (`.sdaf/`) | Pin claro, upgrade explícito | Curva git submodule |
| Subtree | Historia integrada | Merges de upgrade más ruidosos |
| Copia / template | Simple al inicio | Difícil propagar mejoras del core |

### Adoptar sobre un repo con código

Aplica cuando el repo ya tiene código previo a la adopción y no puede cumplir Gate 0 con él desde el primer día ([ADR-008](../architecture/decisions/ADR-008-adopcion-sobre-codigo-existente.md)). En un repo vacío, usar el flujo anterior.

Precondiciones:

- `sdaf-bootstrap` ejecutado: existen `sdaf.config.yaml` y el árbol.
- El repo adopta la línea `0.5.0` (opt-in): la línea base y G0.6 son de esa línea ([sección 0.5.0](#050-opt-in)).
- Hay un humano que aceptará los ADRs y aprobará la línea base. Los agentes los dejan en Propuesto o Draft.

Ejecutar [`sdaf-adopt-existing`](../skills/sdaf-adopt-existing/SKILL.md). Sus pasos (los cinco de ADR-008 §6 más el cierre en Gate 0):

1. Inventariar las unidades del código existente y proponer cuáles quedan en el perímetro heredado.
2. Rellenar la línea base descriptiva en Draft, con esas unidades marcadas «heredada».
3. Proponer un ADR de reconocimiento por decisión previa a la adopción.
4. Proponer el ADR de excepción de adopción ([H13 §3](../handbook/13-enmienda-excepciones-ciclo-de-vida.md#3-excepciones-temporales)), con caducidad propuesta y plan de retorno que lista las unidades heredadas.
5. Abrir el primer PBI gobernado en Draft y, si procede, specs de caracterización ([H04 §4](../handbook/04-specification-standard.md#4-cabecera-obligatoria)).
6. Ejecutar Gate 0: el STOP esperado es G0.1, G0.2, G0.4 y G0.6 (G0.3 solo si el PBI toca límites, [H14 §6](../handbook/14-architecture-description.md#6-cuándo-cambia)) hasta que un humano acepte los ADRs, apruebe la línea base y apruebe las specs con su acceptance.

Aceptar el ADR de excepción legitima solo los cambios correctivos con worklog en el perímetro heredado; no desbloquea Gate 0 en el perímetro gobernado. Una feature nueva o un cambio de comportamiento pasa la unidad al perímetro gobernado antes de implementar.

La caducidad la fija el humano. Caducada sin prórroga humana, la excepción deja de aplicar y el perímetro heredado pasa a Gate 0 completo: revisar entonces el plan de retorno.

Limitaciones de las comprobaciones actuales:

- [`scripts/check-adrs.py`](../scripts/check-adrs.py) valida los ADRs del core y aún no es apto para los de un consumidor con formato anterior: véase el aviso de la [sección 0.5.0](#050-opt-in).
- `check-worklog-presence.py` solo mira `stack.src_path` y `stack.tests_path`: el código heredado fuera de esas rutas no queda cubierto por esa comprobación hasta que haya unidades de código (v0.6.0).

## Upgrade

Usar [`sdaf-upgrade`](../skills/sdaf-upgrade/SKILL.md). Checklist:

1. Actualizar pin del submodule/tag al nuevo `vX.Y.Z`.
2. Leer [`handbook/CHANGELOG.md`](../handbook/CHANGELOG.md).
3. Actualizar `sdaf.version`.
4. Incorporar a `AGENTS.md` los cambios de la plantilla si cambió, conservando lo propio del consumidor (regenerarlo entero solo si no está personalizado).
5. Revisar citas `skill-id@version` en worklogs **nuevos**.
6. Si venías de 0.1.x: remapear citas de capítulos según la tabla siguiente.
7. No auto-migrar specs ni handbook de producto del consumidor.

## Migración de citas handbook (0.1.x → 0.2.0)

<details>
<summary>Tabla de remap 0.1.x → 0.2.0 (citas de capítulos)</summary>

| Antes | Después |
|-------|---------|
| `handbook/05-sdaf-framework.md` / H05 | `handbook/01-sdaf-framework.md` / H01 |
| `handbook/06-engineering-principles.md` / H06 | `handbook/02-engineering-principles.md` / H02 |
| `handbook/07-repository-organization.md` / H07 | `handbook/03-repository-organization.md` / H03 |
| `handbook/08-specification-standard.md` / H08 | `handbook/04-specification-standard.md` / H04 |
| `handbook/09-development-workflow.md` / H09 | `handbook/05-development-workflow.md` / H05 |
| `handbook/13-ai-agent-framework.md` / H13 | `handbook/06-ai-agent-framework.md` / H06 |
| `handbook/14-prompt-engineering-standard.md` / H14 | `handbook/07-prompt-engineering-standard.md` / H07 |
| `handbook/15-agent-traceability.md` / H15 | `handbook/08-agent-traceability.md` / H08 |
| `handbook/B-templates.md` | `handbook/A-templates.md` |

</details>

Partes: antigua “Parte II / IV” → **Parte I (método)** / **Parte II (IA)**.

## Pack de stack

Si `stack.pack` ≠ `null`, cumplir [`contrato-pack-stack.md`](contrato-pack-stack.md).

### Materialización en el consumidor

Preferir **symlinks relativos** (Git mode `120000`) de skills, agentes, prompts y reglas del core y del pack hacia la raíz del consumidor. En repos de referencia (p. ej. ShiftFlow-sdaf) hay un script documentado `scripts/materialize-submodules.ps1` + HOWTO `docs/materializacion-submodules.md`. Superficie Cursor opcional: `.cursor/skills/<id>` enlazada al submodule.

Copia literal solo como fallback documentado.

> [!WARNING]
> No usar junctions de Windows (`mklink /J`).

Parche **0.2.1** (hasta pin `v0.2.1`): contexto autorizado en contratos; recibo y línea de decisión en worklogs **nuevos**. Sin backfill. `sdaf.version` puede seguir `0.2.0`.

Parche **0.2.2** (docs): navegación, diagramas y vocabulario visual; no cambia la norma. No exige retag ni cambio de `sdaf.version`.

## 0.3.0 (opt-in)

Línea nueva de constitución. **No** rompe citas `H00`–`H08`. Quien se quede en `v0.2.1` no está obligado.

Al pinnear la línea 0.3 (tag `v0.3.3`; no hay tag `v0.3.0`):

1. Leer Parte III: [H09](../handbook/09-testing-framework.md)–[H12](../handbook/12-security-standards.md).
2. Adoptar QG-Sec y runbook local si no existían.
3. Materializar `SECURITY.md` desde [`templates/security.md`](../templates/security.md).
4. Opcional: ADR de coding standards para QG-Docs (pack o consumidor).
5. Actualizar `sdaf.version` a `0.3.0` y materializar skills nuevas (`testing-review-pr`, `security-review`, `devops-ci-gate`).

Métricas de sprint detalladas siguen en el handbook de **producto**, no en el core.

## 0.3.1 (parche)

Enmienda de [H06 §7](../handbook/06-ai-agent-framework.md#7-restricciones-globales): commit local y cualquier escritura al remoto (push, tags, releases, merge, PR, APIs, CI que escriba el repo) solo con petición humana explícita. La excepción en `AGENTS.md` o ADR debe enumerar qué permite.

No rompe citas. No exige cambiar `sdaf.version` si ya está en `0.3.0`.

## 0.3.2 (parche)

Ganchos de gobernanza **sin estatizar adopción**. Al pinnear un tag que incluya 0.3.2:

1. QG-Sec según [H12 §5.2](../handbook/12-security-standards.md#52-qg-sec) (no solo secreto y bypass de auth).
2. Merge a demo/integración: humano nominado ([H10](../handbook/10-code-review-and-quality-gates.md) QG-Review).
3. Worklogs **nuevos** de código de producto: origen de cambios ([H08 §4.3](../handbook/08-agent-traceability.md#43-origen-de-cambios)); sin backfill.
4. Overlays (SSDF, SBOM, AIMS, …): **N/A** hasta que el consumidor apruebe un ADR. No son bug por sí solos.

No rompe citas. `sdaf.version` puede seguir `0.3.0`.

## 0.3.3 (parche)

Enmienda de [H06 §7](../handbook/06-ai-agent-framework.md#7-restricciones-globales): **encargo vigente** = el mensaje de usuario de **este turno**. El historial de la conversación, un PR abierto o terminar archivos no autorizan commit ni escritura al remoto. Autoriza solo lo que este mensaje nombra.

Copia operativa para agentes Cursor: `.cursor/rules/git-remoto-encargo.mdc` (materializar junto a `idioma-castellano.mdc`).

No rompe citas. No exige cambiar `sdaf.version` si ya está en `0.3.0`.

## 0.4.0 (opt-in)

Línea nueva de constitución. **No** rompe citas `H00`–`H12`. Quien se quede en `v0.3.3` o `v0.2.1` no está obligado.

Al pinnear `v0.4.0`:

1. Leer [H13](../handbook/13-enmienda-excepciones-ciclo-de-vida.md): enmienda, excepciones con caducidad, derogación, breaking y mantenedor único.
2. QG-Review: «nominada» = la identidad de `CODEOWNERS` del consumidor ([H10](../handbook/10-code-review-and-quality-gates.md)).
3. Worklogs **nuevos** con el frontmatter de [`templates/worklog.md`](../templates/worklog.md) (`commit`, `pr`, `rama`, `sha` o `null`). Los worklogs en tabla siguen válidos; sin backfill.
4. Si algún script lee el historial del cuerpo de un capítulo, pasa a leer `handbook/_meta/<capítulo>.yaml`.
5. Opcional: composite action [`validate-sdaf`](../.github/actions/validate-sdaf/README.md) en el CI del consumidor.
6. Actualizar `sdaf.version` a `"0.4.0"`.

## 0.4.1 (parche)

[ADR-004](../architecture/decisions/ADR-004-tooling-externo-de-agentes.md): el tooling externo de agentes es **opcional**. Al pinnear `v0.4.1`:

1. Nada obligatorio: toda `sdaf.config.yaml` válida en `0.4.0` sigue validando.
2. Si el repo adopta gentle-ai, declararlo en `tooling.gentle_ai` (release o SHA de commit) y seguir [`integracion-gentle-ai.md`](integracion-gentle-ai.md).

No rompe citas. `sdaf.version` sigue en `"0.4.0"`.

## 0.4.2 (parche)

Cierra el seguimiento de ADR-004. Al pinnear `v0.4.2`:

1. Sin `tooling.gentle_ai` en la config: nada que hacer.
2. Con `tooling.gentle_ai`: regenerar `AGENTS.md` desde [`AGENTS.md.template`](../AGENTS.md.template) ([`sdaf-upgrade`](../skills/sdaf-upgrade/SKILL.md) paso 4) para incorporar la sección «Tooling externo», o copiarla a mano.

No rompe citas. `sdaf.version` sigue en `"0.4.0"`.

## 0.4.3 (parche)

Coherencia de versiones en la documentación publicada (H-10 de [INIT-arquitectura](iniciativas/INIT-arquitectura.md)). Al pinnear `v0.4.3` no hay nada que hacer: sin cambio de norma.

No rompe citas. `sdaf.version` sigue en `"0.4.0"`.

## 0.5.0 (opt-in)

Línea nueva de constitución. **No** rompe citas `H00`–`H13`, pero **sí** cambia el significado de Gate 0 ([H13 §5](../handbook/13-enmienda-excepciones-ciclo-de-vida.md)): por eso es opt-in. Quien se quede en `0.4.x` no está obligado.

Al pinnear `v0.5.0`:

1. Leer [H14](../handbook/14-architecture-description.md) y [`templates/architecture-description.md`](../templates/architecture-description.md).
2. Construir `architecture/description.md` desde los ADRs vigentes ([H14 §9](../handbook/14-architecture-description.md#9-migración-desde-un-consumidor-existente)): listar las unidades y reglas que esos ADRs ya establecen, enlazarlos y escribir `N/A: <motivo>` en lo demás. No se reescriben ADRs.
3. Pedir la aprobación humana de la línea base (Draft → Approved). Sin ella, G0.6 hace STOP.
4. Gate 0 ([H05](../handbook/05-development-workflow.md)): G0.6 exige la línea base Approved; G0.3 exige un ADR Aceptado si el cambio toca límites ([H14 §6](../handbook/14-architecture-description.md#6-cuándo-cambia)); G0.4 exige un PBI de [`templates/pbi.md`](../templates/pbi.md) (specs Approved, acceptance y unidades).
5. QG-Arch ([H10](../handbook/10-code-review-and-quality-gates.md)) verifica las reglas de dependencia de la línea base; solo es `N/A` con el motivo en el worklog.
6. Estados de ADR según [ADR-006](../architecture/decisions/ADR-006-ciclo-de-vida-de-adrs.md): los ADRs antiguos con tres estados siguen válidos; las excepciones llevan `Tipo = Excepción` y `Caducidad`; la sustitución es recíproca (Sustituye / Sustituido por).
7. Crear `specs/integration/` y usar los campos Unidades y Origen en las specs ([H04](../handbook/04-specification-standard.md)).
8. Aplicar la precedencia única de [H01 §3.2](../handbook/01-sdaf-framework.md): spec y ADR al mismo nivel; un conflicto entre ambos es STOP y enmienda.
9. Incorporar a `AGENTS.md` los cambios de [`AGENTS.md.template`](../AGENTS.md.template) `0.5.0` (norma H14 y precedencia única en la sección de gobierno), conservando lo propio; regenerarlo entero solo si no está personalizado.
10. El idioma `es` lo registra [ADR-009](../architecture/decisions/ADR-009-idioma-de-artefactos.md).
11. Actualizar `sdaf.version` a `"0.5.0"`.

[`sdaf-bootstrap`](../skills/sdaf-bootstrap/SKILL.md) con `0.5.0` crea la línea base en Draft y su STOP cita G0.1 y G0.6.

Los ADRs del consumidor no se reescriben. [`scripts/check-adrs.py`](../scripts/check-adrs.py) valida los ADRs **del core** (fechas con hora y zona, numeración sin huecos, índice con el estado en la segunda columna): aún no es apto para los ADRs de un consumidor con formato anterior. Su modo consumidor está previsto en el backlog de la iniciativa (ARQ-6.3).

No rompe citas. `sdaf.version` pasa a `"0.5.0"` solo si el consumidor adopta la línea.

## 0.5.1 (parche)

Procedimiento **opcional** para adoptar SDAF sobre un repo con código previo ([ADR-008](../architecture/decisions/ADR-008-adopcion-sobre-codigo-existente.md)): skill [`sdaf-adopt-existing`](../skills/sdaf-adopt-existing/SKILL.md) (Draft, pendiente de aprobación humana), excepción de adopción ([H13 §3](../handbook/13-enmienda-excepciones-ciclo-de-vida.md#3-excepciones-temporales)) y specs de caracterización ([H04 §4](../handbook/04-specification-standard.md#4-cabecera-obligatoria)). No añade gates ni cambia los existentes.

Al pinnear `v0.5.1`:

1. Quien no adopte sobre código existente: nada que hacer.
2. Quien lo haga, en la línea `0.5.0`: seguir [Adoptar sobre un repo con código](#adoptar-sobre-un-repo-con-código).

Diferido a un parche posterior: el catálogo de H06 §6, `sdaf-gate0` y `sdaf-bootstrap` aún no conocen la skill ni los perímetros.

No rompe citas. `sdaf.version` sigue en `"0.5.0"`.

## 0.5.2 (parche)

Completa lo diferido en 0.5.1: el catálogo de [H06 §6](../handbook/06-ai-agent-framework.md) lista [`sdaf-adopt-existing`](../skills/sdaf-adopt-existing/SKILL.md) (`0.1.1`, Approved por aprobación humana), [H08 §5](../handbook/08-agent-traceability.md#5-cuándo-crear-worklog) exige worklog en los cambios correctivos del perímetro heredado, [`sdaf-gate0`](../skills/sdaf-gate0/SKILL.md) no hace STOP en ellos con el ADR de excepción de adopción Aceptado y vigente, y [`sdaf-bootstrap`](../skills/sdaf-bootstrap/SKILL.md) deriva a la skill si el repo ya tiene código previo. No añade gates ni cambia los del perímetro gobernado.

Al pinnear `v0.5.2`:

1. Quien no adopte sobre código existente: nada que hacer.
2. Quien lo haga, en la línea `0.5.0`: seguir [Adoptar sobre un repo con código](#adoptar-sobre-un-repo-con-código); un cambio correctivo en el perímetro heredado ya no se detiene en Gate 0 si el ADR sigue vigente, y una feature pasa antes al perímetro gobernado.

No rompe citas. `sdaf.version` sigue en `"0.5.0"`.

## Fuera de 0.5.x

Sin implementar en esta línea:

- Métricas de sprint / capacidad humana detallada (producto)
- Glosario de dominio (pertenece al producto)
- Script de materialización en el core (previsto en la línea 0.6.0)

`project.language` distinto de `es` ya no está pendiente: lo registra [ADR-009](../architecture/decisions/ADR-009-idioma-de-artefactos.md) y otro idioma exige un ADR sustituto.

No se reintroducen huecos numéricos “por si acaso” en el handbook del core.

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| 🧭 | [mapa-navegacion.md](mapa-navegacion.md) | Ocho tareas y clics |
| 🛠️ | [skills/sdaf-bootstrap](../skills/sdaf-bootstrap/SKILL.md) | Pasos de árbol y config |
| 🛠️ | [skills/sdaf-upgrade](../skills/sdaf-upgrade/SKILL.md) | Mover el pin |
| 📖 | [handbook/CHANGELOG.md](../handbook/CHANGELOG.md) | Qué cambió en cada tag |
