---
pbi: INIT-arquitectura
iteracion: Iteration-022
fecha: 2026-10-13
inicio: 2026-10-13T15:30:00+02:00
fin: 2026-10-18T18:42:00+02:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: "sdaf-adopt-existing@0.1.0 (solo en el recorrido sintético de aceptación)"
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano: ejecutar v0.5.1 (bloque 5, ARQ-5.1 a 5.3) con entrega en un PR de 4 commits (decisión I, 2026-10-13)."
contexto: "Parche de línea v0.5.1: adopción sobre código existente (ADR-008 Aceptado) como excepción de adopción, specs de caracterización con ADRs de reconocimiento y skill sdaf-adopt-existing."
especificaciones_utilizadas: "ADR-008; handbook/05 §3 y §8; handbook/13 §3; handbook/04 §4; handbook/14; docs/iniciativas/INIT-arquitectura.md (bloque 5)"
archivos_leidos: "ADR-008; handbook/04, 05, 10, 13 y 14 con sus sidecars; handbook/index.yaml; templates/spec.md, adr.md, architecture-description.md y worklog.md; skills/README.md y skills/sdaf-gate0; AGENTS.md.template; docs/adopcion-y-upgrade.md; scripts/check-adrs.py, check-worklog-presence.py y validate-worklog.py; plan de la iniciativa"
archivos_modificados: "handbook/04, 05, 10 y 13 (con sus handbook/_meta/*.yaml) y handbook/index.yaml; templates/spec.md, adr.md y architecture-description.md; skills/sdaf-adopt-existing/SKILL.md (nuevo) y skills/README.md; AGENTS.md.template; mkdocs/mkdocs.yml; docs/adopcion-y-upgrade.md; docs/iniciativas/INIT-arquitectura.md (plan 0.1.20); docs/iniciativas/README.md; este worklog."
origen_cambios: "Capítulos, plantillas, skill, guía y plan: redacción de subagentes escritores delegados, revisada por el orquestador; ver cuerpo."
resultado: "Contenido de v0.5.1 listo en rama local, pendiente de revisión y de publicación: ARQ-5.1 (7fb4665), ARQ-5.2 (b098f51) y ARQ-5.3 (9e3b984), y este cuarto commit con worklog y plan. Todo queda en Draft o Propuesto."
tiempo: PT1H30M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "El inicio (15:30) es aproximado. El tiempo es una estimación de trabajo activo, no la diferencia entre fin e inicio: hubo una pausa entre días (los commits 1 y 2 son del 2026-10-13 y el 3, del 2026-10-18). Hallazgo principal del recorrido sintético: la skill predecía mal Gate 0 y se corrigió. Recorrido con repo ficticio de tres unidades en el directorio temporal de la sesión; no se cita ningún consumidor real. Fuera de alcance por defecto (recomendación del asistente, no objetada por el humano; reabrible, para un parche posterior): H06 §6, sdaf-gate0, H08 §5 y sdaf-bootstrap, que no listan la skill ni conocen los perímetros. Sin push ni PR salvo orden posterior."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (revisar; push y PR solo con orden; después preparación de la release)
commit: null
pr: null
rama: docs/adopcion-v0.5.1
sha: null
resumen_acumulado: "ad hoc — v0.5.1 / ARQ-5.1 a 5.3 en rama local, pendiente de revisión; sin PR/tag"
---

# INIT-arquitectura / Iteration-022

## Línea de decisión

- Entrega en un solo PR a `main` con cuatro commits, sin rama tracker (decisión I, 2026-10-13): el parche es una línea corta y no tiene dependencias entre slices.
- La excepción de adopción es un ADR con `Tipo | Excepción` ([H13 §3](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md)), sin tipo nuevo: `check-adrs.py` solo admite ese valor. El subtipo se declara en Alcance y cuerpo.
- «Origen» ([H04 §4](../../handbook/04-specification-standard.md)) es una lista cerrada con `caracterización`; la ausencia de valor es una spec de PBI nuevo. La marca «heredada» es una nota de la plantilla de línea base, no una columna.
- Bumps: H05 0.6.0, H13 0.5.0, H04 0.4.0, H10 0.5.1 (nota de línea opt-in, sin cambio de norma), `AGENTS.md.template` 0.5.1, `skills/README.md` 0.3.5 y skill nueva 0.1.0 en Draft. Las plantillas no suben de versión (precedente).
- Fuera de alcance por defecto (recomendación del asistente, no objetada por el humano; reabrible): H06 §6, `sdaf-gate0`, H08 §5 y `sdaf-bootstrap`, para un parche posterior.
- Todo queda en Draft o Propuesto: ningún agente acepta ADRs ni aprueba capítulos o skills ([H00 §3.3](../../handbook/00-preface.md)).

### Recorrido de aceptación en repo sintético

- Repo ficticio de tres unidades de código con código previo, creado en el directorio temporal de la sesión.
- `check-adrs.py --root` OK sobre tres ADRs sintéticos (índice incluido), `validate-worklog.py` OK y `check-worklog-presence.py` OK, pero este último no ve el código heredado fuera de `stack.src_path`: limitación de tooling que resuelven las unidades de código de v0.6.0 (documentada en la skill).
- Hallazgo principal: la skill predecía mal Gate 0. El STOP real es G0.1, G0.2, G0.4 y G0.6; G0.3 solo si el PBI toca límites; y aceptar el ADR de excepción no desbloquea el perímetro gobernado. Corregido.
- Otras 11 fricciones menores, corregidas: formato de la caducidad propuesta, índice de ADRs, nombres y orden de ADRs, inventario en el worklog, reglas descriptivas, orden de las acciones humanas, bootstrap como precondición, tests de caracterización, registro de la skill una sola vez y la limitación de `check-worklog-presence.py`.

## Pruebas

`check-version-metadata.py` (69 ficheros), `check-history-append-only.py`, `check-adrs.py` (9 ADRs), `test-adrs.py`, `measure-handbook-scaffolding.py`, `validate-config.py`, `validate-examples.py`, `validate-worklog.py` (Iteration-001 a 022) y `check-local-links.py --strict-anchors --strict-orphans` sobre copia limpia (130 markdown). markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | Redacción IA revisada; sin ejecutable nuevo. |
