---
pbi: ADR-004-tooling-externo
iteracion: Iteration-002
fecha: 2026-09-26
inicio: 2026-09-26T08:46:00+02:00
fin: 2026-09-26T08:54:00+02:00
agente: humano + asistente IA (Claude Code)
modelo: claude-opus-5-5
version_prompt: N/D
prompt_base: ninguno (encargo ad hoc en chat; sin prompt versionado de prompts/)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano, git-remoto-encargo
ad_hoc: "Pregunta del humano: ¿se puede compatibilizar SDD con Gate 0? Plan aprobado: responder y ajustar la guía y el ADR en la misma rama."
contexto: "Encaje del ciclo SDD de gentle-ai con Gate 0, y corrección de la guía tras descubrir que gentle-ai retiró SDD/OpenSpec en main (PR 4967, merge 520ed86e8, 2026-09-25)."
especificaciones_utilizadas: "handbook/04-specification-standard.md §3, §6 y §7; handbook/05-development-workflow.md §3; handbook/06-ai-agent-framework.md §7; handbook/10-code-review-and-quality-gates.md §2; skills/sdaf-gate0/SKILL.md; skills/spec-draft-pbi/SKILL.md; gentle-ai: PR 4967, issue 4959, árbol de main, odd/tasks/remove-sdd-odd-only-main.md, releases (v3.7.0 la última)"
archivos_leidos: "handbook/04-specification-standard.md; handbook/05-development-workflow.md; skills/sdaf-gate0/SKILL.md; skills/spec-draft-pbi/SKILL.md; templates/spec.md; docs/integracion-gentle-ai.md"
archivos_modificados: "docs/integracion-gentle-ai.md (nota de revisión, fila sdd, aviso de presets, sección SDD y Gate 0); architecture/decisions/ADR-004-tooling-externo-de-agentes.md (contexto y enlace a worklogs); este worklog"
origen_cambios: mixto
resultado: "Respuesta: SDD se puede encajar con Gate 0 solo con condiciones (specs en specs/ con la plantilla SDAF, sdaf-gate0 entre sdd-tasks y sdd-apply, sdd-archive vetado, commits bajo H06 §7); no compensa, porque duplica las skills del core y gentle-ai lo retiró en main. Camino recomendado: ODD tras Gate 0. La guía distingue v3.7.0 (con SDD) de main (sin SDD) e incluye la tabla fase a fase y un diagrama. ADR-004 sigue en Propuesto."
tiempo: PT8M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: 170362
  fuente: "get_usage de Claude Code a las 08:51 (+02:00): tokens de contexto acumulados de la sesión (incluye Iteration-001, 129676 a las 08:43), no el total procesado. Plan Pro: sin importe por uso."
observaciones: "inicio es una cota: coincide con el fin de Iteration-001, porque la herramienta no expone la hora del mensaje del humano. La documentación de gentle-ai (docs/components.md) sigue listando SDD tras el merge del PR 4967; manda el árbol de main, que ya no contiene skills sdd-*. Sin commit, push ni PR (H06 §7)."
pruebas_ejecutadas: "Locales, exit 0: check-adrs.py, check-local-links.py --strict-anchors --strict-orphans, validate-worklog.py (Iteration-001 y 002), check-version-metadata.py, check-history-append-only.py. MD040 y MD042 revisadas a mano (sin Node). mkdocs build --strict: no ejecutado en local; lo cubre el CI."
estado: hecho
siguiente_agente: humano (revisión del diff, aceptación o rechazo de ADR-004, commit y PR)
commit: null
pr: null
rama: docs/adr-004-tooling-externo
sha: null
resumen_acumulado: "ad hoc (chat) — SDD frente a Gate 0 en la guía gentle-ai; rama docs/adr-004-tooling-externo; commit/PR/SHA ausentes"
---

# ADR-004-tooling-externo / Iteration-002

## Línea de decisión

- `sdd-archive` fusiona deltas en specs sin revisión humana: incompatible con [H04 §7](../../handbook/04-specification-standard.md#7-versionado-y-cambios).
- `sdd-apply` solo es admisible tras [`sdaf-gate0`](../../skills/sdaf-gate0/SKILL.md) y con commits bajo [H06 §7](../../handbook/06-ai-agent-framework.md#7-restricciones-globales).
- No se compatibiliza SDD: duplica `spec-draft-pbi`, `adr-propose`, `sdaf-gate0` y `testing-review-pr`, y gentle-ai lo retiró en `main` ([Gentleman-Programming/gentle-ai#4967](https://github.com/Gentleman-Programming/gentle-ai/pull/4967)).
- La guía distingue la versión publicada (v3.7.0, con SDD) de `main` (sin SDD).

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | Guía y ADR: `mixto` (redacción IA; pregunta y aprobación del plan, humanas). |
