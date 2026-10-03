---
pbi: INIT-arquitectura
iteracion: Iteration-006
fecha: 2026-10-03
inicio: 2026-10-03T11:00:00+02:00
fin: 2026-10-03T11:02:00+02:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano: «Acepta ADR-005»."
contexto: "ARQ-2.1 de INIT-arquitectura (en curso): aceptación de ADR-005, línea base arquitectónica del consumidor."
especificaciones_utilizadas: "handbook/00-preface.md §3.3; handbook/13-enmienda-excepciones-ciclo-de-vida.md; architecture/decisions/ADR-004 (precedente de fila Aceptación); scripts/check-adrs.py"
archivos_leidos: "architecture/decisions/ADR-005 y ADR-004; architecture/decisions/README.md; docs/iniciativas/INIT-arquitectura.md; scripts/check-adrs.py"
archivos_modificados: "architecture/decisions/ADR-005-linea-base-arquitectonica.md; architecture/decisions/README.md; docs/iniciativas/INIT-arquitectura.md (plan 0.1.4); docs/iniciativas/README.md; este worklog."
origen_cambios: N/A
resultado: "ADR-005 pasa a Aceptado con fila Aceptación (decisor humano, transcrita del encargo). Índice de ADRs y plan actualizados. ADR-006, 007 y 008 siguen Propuestos."
tiempo: PT2M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "La aceptación la decide el humano; el agente solo transcribe (H00 §3.3). Sin push, rama remota, PR ni tag salvo orden posterior. Aceptar ADR-005 no activa nada en los consumidores: G0.6 y la línea base entran con la línea 0.5.0 (opt-in), cuando se publiquen ARQ-3.1 a 3.13. ADR-005 referencia a ADR-006 (estados y sustitución) y ADR-007 (precedencia): sus puntos 2 y 6 dependen de que ambos se acepten antes de 0.5.0."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (aceptación o rechazo de ADR-006, ADR-007 §2 y ADR-008, ARQ-2.1)
commit: null
pr: null
rama: docs/aceptar-adr-005
sha: null
resumen_acumulado: "ad hoc — ADR-005 Aceptado (ARQ-2.1 en curso) en rama local"
---

# INIT-arquitectura / Iteration-006

## Línea de decisión

- Decisor: Manuel Ortiz de Villajos Quirós (CODEOWNERS), 2026-10-03T11:01+02:00, a petición expresa en el chat. El agente transcribe la aceptación; no la autodeclara.
- El texto «ruta pendiente de la decisión D-2» se cambia por «ruta fijada por la decisión D-2 … cerrada el 2026-10-02»; no cambia el sentido de la decisión.
- El índice de ADRs y el plan (0.1.4) reflejan el estado; ARQ-2.1 queda «en curso» hasta aceptar o rechazar ADR-006, 007 y 008.
- Aceptar ADR-005 no obliga a ningún consumidor: la línea base entra con `0.5.0` (opt-in).

## Pruebas

`check-adrs.py`, `test-dates.py`, `check-version-metadata.py`, `check-history-append-only.py`, `validate-worklog.py` (Iteration-001 a 006) y `check-local-links.py --strict-anchors --strict-orphans` (copia limpia). markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | Redacción IA; aceptación del humano. |
