# CHANGELOG — handbook sdaf-core

## 0.4.2 — 2026-09-26T17:27+02:00

Parche (**no** breaking de citas `H00`–`H13` ni de configs). Sin cambio de capítulos. Cierra el seguimiento de [ADR-004](../architecture/decisions/ADR-004-tooling-externo-de-agentes.md).

- `AGENTS.md.template` `0.4.2`: sección opcional «Tooling externo» con la cláusula de precedencia (Gate 0, H06 §7 y worklogs sobre `sdd-*`, ODD y la memoria del tooling). Se borra al materializar si `tooling.gentle_ai` no se declara.
- `sdaf-bootstrap` `0.4.2`: `tooling` opcional en la config y la sección anterior solo si se declara.
- Worklog: [`worklogs/ADR-004-tooling-externo/Iteration-006.md`](../worklogs/ADR-004-tooling-externo/Iteration-006.md).

Quien no adopte tooling externo no tiene que hacer nada. Quien lo adopte regenera `AGENTS.md` ([`sdaf-upgrade`](../skills/sdaf-upgrade/SKILL.md) paso 4). `sdaf.version` sigue en `"0.4.0"`. Pin de árbol: `v0.4.2`. Quien siga en `v0.4.1` o `v0.4.0` no está obligado a moverlo.

## 0.4.1 — 2026-09-26T11:41+02:00

Parche (**no** breaking de citas `H00`–`H13` ni de configs: toda `sdaf.config.yaml` válida en `0.4.0` sigue siéndolo). Sin cambio de capítulos. ADR-004 aceptado por humano: Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS).

- [ADR-004](../architecture/decisions/ADR-004-tooling-externo-de-agentes.md) Aceptado: el tooling externo de agentes (gentle-ai como caso de referencia) es una capa de entorno del consumidor, opcional y subordinada al método. Specs y worklogs siguen siendo la única evidencia; Gate 0 y H06 §7 prevalecen sobre sus flujos.
- Config: bloque opcional `tooling` con `tooling.gentle_ai` (`null`, release semver o SHA de commit de 40 hex; una rama no vale). Ausente o `null` = no adoptado.
- Validador: aviso **T1** (nunca error) si `tooling.gentle_ai` es una release ≤ `3.7.0`, que incluye el componente `sdd`.
- HOWTO nuevo: [`docs/integracion-gentle-ai.md`](../docs/integracion-gentle-ai.md) (matriz de encaje, SDD frente a Gate 0, cláusula de precedencia para `AGENTS.md`).
- Worklogs del cambio: [`worklogs/ADR-004-tooling-externo/`](../worklogs/ADR-004-tooling-externo/Iteration-005.md) (iteraciones 001–005).

`sdaf.version` sigue en `"0.4.0"`: nombra la línea, no el parche. Pin de árbol: `v0.4.1`. Quien siga en `v0.4.0` no está obligado a moverlo.

## 0.4.0 — 2026-09-24T18:54+02:00

Línea nueva de constitución (**no** breaking de citas `H00`–`H12`). Aceptada por humano: Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS). Quien se quede en `v0.3.3` o `v0.2.1` no está obligado.

