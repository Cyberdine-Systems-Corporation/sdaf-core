---
pbi: ADR-004-tooling-externo
iteracion: Iteration-001
fecha: 2026-09-26
inicio: 2026-09-26T08:26:22+02:00
fin: 2026-09-26T08:46:00+02:00
agente: humano + asistente IA (Claude Code)
modelo: claude-opus-5-5
version_prompt: N/D
prompt_base: ninguno (encargo ad hoc en chat; sin prompt versionado de prompts/)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano, git-remoto-encargo
ad_hoc: "Pregunta del humano: cómo encaja gentle-ai en este repositorio. Elección del humano: ADR + guía en el core. Encargo de implementación: en una rama independiente."
contexto: "Postura del core ante tooling externo de agentes (gentle-ai como caso de referencia) y guía HOWTO para usarlo en un consumidor sin saltar Gate 0 ni H06 §7."
especificaciones_utilizadas: "handbook/00-preface.md §3; handbook/05-development-workflow.md §3; handbook/06-ai-agent-framework.md §6 y §7; handbook/08-agent-traceability.md §5; handbook/10-code-review-and-quality-gates.md §2; handbook/12-security-standards.md; docs/contrato-pack-stack.md; docs/checklist-pagina-docs.md; templates/adr.md; documentación pública de gentle-ai (README, docs/components.md, docs/intended-usage.md, docs/usage.md, docs/non-interactive.md, docs/skill-registry.md, docs/engram.md) a 2026-09-25"
archivos_leidos: "README.md; AGENTS.md.template; skills/README.md; skills/sdaf-gate0/SKILL.md; docs/contrato-pack-stack.md; docs/README.md; docs/adopcion-y-upgrade.md; docs/checklist-pagina-docs.md; docs/mapa-navegacion.md; handbook/06-ai-agent-framework.md; handbook/08-agent-traceability.md; architecture/decisions/README.md; architecture/decisions/ADR-003-formato-de-artefactos.md; templates/adr.md; templates/worklog.md; scripts/check-adrs.py; scripts/check-worklog-presence.py; mkdocs/mkdocs.yml; .github/workflows/validate.yml; CONTRIBUTING.md; handbook/CHANGELOG.md"
archivos_modificados: "architecture/decisions/ADR-004-tooling-externo-de-agentes.md (nuevo); architecture/decisions/README.md; docs/integracion-gentle-ai.md (nuevo); docs/README.md; mkdocs/mkdocs.yml; este worklog"
origen_cambios: mixto
resultado: "ADR-004 en estado Propuesto (sin fila Aceptación): el core sigue tool-agnostic, el tooling externo es capa de entorno del consumidor, specs y worklogs son la única evidencia, ningún flujo externo sustituye a Gate 0, H06 §7 prevalece y la review automatizada no es QG-Review. Guía docs/integracion-gentle-ai.md con matriz de encaje, instalación recomendada (preset custom sin sdd), cláusula de precedencia para AGENTS.md, memoria vs worklog, limitación del registry con submodule y verificación. Índices de ADRs, docs y mkdocs actualizados."
tiempo: PT19M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: 129676
  fuente: "get_usage de Claude Code a las 08:43 (+02:00): tokens de contexto de la sesión, no el total procesado. Plan Pro: sin importe por uso."
observaciones: "Sin commit, push ni PR: el encargo nombra solo la rama (H06 §7). La rama docs/adr-004-tooling-externo sale de origin/main (cd1742e) y es solo local. La aceptación de ADR-004 corresponde a un humano (H00 §3.3). No hay bump ni fila de CHANGELOG: el ADR no cambia la constitución."
pruebas_ejecutadas: "Locales, exit 0: check-adrs.py, check-local-links.py --strict-anchors --strict-orphans, validate-worklog.py (este worklog), check-version-metadata.py, check-history-append-only.py, test-dates.py, test-worklog.py, check-worklog-presence.py. markdownlint: MD040 y MD042, únicas reglas activas, comprobadas a mano (sin Node). mkdocs build --strict: no ejecutado (mkdocs no instalado en local); lo cubre el job docs-build del CI."
estado: hecho
siguiente_agente: humano (revisión del diff, aceptación o rechazo de ADR-004, commit y PR)
commit: null
pr: null
rama: docs/adr-004-tooling-externo
sha: null
resumen_acumulado: "ad hoc (chat) — ADR-004 Propuesto + guía gentle-ai; rama docs/adr-004-tooling-externo; commit/PR/SHA ausentes"
---

# ADR-004-tooling-externo / Iteration-001

## Línea de decisión

- gentle-ai no es un pack: no aporta contratos, prompts ni ids de extensión ([contrato de pack](../../docs/contrato-pack-stack.md)). Se trata como capa de entorno del consumidor ([ADR-004](../../architecture/decisions/ADR-004-tooling-externo-de-agentes.md)).
- `sdd-*` se desaconseja: implementa sin Gate 0 ni specs Approved por humano ([H05 §3](../../handbook/05-development-workflow.md#3-gate-0-pre-implementación-stop)).
- ODD cierra tareas con commit: H06 §7 prevalece salvo excepción enumerada en el `AGENTS.md` del consumidor ([H06 §7](../../handbook/06-ai-agent-framework.md#7-restricciones-globales)).
- Engram es caché; la evidencia sigue en worklogs y specs ([H08](../../handbook/08-agent-traceability.md)).
- ADR en Propuesto: un agente no escribe la Aceptación ([H00 §3](../../handbook/00-preface.md)).
- Este worklog existe porque el cambio es un ADR material ([H08 §5](../../handbook/08-agent-traceability.md)).

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | El core no contiene producto. ADR y guía: `mixto` (redacción IA; elección de entregable y rama, humanas). |
