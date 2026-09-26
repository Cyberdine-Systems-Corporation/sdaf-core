---
pbi: ADR-004-tooling-externo
iteracion: Iteration-005
fecha: 2026-09-26
inicio: 2026-09-26T11:41:14+02:00
fin: 2026-09-26T11:42:49+02:00
agente: humano + asistente IA (Claude Code)
modelo: claude-opus-5-5
version_prompt: N/D
prompt_base: ninguno (encargo ad hoc en chat; sin prompt versionado de prompts/)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano, git-remoto-encargo
ad_hoc: "Encargo del humano en este turno: «Acepta ADR-004, añade entrada en changelog, sube versión, commit y PR»."
contexto: "Aceptación humana de ADR-004 y publicación del cambio como parche 0.4.1 en un PR."
especificaciones_utilizadas: "handbook/00-preface.md §3.3; handbook/06-ai-agent-framework.md §7; handbook/13-enmienda-excepciones-ciclo-de-vida.md §5, §6 y §9; architecture/decisions/ADR-003-formato-de-artefactos.md (forma de la fila Aceptación); handbook/CHANGELOG.md (entradas 0.4.0 y 0.3.x); .github/pull_request_template.md"
archivos_leidos: "handbook/CHANGELOG.md; CHANGELOG.md; README.md; docs/adopcion-y-upgrade.md; CODEOWNERS; .github/pull_request_template.md; commits 93c17ca, fa48537 y cd1742e (patrón de versión y de tag «tras el merge»)"
archivos_modificados: "architecture/decisions/ADR-004-tooling-externo-de-agentes.md (Aceptado, fila Aceptación, consecuencias); architecture/decisions/README.md; docs/integracion-gentle-ai.md; handbook/CHANGELOG.md (entrada 0.4.1); CHANGELOG.md; README.md (Contenido v0.4.1, docs, release); docs/adopcion-y-upgrade.md (sección 0.4.1); este worklog"
origen_cambios: mixto
resultado: "ADR-004 Aceptado con la aceptación transcrita del encargo (2026-09-26T11:41+02:00). Parche 0.4.1 en handbook/CHANGELOG.md, no breaking; sdaf.version sigue en 0.4.0. README y HOWTO de adopción anuncian v0.4.1 tras el merge, con el mismo patrón que la línea 0.4.0. Badge de release, tags publicados y pin recomendado siguen en v0.4.0 hasta que exista el tag."
tiempo: PT1M35S
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: 266574
  fuente: "get_usage de Claude Code durante la iteración: tokens de contexto acumulados de la sesión (incluye Iteration-001 a 004), no el total procesado. Plan Pro: sin importe por uso."
observaciones: "La aceptación la da el humano en el encargo; el asistente solo la transcribe (H00 §3.3). El encargo nombra commit y PR: autoriza el commit, el push de la rama imprescindible para abrir el PR y el PR (H06 §7); no autoriza merge, tag ni release. commit, pr y sha quedan en null: el worklog entra en el mismo commit que documenta y no puede contener su propio SHA; se enlazan desde el PR."
pruebas_ejecutadas: "Locales, exit 0, mismo conjunto que validate.yml: validate-config.py, test-validate-config.py, test-worklog.py, check-version-metadata.py, check-history-append-only.py, check-adrs.py, test-dates.py, measure-handbook-scaffolding.py, validate-worklog.py (plantilla y worklogs/**), check-worklog-presence.py, check-local-links.py --strict-anchors --strict-orphans. markdownlint (MD040, MD042) revisado a mano (sin Node). mkdocs build --strict: no ejecutado en local; lo cubre el job docs-build del PR."
estado: hecho
siguiente_agente: humano (QG-Review del PR, merge y tag v0.4.1)
commit: null
pr: null
rama: docs/adr-004-tooling-externo
sha: null
resumen_acumulado: "ad hoc (chat) — ADR-004 Aceptado y parche 0.4.1; rama docs/adr-004-tooling-externo; commit/PR/SHA en la descripción del PR"
---

# ADR-004-tooling-externo / Iteration-005

## Línea de decisión

- Parche y no minor: no cambia ningún capítulo Approved y el schema solo gana un bloque opcional ([H13 §5 y §6](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md)).
- `sdaf.version` sigue en `"0.4.0"`: nombra la línea, no el parche ([`docs/adopcion-y-upgrade.md`](../../docs/adopcion-y-upgrade.md)).
- El tag `v0.4.1` se crea tras el merge, como `v0.4.0`; mientras tanto, el pin publicado sigue en `v0.4.0`.
- Fila Aceptación con la forma de [ADR-003](../../architecture/decisions/ADR-003-formato-de-artefactos.md): fecha con hora y zona, quién, y que el agente solo transcribe.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | Aceptación y versión: decisión humana; redacción IA. |
