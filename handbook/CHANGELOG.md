# CHANGELOG — handbook sdaf-core

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
