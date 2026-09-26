---
pbi: ADR-004-tooling-externo
iteracion: Iteration-004
fecha: 2026-09-26
inicio: 2026-09-26T09:46:00+02:00
fin: 2026-09-26T11:31:00+02:00
agente: humano + asistente IA (Claude Code)
modelo: claude-opus-5-5
version_prompt: N/D
prompt_base: ninguno (encargo ad hoc en chat; sin prompt versionado de prompts/)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano, git-remoto-encargo
ad_hoc: "Objeción del humano: si SDD choca con sdaf-core, ¿por qué la config impide adoptar main, que ya lo retiró? Elecciones del humano: admitir semver o SHA de commit, y avisar cuando la release incluye SDD."
contexto: "Corregir la incoherencia de la iteración 3: exigir semver obligaba a declarar v3.7.0 (con SDD) e impedía declarar main (sin SDD)."
especificaciones_utilizadas: "architecture/decisions/ADR-004-tooling-externo-de-agentes.md; sdaf.config.schema.yaml; sdaf.config.schema.json; handbook/13-enmienda-excepciones-ciclo-de-vida.md §5; gentle-ai: commit 520ed86e8c598b01f439e28c34d391cd6f1744e3 (merge del PR 4967, 2026-09-25T02:25:43Z)"
archivos_leidos: "scripts/validate-config.py; scripts/test-validate-config.py; sdaf.config.schema.json; sdaf.config.schema.yaml; examples/README.md; examples/08-completo.yaml; docs/integracion-gentle-ai.md"
archivos_modificados: "sdaf.config.schema.json (gentle_ai admite SHA de 40 hex); scripts/validate-config.py (aviso T1); scripts/test-validate-config.py; scripts/testdata/tooling-sdd-warning.yaml (nuevo); sdaf.config.schema.yaml (fila tooling.gentle_ai y T1); examples/08-completo.yaml (SHA); examples/README.md; architecture/decisions/ADR-004-tooling-externo-de-agentes.md (decisión 7 y enlaces); docs/integracion-gentle-ai.md (Adopción opcional e Instalación recomendada); este worklog"
origen_cambios: mixto
resultado: "tooling.gentle_ai acepta null, release semver o SHA de 40 hex; main y SHA cortos fallan. Aviso T1 (nunca error) si la release es ≤ 3.7.0: incluye sdd, que no se instala. 08 declara el SHA 520ed86e8… (commit de main que retira SDD) y no dispara T1. La guía explica cómo instalar ese commit con go install y cuándo excluir sdd."
tiempo: "N/D: la herramienta no expone la hora de los mensajes del humano; inicio es la cota del fin de Iteration-003 e incluye la espera entre turnos"
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: 244798
  fuente: "get_usage de Claude Code a las 11:29 (+02:00): tokens de contexto acumulados de la sesión (incluye Iteration-001 a 003), no el total procesado. Plan Pro: sin importe por uso."
observaciones: "El validador no evalúa SHAs: sin red no sabe si un commit es anterior a la retirada de SDD; el catálogo pide un SHA igual o posterior a 520ed86e8. El SHA existe y su fecha se verificó con la API de GitHub. Un primer intento de edición por heredoc falló en la primera sustitución por escapes y codificación, y no escribió nada (git diff --stat lo confirmó); se repitió desde un script UTF-8. Sin commit, push ni PR (H06 §7)."
pruebas_ejecutadas: "Locales, exit 0: validate-config.py, test-validate-config.py (casos tooling y T1), check-adrs.py, check-local-links.py --strict-anchors --strict-orphans, validate-worklog.py (Iteration-001 a 004), check-version-metadata.py, check-history-append-only.py, test-worklog.py, test-dates.py. Matriz manual: sin bloque y null OK; 3.7.0 y 3.6.1 OK con WARN T1; 3.8.0 y SHA de 40 hex OK sin aviso; main y SHA corto FAIL. MD040 y MD042 revisadas a mano (sin Node). mkdocs build --strict: no ejecutado en local; lo cubre el CI."
estado: hecho
siguiente_agente: humano (revisión del diff, aceptación o rechazo de ADR-004, CHANGELOG y bump al aceptar, commit y PR)
commit: null
pr: null
rama: docs/adr-004-tooling-externo
sha: null
resumen_acumulado: "ad hoc (chat) — tooling.gentle_ai admite SHA y aviso T1; rama docs/adr-004-tooling-externo; commit/PR/SHA ausentes"
---

# ADR-004-tooling-externo / Iteration-004

## Línea de decisión

- Exigir solo releases empujaba a adoptar la versión incompatible (v3.7.0, con SDD). Un SHA de 40 hex mantiene la reproducibilidad y permite adoptar `main` sin SDD ([Iteration-003](Iteration-003.md)).
- `main` literal sigue sin valer: una rama no fija qué versión rige.
- T1 es aviso y no error: con v3.7.0 se puede adoptar gentle-ai sin instalar `sdd` (preset `custom`) ([ADR-004](../../architecture/decisions/ADR-004-tooling-externo-de-agentes.md)).
- El ejemplo de techo (08) declara el SHA de la retirada para mostrar una versión compatible con el método.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | Schema, validador, ejemplos, ADR y guía: `mixto` (redacción IA; objeción y elecciones, humanas). |
