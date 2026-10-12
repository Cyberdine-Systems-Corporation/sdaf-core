---
pbi: INIT-arquitectura
iteracion: Iteration-020
fecha: 2026-10-12
inicio: 2026-10-12T18:58:00+02:00
fin: 2026-10-12T19:17:00+02:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano: «#45 fusionado. el humano indica el repo del piloto»; autorización: rama local en ese repo, sin push ni red. Después: incorporar los hallazgos del piloto con un PR extra al tracker."
contexto: "Piloto de la línea 0.5.0 sobre un consumidor real (overlay de adopción con el core y un pack como submódulos), exigido por INIT-arquitectura §8 antes del tag, y corrección de los hallazgos genéricos."
especificaciones_utilizadas: "docs/iniciativas/INIT-arquitectura.md (§8 Validación, ARQ-3.13, ARQ-6.3); docs/adopcion-y-upgrade.md (sección 0.5.0); handbook/14-architecture-description.md §9; skills/sdaf-upgrade"
archivos_leidos: "Del consumidor (solo lectura y rama local sin publicar): configuración, ADRs, AGENTS.md, scripts de materialización y workflow de validación. Del core: guía de adopción, sdaf-upgrade, check-adrs.py, validate-config.py"
archivos_modificados: "docs/adopcion-y-upgrade.md (pasos sobre AGENTS.md y aviso sobre check-adrs.py); skills/sdaf-upgrade/SKILL.md (0.3.1); handbook/CHANGELOG.md; docs/iniciativas/INIT-arquitectura.md (plan 0.1.18, backlog de ARQ-6.3); docs/iniciativas/README.md; este worklog."
origen_cambios: N/A
resultado: "Piloto sin bloqueos. En una rama local del consumidor: submódulo del core en el tracker, sdaf.version 0.5.0, línea base en Draft construida desde sus ocho ADRs, AGENTS.md con la precedencia única. Validan la configuración (estricta) y los quince worklogs con frontmatter. Tres hallazgos genéricos incorporados al core."
tiempo: PT19M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "Evidencia externa: el piloto no se cita como norma en el core y sus resultados entran como cambios genéricos (INIT §8). Resultados: (1) el submódulo se actualiza con un fetch local y los enlaces simbólicos materializados resuelven solos a las versiones nuevas, sin volver a materializar; (2) validate-config.py con strict-i4 y consumer-root valida sdaf.version 0.5.0; (3) los worklogs con frontmatter pasan; (4) la línea base se construye desde los ADRs siguiendo H14 §9: siete unidades y sus reglas de dependencia salen de un ADR de layout, y lo que ningún ADR establece (actores, atributos de calidad, specs de integración) queda como N/A; (5) con la línea base en Draft, G0.6 hace STOP, que es el comportamiento previsto hasta la aprobación humana. Hallazgos: A) la guía y sdaf-upgrade decían «regenerar AGENTS.md», ambiguo para un AGENTS.md personalizado con su propio historial: ahora dicen incorporar los cambios conservando lo propio; B) check-adrs.py, pensado para los ADRs del core, falla sobre los de un consumidor con formato anterior (fechas sin hora y zona, un hueco en la numeración, índice con el estado en la tercera columna): se avisa en la guía; C) ARQ-6.3 recoge el modo consumidor. Ninguno bloquea 0.5.0, porque la validación de ADRs del consumidor no forma parte de la línea. La rama del consumidor queda sin commit, local y sin publicar; la descarta o la conserva el humano. Sin push ni PR salvo orden posterior."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (revisión y confirmación de commits locales; decidir qué hacer con la rama del piloto; después fusionar #37 y crear el tag v0.5.0)
commit: null
pr: null
rama: feat/linea-0.5.0-07-hallazgos-piloto
sha: null
resumen_acumulado: "ad hoc — piloto de 0.5.0 sin bloqueos y hallazgos al core en rama local; sin PR/tag"
---

# INIT-arquitectura / Iteration-020

## Línea de decisión

- Alcance autorizado por el humano: rama local en el repo del piloto, sin push ni red; el submódulo del core se actualizó con un fetch desde el clon local. No se hizo commit en el repo del piloto.
- Los hallazgos entran al core como cambios genéricos y sin nombrar al consumidor ([INIT §8](../../docs/iniciativas/INIT-arquitectura.md)).
- El modo consumidor de `check-adrs.py` queda en el backlog de ARQ-6.3 (posterior a `0.5.0`): la validación de ADRs del consumidor no forma parte de la línea.

## Pruebas

`check-version-metadata.py`, `check-history-append-only.py`, `check-adrs.py`, `validate-worklog.py` (Iteration-001 a 020) y `check-local-links.py --strict-anchors --strict-orphans` (copia limpia). markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| docs/adopcion-y-upgrade.md, skills/sdaf-upgrade, CHANGELOG, plan | IA | Redacción; hallazgos del piloto |
