---
pbi: INIT-arquitectura
iteracion: Iteration-017
fecha: 2026-10-12
inicio: 2026-10-12T18:18:00+02:00
fin: 2026-10-12T18:26:00+02:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: chained-pr
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano: «Continúa con el siguiente paso» (S5 del plan); decisión del humano: registrar el idioma con ADR-009 más nota en el esquema; pedir confirmación antes de cada commit local."
contexto: "ARQ-3.11 y ARQ-3.12 de INIT-arquitectura (slice S5 de v0.5.0): bootstrap con línea base, enlaces a la línea base e idioma fijo con decisión citable."
especificaciones_utilizadas: "docs/iniciativas/INIT-arquitectura.md (ARQ-3.11, 3.12, D-8); architecture/decisions/ADR-005 §1 y §9; ADR-006; handbook/14-architecture-description.md; handbook/05-development-workflow.md §2 y §3"
archivos_leidos: "skills/sdaf-bootstrap/SKILL.md; templates/handbook-product.md; docs/mapa-navegacion.md; sdaf.config.schema.yaml y .json; examples/README.md; architecture/decisions/ADR-005 a 008 y README; mkdocs/mkdocs.yml; scripts de validación"
archivos_modificados: "skills/sdaf-bootstrap/SKILL.md (0.5.0); templates/handbook-product.md (0.1.1); docs/mapa-navegacion.md; architecture/decisions/ADR-009-idioma-de-artefactos.md (nuevo, Propuesto); architecture/decisions/README.md; mkdocs/mkdocs.yml; sdaf.config.schema.yaml y .json; examples/README.md; docs/iniciativas/INIT-arquitectura.md (plan 0.1.15); docs/iniciativas/README.md; este worklog."
origen_cambios: "skill, plantilla, ADR-009, esquema y ejemplos: redacción de un subagente escritor delegado, revisada por el orquestador."
resultado: "sdaf-bootstrap 0.5.0 crea la línea base en Draft (solo con sdaf.version 0.5.0 o superior) y añade specs/integration al árbol; el STOP de Gate 0 cita G0.1 y G0.6. El handbook de producto y el mapa de navegación enlazan la línea base. El idioma es queda registrado en ADR-009 (Propuesto) con nota en el esquema, el JSON y los ejemplos."
tiempo: PT8M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "ADR-009 queda Propuesto: lo acepta un humano (H00 §3.3), y el agente no escribe la fila Aceptación; mientras tanto la nota del esquema remite a un ADR aún no aceptado. La decisión D-8 del plan ya está cerrada, pero su registro citable es este ADR. La creación de architecture/description.md por el bootstrap depende de sdaf.version 0.5.0 o superior porque la línea base es opt-in. La plantilla del handbook de producto sube a 0.1.1 (una fila de enlace, sin cambio de obligación). Ningún capítulo del handbook cambia en este slice, así que no hay bump de capítulos Approved. Sin push ni PR salvo orden posterior."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (revisión, confirmación de commits locales; aceptación o rechazo de ADR-009; después publicar el PR de S5)
commit: null
pr: null
rama: feat/linea-0.5.0-05-bootstrap-idioma
sha: null
resumen_acumulado: "ad hoc — S5 / ARQ-3.11 y 3.12 en rama local; ADR-009 Propuesto; sin commit/PR/tag"
---

# INIT-arquitectura / Iteration-017

## Línea de decisión

- Idioma: de las tres opciones (nota en el esquema, ADR nuevo o enmienda de capítulos) el humano eligió ADR-009 más nota. Un ADR es citable por ruta estable y sustituible por el ciclo de ADR-006; una nota en el esquema no lo es, y una enmienda de H02 o H07 sería desproporcionada para una decisión que no cambia ninguna obligación.
- ADR-009 nace Propuesto: no hay fila Aceptación (`check-adrs.py` la rechaza en un Propuesto). El índice de ADRs y la navegación de mkdocs lo incluyen.
- El bootstrap no crea la línea base con `sdaf.version` `0.4.0`: la línea `0.5.0` es opt-in (ADR-005 §9, H05 §3).
- Trazabilidad ODD: mapeo previo delegado, redacción delegada (disparador de escritura) y verificación repetida por el orquestador.

## Pruebas

`check-adrs.py` (9 ADRs), `test-adrs.py`, `check-version-metadata.py`, `check-history-append-only.py`, `measure-handbook-scaffolding.py`, `validate-config.py`, `validate-examples.py`, `validate-worklog.py` (Iteration-001 a 017) y `check-local-links.py --strict-anchors --strict-orphans` (copia limpia). markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| skills/sdaf-bootstrap, templates/handbook-product.md, ADR-009, esquema y ejemplos | IA | Subagente escritor; revisado |
| mapa de navegación, índice de ADRs, mkdocs | IA | Redacción |
