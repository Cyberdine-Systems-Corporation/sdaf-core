---
pbi: INIT-arquitectura
iteracion: Iteration-014
fecha: 2026-10-08
inicio: 2026-10-08T23:03:00+02:00
fin: 2026-10-08T23:12:00+02:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: chained-pr
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano: «acepto las recomendaciones» sobre las cuatro decisiones de S3, tras «Siguiente paso»."
contexto: "ARQ-3.5, ARQ-3.4 y ARQ-3.10 de INIT-arquitectura (slice S3 de v0.5.0): estándar de specs, árbol del consumidor y plantilla de PBI."
especificaciones_utilizadas: "architecture/decisions/ADR-005 §2 y §7; ADR-008 §5; handbook/14-architecture-description.md; handbook/13-enmienda-excepciones-ciclo-de-vida.md §6; docs/iniciativas/INIT-arquitectura.md (ARQ-3.4, 3.5, 3.10)"
archivos_leidos: "handbook/03, 04, 05, 08 y 14 (y sus _meta); templates/spec.md; skills/spec-draft-pbi; prompts/planning/backlog-refinement.md; handbook/A-templates.md; mkdocs/mkdocs.yml; scripts de validación"
archivos_modificados: "handbook/04 y 03 (0.3.0), 05 (0.4.0), 14 (0.1.2) y sus _meta; handbook/index.yaml; handbook/A-templates.md y _meta (0.3.5); mkdocs/mkdocs.yml; templates/spec.md; templates/pbi.md (nuevo); skills/spec-draft-pbi (0.3.0); prompts/planning/backlog-refinement.md (0.4.0); docs/iniciativas/INIT-arquitectura.md (plan 0.1.12); docs/iniciativas/README.md; este worklog."
origen_cambios: "handbook, plantillas, skill y prompt: redacción de un subagente escritor delegado, revisada por el orquestador."
resultado: "H04 define el tipo de integración, los campos Unidades y Origen y los atributos de calidad con escenario medible; H03 incorpora architecture/description.md y specs/integration/; templates/pbi.md y G0.4 comprobable; skill y prompt de backlog usan la plantilla; la cita de trazabilidad de H14 apunta a H08 §6."
tiempo: PT9M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "Cambios de significado en capítulos Approved: H04 y H03 suben a 0.3.0 y H05 a 0.4.0 (un bump por slice; S4b llevará H05 a 0.5.0 con G0.3 y G0.6); la entrada del CHANGELOG del handbook es de la release (S6). H14 sube a 0.1.2 solo por corregir una cita (sin cambio de norma). Origen queda como campo opcional; el valor caracterización se define en v0.5.1 (ARQ-5.2). Ajuste del orquestador: H04 §5.5 se alinea con H14 §3 (la línea base resume el escenario y enlaza la spec; si difieren, manda la spec). Punto abierto, no resuelto en este slice: G0.4 exige las unidades de la línea base, que un consumidor sin línea base no puede citar; es coherente con la línea 0.5.0, que exige G0.6, pero el slice S4b debe dejar claro en H05 que G0.4 y G0.6 van juntos. El historial de templates/pbi.md lleva fecha real (check-history-append-only exige hora y zona). Sin push ni PR salvo orden posterior."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (revisión, confirmación de commits locales; después publicar el PR de S3)
commit: null
pr: null
rama: feat/linea-0.5.0-03-specs-arbol-pbi
sha: null
resumen_acumulado: "ad hoc — S3 / ARQ-3.5, 3.4 y 3.10 en rama local; sin commit/PR/tag"
---

# INIT-arquitectura / Iteration-014

## Línea de decisión

- Decisiones del humano (2026-10-08, «acepto las recomendaciones»): crear ya `specs/integration/`; alinear el campo «PBIs / backlog» de la plantilla con H04; corregir la cita de H14 a H08 §6 (patch); un bump de H05 por slice.
- H03 y H04 son cambios de significado de capítulos Approved ([H13 §6](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md)): bump minor. La aprobación del PR de S3 por el humano es la revisión formal que exige H13.
- La prueba de abstracción se verifica con una búsqueda de estilos, notaciones y stacks sobre lo añadido: sin coincidencias.
- Trazabilidad ODD: ruta de redacción delegada (disparador de escritura); mapeo previo delegado; verificación repetida por el orquestador.

## Pruebas

`check-version-metadata.py`, `check-history-append-only.py`, `measure-handbook-scaffolding.py`, `check-adrs.py`, `test-adrs.py`, `validate-config.py`, `validate-examples.py`, `validate-worklog.py` (Iteration-001 a 014) y `check-local-links.py --strict-anchors --strict-orphans` (copia limpia). markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| handbook/03, 04, 05, 14; templates/spec.md y pbi.md; skill y prompt | IA | Subagente escritor; revisado |
| Índices, mkdocs, A-templates | IA | Redacción |