- H13 Approved (`0.4.0`): enmienda, excepciones con caducidad, derogación, qué es breaking, regla de bump, mantenedor único y fechas con hora y zona desde esta línea (§9). Parte IV del índice.
- ADR-001 (núcleo reutilizable), ADR-002 (gobernanza) y ADR-003 (formato) Aceptados, en [`architecture/decisions/`](../architecture/decisions/README.md). Los ADRs del core se numeran desde 001: «ADR-008» en las entradas anteriores equivale a ADR-001.
- H00 `0.4.0`: remite a H13. H10 `0.4.0`: «nominada» = CODEOWNERS; el mantenedor nombrado puede aprobar su propio PR. H08 `0.4.0`: worklog con frontmatter, `inicio`/`fin` con hora y zona, `tiempo` y `coste` estructurados (`N/D` solo con motivo) y `commit`/`pr`/`rama`/`sha`; la tabla vigente sigue válida, sin backfill. H07 `0.3.0`: el andamiaje de capítulos vive en `handbook/_meta/`. H03 `0.2.3`: el core publica sus ADRs.
- Formato: cabecera, TOC, Relacionado e Historial de los capítulos salen del cuerpo a `handbook/_meta/` e `handbook/index.yaml`. Quien parsee el historial en el cuerpo debe leer el sidecar.
- Tooling: validador de config (I1–I3 error, I4 aviso / `--strict-i4`), action `validate-sdaf`, metadatos de versión, historial que solo crece, fechas con hora (H13 §9), ADRs del core (`check-adrs.py`: numeración, estado, fechas e índice), schema de worklog, presencia de worklog.
- Worklog del cambio: [`worklogs/INIT-auditoria-v0.3.3/Iteration-001.md`](../worklogs/INIT-auditoria-v0.3.3/Iteration-001.md). El core guarda en `worklogs/` los worklogs de sus cambios materiales ([H08 §5](08-agent-traceability.md)).

`sdaf.version: "0.4.0"` nombra esta línea. Pin de árbol: `v0.4.0`. Quien siga en `v0.3.3` mantiene `sdaf.version: "0.3.0"`.

## 0.3.3 — 2026-09-19

Parche (**no** breaking de citas `H00`–`H08`). H06 §7: **encargo vigente** = el mensaje de usuario de **este turno**. El historial de la conversación, un PR abierto o terminar archivos no autorizan commit ni escritura al remoto. Autoriza solo lo que este mensaje nombra.

Copia operativa: regla IDE `git-remoto-encargo`, `AGENTS.md.template`, `prompts/system/master-architect.md`.

`sdaf.version` nombra la **línea de constitución** (`0.3.0`), no un tag. Pin de árbol: `v0.3.3`.

## 0.3.2 — 2026-09-19

Parche (**no** breaking de citas `H00`–`H08`). Ganchos de gobernanza **sin estatizar adopción**:

- H12 §3: catálogo de referencias con uso **baseline** / **overlay** (N/A salvo ADR) / **fuera del método** (GRC o handbook de producto). SSDF/800-218A, SBOM/AIBOM y 42001/AI Act/CRA no entran en el baseline.
- H12 §5.2 / H10: QG-Sec alineado al mapa §4.3 (secreto, bypass de auth, injection, SSRF, CVE crítica identificada en el review). Scanner con umbral = overlay.
- H10: QG-Review exige aprobación humana nominada del merge; el dictamen del agente no basta.
- H08 §4.3: origen de cambios (`humano` / `ia` / `mixto` / `dependencia`) en worklogs **nuevos** de código de producto; sin backfill.
- Catálogo: `security-review` prioridad alta.

`sdaf.version` nombra la **línea de constitución** (`0.3.0`), no un tag. Pin de árbol: `v0.3.2` (incluido en `v0.3.3`).

## 0.3.1 — 2026-09-19

Parche (**no** breaking de citas `H00`–`H08`). Enmienda de H06: los agentes no crean commit local ni alteran el remoto del proyecto sin petición humana explícita. El criterio es el **efecto** (el remoto cambia), no el comando: push, tags, releases, merge, PR, APIs de contenidos, CI que escriba el repo. Terminar archivos o un DoD no autoriza git.

El consumidor puede exceptuarlo por cláusula en su `AGENTS.md` o por ADR; la cláusula debe **enumerar** qué permite. Lo no enumerado sigue prohibido. Force-push, reescribir historia y auto-merge siguen exigiendo orden humana.

`sdaf.version` nombra la **línea de constitución** (`0.3.0`), no un tag. Esta entrada **no** tiene tag `v0.3.1`. Pin de árbol: `v0.3.2` o `v0.3.3`.

## 0.3.0 — 2026-09-19

