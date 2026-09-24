---
pbi: INIT-auditoria-v0.3.3
iteracion: Iteration-001
fecha: 2026-09-24
inicio: 2026-09-24T08:49:43+02:00
fin: 2026-09-24T18:55:14+02:00
agente: humano + asistente IA (Claude Code)
modelo: claude-opus-5-5 (revisión, correcciones y registro de la aceptación); N/D para la implementación previa de los bloques 0–5
version_prompt: N/D
prompt_base: ninguno (encargo ad hoc en chat; sin prompt versionado de prompts/)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano, git-remoto-encargo
ad_hoc: "Plan de auditoría v0.3.3 (23 PBIs, bloques 0–5) pegado en chat; no versionado en el repo. Encargos del humano: confirmar cobertura del plan, aplicar correcciones, aceptar la línea 0.4.0, cerrar H10, confirmar decisiones, renumerar ADRs desde 001 e incluir este worklog."
contexto: "Cierre de los doce hallazgos de la auditoría de sdaf-core v0.3.3 y publicación de la línea de constitución 0.4.0."
especificaciones_utilizadas: "Plan de auditoría (chat); handbook/00-preface.md §3; handbook/03-repository-organization.md §2; handbook/06-ai-agent-framework.md §7; handbook/07-prompt-engineering-standard.md §4 y §7; handbook/08-agent-traceability.md §4–§7; handbook/10-code-review-and-quality-gates.md §2 y §3.1; handbook/13-enmienda-excepciones-ciclo-de-vida.md; sdaf.config.schema.yaml (invariantes 1–4)"
archivos_leidos: ".github/workflows/validate.yml; .github/actions/validate-sdaf/; handbook/*.md y handbook/_meta/*.yaml; handbook/index.yaml; handbook/CHANGELOG.md; architecture/decisions/*.md; scripts/*.py; templates/worklog.md; worklog.schema.json; sdaf.config.schema.yaml; docs/adopcion-y-upgrade.md; README.md; CONTRIBUTING.md; CODEOWNERS"
archivos_modificados: "Raíz: .editorconfig, .markdownlintignore, CHANGELOG.md, CODEOWNERS, CONTRIBUTING.md, SECURITY.md, README.md, sdaf.config.*, worklog.schema.json. CI: .github/workflows/validate.yml, .github/dependabot.yml, .github/actions/validate-sdaf/, .github/pull_request_template.md. Norma: handbook/ (00, 03, 07, 08, 10, 13, A, B, README, CHANGELOG, _meta/, index.yaml), architecture/decisions/ (ADR-001–003). Artefactos: agents/*.md, skills/*/SKILL.md, templates/, AGENTS.md.template, examples/*.yaml. Tooling: scripts/ (validate-config, validate-worklog, check-version-metadata, check-history-append-only, check-worklog-presence, check-local-links, sdaf_meta, extract-handbook-meta, measure-handbook-scaffolding, tests y testdata). Docs: docs/adopcion-y-upgrade.md, mkdocs/mkdocs.yml. Este worklog."
origen_cambios: mixto
resultado: "23 PBIs del plan implementados. Correcciones: resolución de enlaces de _meta, chequeo de worklog que falla si no puede calcular el diff, tres filas de historial restauradas, checker de historial que solo crece, formato de sha y fecha en el schema de worklog. Aceptación humana: H13 Approved, H00/H08/H10 0.4.0, ADR-001–003 Aceptados, línea 0.4.0 en el CHANGELOG. ADRs del core renumerados desde 001. Worklog: inicio/fin con hora y zona, tiempo ISO 8601 y coste estructurado; N/D solo con motivo. Fechas con hora y zona desde la línea 0.4.0 en cabeceras, historiales, ADRs y CHANGELOG (H13 §9); fechas de cabecera alineadas con la fila más reciente. Checker de ADRs (numeración, estado, fechas, índice) y fixtures de los checkers de fechas."
tiempo: PT10H5M31S
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: 297756
  fuente: "get_usage de Claude Code a las 18:55 (+02:00): tokens de contexto de la sesión, no el total procesado. Plan Pro: sin importe por uso; la sesión consumió cuota del plan, no atribuible solo a ella."
