---
pbi: ADR-004-tooling-externo
iteracion: Iteration-006
fecha: 2026-09-26
inicio: 2026-09-26T17:25:00+02:00
fin: 2026-09-26T17:29:26+02:00
agente: humano + asistente IA (Claude Code)
modelo: claude-opus-5-5
version_prompt: N/D
prompt_base: ninguno (encargo ad hoc en chat; sin prompt versionado de prompts/)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano, git-remoto-encargo
ad_hoc: "Encargo del humano: «Adelante» sobre dos ofertas, confirmado con elección explícita: borrar ramas fusionadas y hacer el seguimiento de ADR-004 (rama + PR sobre sdaf-bootstrap y AGENTS.md.template; sin tag ni release)."
contexto: "Seguimiento de ADR-004: llevar la cláusula de precedencia del tooling externo a AGENTS.md.template y a sdaf-bootstrap como sección opcional, condicionada a tooling.gentle_ai."
especificaciones_utilizadas: "architecture/decisions/ADR-004-tooling-externo-de-agentes.md (consecuencias); docs/integracion-gentle-ai.md (cláusula); handbook/06-ai-agent-framework.md §7; handbook/13-enmienda-excepciones-ciclo-de-vida.md §5 y §6; docs/adopcion-y-upgrade.md (versiones de artefactos alineadas a la línea); skills/sdaf-upgrade/SKILL.md paso 4"
archivos_leidos: "AGENTS.md.template; skills/sdaf-bootstrap/SKILL.md; skills/sdaf-worklog-handoff/SKILL.md (orden del historial); skills/sdaf-upgrade/SKILL.md; scripts/check-version-metadata.py; scripts/check-local-links.py; docs/integracion-gentle-ai.md; docs/adopcion-y-upgrade.md"
archivos_modificados: "AGENTS.md.template (0.4.2, sección Tooling externo opcional); skills/sdaf-bootstrap/SKILL.md (0.4.2, pasos 2, 3, 7 y DoD); docs/integracion-gentle-ai.md; architecture/decisions/ADR-004-tooling-externo-de-agentes.md (consecuencias y enlace); handbook/CHANGELOG.md (entrada 0.4.2); CHANGELOG.md; README.md; docs/adopcion-y-upgrade.md (sección 0.4.2); este worklog"
origen_cambios: mixto
resultado: "AGENTS.md.template y sdaf-bootstrap en 0.4.2: la sección «Tooling externo (opcional)» declara la precedencia de Gate 0, H06 §7 y worklogs sobre sdd-*, ODD y la memoria del tooling, y se borra al materializar si tooling.gentle_ai no se declara. Parche 0.4.2 en handbook/CHANGELOG.md, no breaking; el tag v0.4.2 se crea tras el merge (este encargo no lo incluye). Antes, las ramas locales ya fusionadas por squash (#24, #25, #26) se borraron tras comprobar que su árbol coincidía con el merge; en GitHub ya no existían."
tiempo: PT4M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: 309529
  fuente: "get_usage de Claude Code durante la iteración: tokens de contexto acumulados de la sesión (incluye Iteration-001 a 005), no el total procesado. Plan Pro: sin importe por uso."
observaciones: "inicio es aproximado: la herramienta no expone la hora del mensaje del humano; la primera hora medida en la iteración es 17:27:25. Versión 0.4.2 para ambos artefactos por la convención de alinear la versión del artefacto con la línea en que cambia (sdaf-worklog-handoff 0.4.0). Commit, push de la rama y PR autorizados por la elección «rama + PR»; sin merge, tag ni release (H06 §7)."
pruebas_ejecutadas: "Locales, exit 0, mismo conjunto que validate.yml: validate-config.py, test-validate-config.py, test-worklog.py, check-version-metadata.py, check-history-append-only.py, check-adrs.py, test-dates.py, measure-handbook-scaffolding.py, validate-worklog.py (plantilla y worklogs), check-worklog-presence.py, check-local-links.py --strict-anchors --strict-orphans. markdownlint (MD040, MD042) revisado a mano (sin Node). mkdocs build --strict: no ejecutado en local; lo cubre el CI."
estado: hecho
siguiente_agente: humano (QG-Review del PR; merge y, si procede, tag v0.4.2)
commit: null
pr: null
rama: docs/adr-004-seguimiento
sha: null
resumen_acumulado: "ad hoc (chat) — AGENTS.md.template y sdaf-bootstrap 0.4.2 con sección de tooling externo opcional; rama docs/adr-004-seguimiento; commit/PR/SHA en la descripción del PR"
---

# ADR-004-tooling-externo / Iteration-006

## Línea de decisión

- Sección opcional en la plantilla, no un fichero aparte: el router del consumidor es un solo `AGENTS.md` ([H06](../../handbook/06-ai-agent-framework.md)).
- Se borra al materializar si no hay `tooling.gentle_ai`: la adopción sigue siendo opcional ([ADR-004](../../architecture/decisions/ADR-004-tooling-externo-de-agentes.md), decisión 7).
- La excepción de commit para ODD no viene activada: solo se ofrece la forma de enumerarla ([H06 §7](../../handbook/06-ai-agent-framework.md#7-restricciones-globales)).
- Parche 0.4.2, no minor: ningún capítulo Approved cambia de obligación y nada obliga a quien no adopta tooling ([H13 §5](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md)).

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | Plantilla, skill y docs: `mixto` (redacción IA; alcance elegido por el humano). |