Línea nueva de constitución (**no** breaking de citas `H00`–`H08`). Caps. 09–12, apéndice B, skills y prompts Parte III: **Approved** (aprobación humana del director técnico).

- Parte III — Calidad y entrega: H09 Testing, H10 Review/QG, H11 DevOps, H12 Security (trasplante genérico extract H16/H17/H18/H20; stack y producto fuera).
- Apéndice B: glosario de método (sin ubiquitous language de dominio).
- Skills `testing-review-pr`, `security-review`, `devops-ci-gate`.
- Prompts `prompts/review/`, `prompts/quality/`, `prompts/planning/`.
- Plantilla `templates/security.md` (el consumidor materializa `SECURITY.md`).

El consumidor puede seguir pinneado a `v0.2.1` / `sdaf.version` `0.2.0` hasta que adopte esta línea. Esta entrada **no** tiene tag `v0.3.0`. Pin de árbol de la línea 0.3: `v0.3.2` o `v0.3.3`. `sdaf.version: "0.3.0"` nombra la línea de constitución, no un tag.

## 0.2.2 — 2026-09-17

Parche de navegación y formato (no breaking, **sin** cambio de significado normativo).

- TOC «En esta página» y bloque Relacionado en capítulos 00–08 y A.
- Diagramas Mermaid (con color semántico) en el índice, H01, H04, H05, H06, H08 y HOWTO de adopción.
- Alertas GFM (NOTE/TIP/WARNING/CAUTION/IMPORTANT) y vocabulario visual cerrado en README, `docs/` y skills.
- Checker de enlaces sobre todo el árbol markdown; checklist de página y mapa de clics en `docs/`.

`sdaf.version` del consumidor puede seguir en `0.2.0`. El pin de árbol recomendado sigue siendo el tag `v0.2.1` hasta el próximo tag.

## 0.2.1 — 2026-09-13

Parche (no breaking). Campos opcionales un ciclo.

- H06 §4: contexto autorizado en el contrato (índice; el agente abre artefactos, no mega-prompt).
- H07 §7: resumen = índice (`id@version` + 1 línea); prohibido como sustituto del prompt o como mega-resumen multi-agente.
- H08 §4: recibo de iteración y línea de decisión opcionales; sin backfill de worklogs.
- Plantillas `templates/worklog.md` y `templates/agent-contract.md`.

`sdaf.version` del consumidor puede seguir en `0.2.0` hasta pin al tag `v0.2.1`.

## 0.2.0 — 2026-08-25

### Breaking: renumeración correlativa

| Antes (0.1.x) | Después (0.2.0) |
|---------------|-----------------|
| 00 preface | 00 preface |
| 05 framework | 01 framework |
| 06 principles | 02 principles |
| 07 repository | 03 repository |
| 08 specification | 04 specification |
| 09 workflow | 05 workflow |
| 13 agents | 06 agents |
| 14 prompts | 07 prompts |
| 15 traceability | 08 traceability |
| B templates | A templates |

Partes: **I — Método** (01–05), **II — Ingeniería IA** (06–08), **Apéndice A**.

### Enmiendas de anclaje

- H01 §6: pack no contradice handbook; contrato en `docs/contrato-pack-stack.md`.
- H03: pin a tag sdaf-core; procedimiento en `docs/adopcion-y-upgrade.md`.
- H05 §2: paso 0 bootstrap (`sdaf-bootstrap`).
- H06 §6: catálogo con `sdaf-bootstrap` y `sdaf-upgrade`.
- Apéndice A: plantilla `handbook-product.md`.

## 0.1.1 — 2026-08-24

- Constitución del método **Approved** (aprobación explícita del director técnico): caps. 00, 05–09, 13–15, B.

## 0.1.0 — 2026-08-24

- Extracción Draft del método (ADR-008): preface, Parte II (05–09), Parte IV (13–15), apéndice B.
- Norma explícita: `specs/` del consumidor es la verdad operativa; el stack concreto queda fuera del core.
