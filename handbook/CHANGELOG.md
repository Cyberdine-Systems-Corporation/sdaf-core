# CHANGELOG — handbook sdaf-core

## 0.3.3 — 2026-09-19

Parche (**no** breaking de citas `H00`–`H08`). H06 §7: **encargo vigente** = el mensaje de usuario de **este turno**. El historial de la conversación, un PR abierto o terminar archivos no autorizan commit ni escritura al remoto. Autoriza solo lo que este mensaje nombra.

Copia operativa: regla IDE `git-remoto-encargo`, `AGENTS.md.template`, `prompts/system/master-architect.md`.

`sdaf.version` puede seguir `0.3.0`. Pin de árbol: el tag posterior a este parche.

## 0.3.2 — 2026-09-19

Parche (**no** breaking de citas `H00`–`H08`). Ganchos de gobernanza **sin estatizar adopción**:

- H12 §3: catálogo de referencias con uso **baseline** / **overlay** (N/A salvo ADR) / **fuera del método** (GRC o handbook de producto). SSDF/800-218A, SBOM/AIBOM y 42001/AI Act/CRA no entran en el baseline.
- H12 §5.2 / H10: QG-Sec alineado al mapa §4.3 (secreto, bypass de auth, injection, SSRF, CVE crítica identificada en el review). Scanner con umbral = overlay.
- H10: QG-Review exige aprobación humana nominada del merge; el dictamen del agente no basta.
- H08 §4.3: origen de cambios (`humano` / `ia` / `mixto` / `dependencia`) en worklogs **nuevos** de código de producto; sin backfill.
- Catálogo: `security-review` prioridad alta.

`sdaf.version` puede seguir `0.3.0`. Pin de árbol: el tag posterior a este parche.

## 0.3.1 — 2026-09-19

Parche (**no** breaking de citas `H00`–`H08`). Enmienda de H06: los agentes no crean commit local ni alteran el remoto del proyecto sin petición humana explícita. El criterio es el **efecto** (el remoto cambia), no el comando: push, tags, releases, merge, PR, APIs de contenidos, CI que escriba el repo. Terminar archivos o un DoD no autoriza git.

El consumidor puede exceptuarlo por cláusula en su `AGENTS.md` o por ADR; la cláusula debe **enumerar** qué permite. Lo no enumerado sigue prohibido. Force-push, reescribir historia y auto-merge siguen exigiendo orden humana.

`sdaf.version` puede seguir `0.3.0`. Pin de árbol: el tag posterior a este parche (no exige retag de `v0.3.0` si aún no existe).

## 0.3.0 — 2026-09-19

Línea nueva de constitución (**no** breaking de citas `H00`–`H08`). Caps. 09–12, apéndice B, skills y prompts Parte III: **Approved** (aprobación humana del director técnico).

- Parte III — Calidad y entrega: H09 Testing, H10 Review/QG, H11 DevOps, H12 Security (trasplante genérico extract H16/H17/H18/H20; stack y producto fuera).
- Apéndice B: glosario de método (sin ubiquitous language de dominio).
- Skills `testing-review-pr`, `security-review`, `devops-ci-gate`.
- Prompts `prompts/review/`, `prompts/quality/`, `prompts/planning/`.
- Plantilla `templates/security.md` (el consumidor materializa `SECURITY.md`).

El consumidor puede seguir pinneado a `v0.2.1` / `sdaf.version` `0.2.0` hasta que adopte esta línea. Pin de árbol 0.3.0: tras el tag `v0.3.0`.

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
