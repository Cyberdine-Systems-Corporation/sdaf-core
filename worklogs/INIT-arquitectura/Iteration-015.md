---
pbi: INIT-arquitectura
iteracion: Iteration-015
fecha: 2026-10-09
inicio: 2026-10-09T12:40:00+02:00
fin: 2026-10-09T12:46:00+02:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: chained-pr
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano: «41 fusionado» tras proponerle empezar S4a; continuar con la siguiente funcionalidad y pedir confirmación antes de cada commit local."
contexto: "ARQ-3.7 y ARQ-3.8 de INIT-arquitectura (slice S4a de v0.5.0): precedencia única y pipeline de dominio neutral."
especificaciones_utilizadas: "architecture/decisions/ADR-007 §1 y §2; ADR-005 §3 y §8; ADR-006 §4; handbook/14-architecture-description.md; docs/iniciativas/INIT-arquitectura.md (ARQ-3.7, 3.8, D-3)"
archivos_leidos: "handbook/01, 05 y README; handbook/_meta/01; handbook/index.yaml; AGENTS.md.template; ADR-005, 006 y 007"
archivos_modificados: "handbook/01-sdaf-framework.md y _meta/01 (0.3.0); handbook/index.yaml; handbook/README.md; AGENTS.md.template (0.5.0); docs/iniciativas/INIT-arquitectura.md (plan 0.1.13); docs/iniciativas/README.md; este worklog."
origen_cambios: "handbook/01, handbook/README y AGENTS.md.template: redacción de un subagente escritor delegado, revisada por el orquestador."
resultado: "H01 §3 y §3.2 adoptan la precedencia única de ADR-007 §2 (spec y ADR al mismo nivel por materia, conflicto = STOP, packs subordinados); H01 §4 hace opcional Calculation Rules y añade el eslabón de arquitectura; el README del handbook y AGENTS.md.template dicen lo mismo."
tiempo: PT6M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "Cambio de significado en un capítulo Approved: H01 sube a 0.3.0 (la entrada del CHANGELOG llega en la release, S6). H05 §2 no se toca: su orden spec antes que ADR es temporal y H01 §3 lo aclara; ninguna otra lista de prioridad del repo contradice la regla nueva (revisadas: H02, H09, docs/integracion-gentle-ai, prompts/system/master-architect). Los diagramas mermaid se revisaron a ojo; no se ejecutó un parser de mermaid, así que el render lo comprueba mkdocs build --strict en CI. Calculation Rules pasa a opcional en lugar de desaparecer, para no romper consumidores cuyo dominio sí tiene reglas derivadas. Sin push ni PR salvo orden posterior."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (revisión, confirmación de commits locales; después publicar el PR de S4a)
commit: null
pr: null
rama: feat/linea-0.5.0-04a-precedencia-pipeline
sha: null
resumen_acumulado: "ad hoc — S4a / ARQ-3.7 y 3.8 en rama local; sin commit/PR/tag"
---

# INIT-arquitectura / Iteration-015

## Línea de decisión

- La precedencia se implementa tal cual ADR-007 §2 y la decisión D-3 (opción C): spec y ADR al mismo nivel por materia, conflicto = STOP y enmienda. No se crea una cuarta regla.
- El diagrama de H01 §3 se redefine como derivación de artefactos, no como orden de prioridad; el orden temporal de H05 §2 queda explícitamente fuera de la prioridad.
- AGENTS.md.template no tenía lista de prioridad: se añade una viñeta compacta en «Gobernanza» que remite a H01 §3.2 (cabecera 0.5.0).
- Trazabilidad ODD: ruta de redacción delegada (disparador de escritura: 2 o más ficheros no triviales); verificación repetida por el orquestador.

## Pruebas

`check-version-metadata.py`, `check-history-append-only.py`, `measure-handbook-scaffolding.py`, `check-adrs.py`, `test-adrs.py`, `validate-config.py`, `validate-examples.py`, `validate-worklog.py` (Iteration-001 a 015) y `check-local-links.py --strict-anchors --strict-orphans` (copia limpia). markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| handbook/01, handbook/README, AGENTS.md.template | IA | Subagente escritor; revisado |
| _meta/01, index.yaml | IA | Redacción |