observaciones: "La implementación de los bloques 0–5 (2026-09-23) es anterior a la sesión que redacta este worklog y no dejó registro de agente, modelo, tiempo ni coste; se declara N/D en lugar de reconstruirlo. inicio, fin, tiempo y coste miden solo la sesión del 2026-09-24: inicio es la creación de la sesión y tiempo es el transcurrido por reloj, no el tiempo activo, que la herramienta no expone. La aceptación de 2026-09-24 la dio el humano en el encargo; el asistente solo la transcribió (H00 §3.3). Sin commit, PR ni tag en esta iteración: cada uno exige orden humana expresa (H06 §7)."
pruebas_ejecutadas: "Locales, exit 0: validate-config.py, test-validate-config.py, test-worklog.py, check-version-metadata.py, check-history-append-only.py, check-adrs.py, test-dates.py (16 casos), measure-handbook-scaffolding.py, validate-worklog.py, check-worklog-presence.py. check-local-links.py --strict-anchors --strict-orphans: OK tras excluir mkdocs/ (espejo de symlinks que mkdocs.yml ya excluye; en Linux sus enlaces se resolvían desde mkdocs/src/ y el CI del PR #16 falló por ello). markdownlint: MD040 y MD042, únicas reglas activas, comprobadas con script local (sin Node). mkdocs build --strict: verde en el CI del PR (docs-build)."
estado: hecho
siguiente_agente: humano (revisión del diff, rama, commit, PR, merge y tag v0.4.0)
commit: null
pr: null
rama: feat/linea-0.4.0
sha: null
resumen_acumulado: "ad hoc (chat) — auditoría v0.3.3 → línea 0.4.0; commit/PR/SHA en la descripción del PR; rama feat/linea-0.4.0"
---

# INIT-auditoria-v0.3.3 / Iteration-001

## Línea de decisión

- Tags `v0.3.0` y `v0.3.1`: no se crean; el CHANGELOG declara su ausencia ([H13 §8](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md), [ADR-002](../../architecture/decisions/ADR-002-gobernanza-del-metodo.md)).
- I4: aviso por defecto y error con `--strict-i4` (H13 §8).
- Artefactos con versión y sin historial: fila inicial que repite la cabecera (H13 §8).
- QG-Review con un solo mantenedor: la identidad de `CODEOWNERS` puede aprobar su propio PR ([H10 §2](../../handbook/10-code-review-and-quality-gates.md), H13 §7).
- Andamiaje de capítulos en `handbook/_meta/` y worklog con frontmatter; `resumen_acumulado` es un índice de una línea ([ADR-003](../../architecture/decisions/ADR-003-formato-de-artefactos.md)).
- ADRs del core numerados desde 001; «ADR-008» en historiales hasta `v0.3.3` equivale a [ADR-001](../../architecture/decisions/ADR-001-nucleo-reutilizable.md).
- Historial publicado: solo se añaden filas ([H08 §7](../../handbook/08-agent-traceability.md)). Se restauraron tres filas borradas en la extracción: A `0.3.2`, H00 `0.3.0 / 2026-09-19` y `sdaf-worklog-handoff` `0.3.2`.
- Fechas nuevas con hora y zona (ISO 8601); las publicadas hasta `v0.3.3` conservan el día. La hora es medida: creación de ficheros (propuestas del 2026-09-23), registro de la aceptación (18:21) y registro de la forma final de la línea ([H13 §9](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md)).
- Este worklog existe porque el cambio es material de handbook y ADR ([H08 §5](../../handbook/08-agent-traceability.md)).

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | El core no contiene producto. Norma y tooling: `mixto` (redacción IA, decisiones y aceptación humanas). |

`commit`, `pr`, `rama` y `sha` quedan en `null`: el worklog entra en el mismo commit que documenta y no puede contener su propio SHA. Se completan cuando exista el PR, o se enlazan desde la descripción del PR.
