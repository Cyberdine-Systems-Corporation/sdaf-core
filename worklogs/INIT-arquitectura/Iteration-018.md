---
pbi: INIT-arquitectura
iteracion: Iteration-018
fecha: 2026-10-12
inicio: 2026-10-12T18:35:00+02:00
fin: 2026-10-12T18:37:00+02:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano: «Si» a aceptar el ADR-009 ahora, antes de publicar el slice S5."
contexto: "Aceptación de ADR-009 (idioma fijo de los artefactos de ingeniería), decisión D-8 de INIT-arquitectura."
especificaciones_utilizadas: "handbook/00-preface.md §3.3; architecture/decisions/ADR-009; ADR-006; scripts/check-adrs.py; docs/iniciativas/INIT-arquitectura.md (D-8, ARQ-3.12)"
archivos_leidos: "architecture/decisions/ADR-009; architecture/decisions/README.md; docs/iniciativas/INIT-arquitectura.md"
archivos_modificados: "architecture/decisions/ADR-009-idioma-de-artefactos.md; architecture/decisions/README.md; docs/iniciativas/INIT-arquitectura.md (plan 0.1.16); docs/iniciativas/README.md; este worklog."
origen_cambios: N/A
resultado: "ADR-009 pasa a Aceptado con fila Aceptación (decisor humano, transcrita del encargo). La nota del esquema, el JSON y los ejemplos ya remiten a un ADR aceptado. Índice y plan actualizados."
tiempo: PT2M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "La aceptación la decide el humano; el agente solo transcribe (H00 §3.3). Sin efecto normativo nuevo: no cambia ningún capítulo, gate ni validación del esquema. Se acepta antes de publicar S5 para que v0.5.0 salga con la referencia del esquema apuntando a un ADR aceptado. Cambiar project.language o abrir otro idioma exige ahora un ADR sustituto (ADR-006 §3). Sin push ni PR salvo orden posterior."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (confirmar el commit local; después publicar el PR de S5)
commit: null
pr: null
rama: feat/linea-0.5.0-05-bootstrap-idioma
sha: null
resumen_acumulado: "ad hoc — ADR-009 Aceptado en la rama local de S5; sin PR/tag"
---

# INIT-arquitectura / Iteration-018

## Línea de decisión

- Aceptante: Manuel Ortiz de Villajos Quirós (CODEOWNERS), 2026-10-12T18:37+02:00, a petición expresa en el chat. El agente transcribe; no autodeclara.
- ARQ-3.12 queda completo: la restricción `es` tiene una decisión citable y aceptada.
- El cambio se apila en la rama de S5 porque comparte el índice de ADRs y el plan, y evita un PR adicional.

## Pruebas

`check-adrs.py` (9 ADRs), `test-adrs.py`, `check-version-metadata.py`, `check-history-append-only.py`, `validate-worklog.py` (Iteration-001 a 018) y `check-local-links.py --strict-anchors --strict-orphans` (copia limpia). markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | Redacción IA; aceptación del humano. |
