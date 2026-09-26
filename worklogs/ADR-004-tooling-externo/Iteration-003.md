---
pbi: ADR-004-tooling-externo
iteracion: Iteration-003
fecha: 2026-09-26
inicio: 2026-09-26T08:54:00+02:00
fin: 2026-09-26T09:46:00+02:00
agente: humano + asistente IA (Claude Code)
modelo: claude-opus-5-5
version_prompt: N/D
prompt_base: ninguno (encargo ad hoc en chat; sin prompt versionado de prompts/)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano, git-remoto-encargo
ad_hoc: "Encargo del humano: la adopción de gentle-ai debe ser opcional. Elección del humano: además, clave en sdaf.config. Valores admitidos: el humano no expresó preferencia; se aplica la opción recomendada (null o semver publicado)."
contexto: "Hacer explícito que adoptar gentle-ai es opcional y dar al consumidor una clave para declararlo: tooling.gentle_ai en sdaf.config.yaml."
especificaciones_utilizadas: "handbook/13-enmienda-excepciones-ciclo-de-vida.md §5 y §6; handbook/00-preface.md §3; sdaf.config.schema.yaml; sdaf.config.schema.json; examples/README.md; architecture/decisions/ADR-004-tooling-externo-de-agentes.md"
archivos_leidos: "sdaf.config.schema.json; sdaf.config.schema.yaml; sdaf.config.example.yaml; examples/README.md; examples/08-completo.yaml; scripts/validate-config.py; scripts/test-validate-config.py; scripts/validate-examples.py; scripts/testdata/i4-extension-without-pack.yaml; configuracion/schema.md; .github/actions/validate-sdaf/action.yml; skills/sdaf-bootstrap/SKILL.md; handbook/13-enmienda-excepciones-ciclo-de-vida.md"
archivos_modificados: "sdaf.config.schema.json (bloque tooling); sdaf.config.schema.yaml (sección tooling y relación con AGENTS.md); examples/08-completo.yaml; examples/README.md; scripts/test-validate-config.py; scripts/testdata/tooling-invalid.yaml (nuevo); architecture/decisions/ADR-004-tooling-externo-de-agentes.md (decisión 7, consecuencias, enlace); docs/integracion-gentle-ai.md (alerta y sección Adopción opcional); este worklog"
origen_cambios: mixto
resultado: "Bloque opcional tooling con additionalProperties false y tooling.gentle_ai = null | semver. Ausente o null = no adoptado; 01–07 y sdaf.config.example.yaml sin cambios; 08 lo declara como techo. Test nuevo: gentle_ai: main falla y nombra la clave. ADR-004 gana la decisión 7 (adopción opcional) y declara el cambio de schema aditivo y no breaking (H13 §5). La guía abre con «opcional» y el criterio para decidir."
tiempo: "N/D: la herramienta no expone la hora de los mensajes del humano; inicio es la cota del fin de Iteration-002 e incluye la espera entre turnos"
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: 211187
  fuente: "get_usage de Claude Code a las 09:43 (+02:00): tokens de contexto acumulados de la sesión (incluye Iteration-001 y 002), no el total procesado. Plan Pro: sin importe por uso."
observaciones: "Sin fila de handbook/CHANGELOG ni bump de línea: se escriben al aceptar ADR-004 (H00 §3.3); el merge del cambio de schema debería esperar a esa aceptación. sdaf-bootstrap y AGENTS.md.template (Approved) no se tocan; mencionar la clave en ellos queda como seguimiento tras la aceptación. Sin commit, push ni PR (H06 §7)."
pruebas_ejecutadas: "Locales, exit 0: validate-config.py (examples y sdaf.config.example.yaml), test-validate-config.py (incluido el caso tooling), check-adrs.py, check-local-links.py --strict-anchors --strict-orphans, validate-worklog.py (Iteration-001 a 003), check-version-metadata.py, check-history-append-only.py, test-worklog.py, check-worklog-presence.py. Manual: configs sin bloque tooling, con gentle_ai null y con \"3.7.0\" validan; con main falla. MD040 y MD042 revisadas a mano (sin Node). mkdocs build --strict: no ejecutado en local; lo cubre el CI."
estado: hecho
siguiente_agente: humano (revisión del diff, aceptación o rechazo de ADR-004, CHANGELOG y bump al aceptar, commit y PR)
commit: null
pr: null
rama: docs/adr-004-tooling-externo
sha: null
resumen_acumulado: "ad hoc (chat) — adopción opcional de gentle-ai y clave tooling.gentle_ai; rama docs/adr-004-tooling-externo; commit/PR/SHA ausentes"
---

# ADR-004-tooling-externo / Iteration-003

## Línea de decisión

- Clave opcional y aditiva: ninguna config existente deja de validar, así que no es breaking ([H13 §5](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md)).
- `tooling` como bloque cerrado (`additionalProperties: false`): admite otro tooling después sin abrir la raíz.
- Solo `null` o semver publicado: una rama no fija versión, y SDD difiere entre v3.7.0 y `main` ([Iteration-002](Iteration-002.md)).
- El fixture `tooling-invalid.yaml` es válido salvo la clave nueva, para que el fallo solo se explique por ella (mismo patrón que `i4-extension-without-pack.yaml`).
- Sin CHANGELOG ni bump hasta la aceptación de ADR-004 ([H00 §3](../../handbook/00-preface.md)).

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | Schema, ejemplos, test, ADR y guía: `mixto` (redacción IA; decisión de la clave, humana). |
