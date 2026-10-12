---
pbi: INIT-arquitectura
iteracion: Iteration-019
fecha: 2026-10-12
inicio: 2026-10-12T18:42:00+02:00
fin: 2026-10-12T18:51:00+02:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: chained-pr
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano: «#44 fusionado» (S5 integrada); continuar con S6. Decisiones del humano: ejemplos a sdaf.version \"0.5.0\" y piloto después de S6 y antes del tag."
contexto: "ARQ-3.13 de INIT-arquitectura (slice S6 de v0.5.0): preparación de la release de la línea 0.5.0."
especificaciones_utilizadas: "docs/iniciativas/INIT-arquitectura.md (ARQ-3.13, §4, §8); handbook/13-enmienda-excepciones-ciclo-de-vida.md §5 y §6; handbook/14-architecture-description.md §9; precedente de las releases 0.4.0 y 0.4.1 a 0.4.3 (commits 93c17ca, 581d4ee, 1548074, 29568ec)"
archivos_leidos: "handbook/CHANGELOG.md; CHANGELOG.md; README.md; docs/adopcion-y-upgrade.md; skills/sdaf-upgrade/SKILL.md; sdaf.config.example.yaml; examples/; handbook/index.yaml; scripts/extract-handbook-meta.py; scripts/validate-config.py; versiones finales en handbook/_meta"
archivos_modificados: "handbook/CHANGELOG.md (entrada 0.5.0); CHANGELOG.md; README.md; docs/adopcion-y-upgrade.md; docs/README.md; skills/sdaf-upgrade/SKILL.md (0.3.0); sdaf.config.example.yaml; examples/01 a 08 y examples/README.md; sdaf.config.schema.yaml; handbook/index.yaml; scripts/extract-handbook-meta.py; docs/iniciativas/INIT-arquitectura.md (plan 0.1.17); docs/iniciativas/README.md; este worklog."
origen_cambios: "CHANGELOG, README, guía de adopción, sdaf-upgrade, ejemplos e índice: redacción de un subagente escritor delegado, revisada por el orquestador."
resultado: "Release 0.5.0 preparada: entrada del CHANGELOG del handbook con las versiones finales, guía de migración con 11 pasos, sdaf-upgrade 0.3.0, ejemplos con sdaf.version \"0.5.0\", README con 00–14 y línea 0.5.0. El tag v0.5.0 y la publicación (badge, pin recomendado, README de la action) quedan para después del merge, por orden humana."
tiempo: PT9M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "Patrón de preparación del precedente 581d4ee: no cambian el badge, el pin recomendado (v0.4.3), la lista de tags publicados ni el README de la action; el chore de publicación tras el tag lo hace. El esquema de config no necesitó cambios: sdaf.version solo exige un semver y \"0.5.0\", \"0.4.0\" y \"0.3.0\" ya validan. El piloto sobre el overlay existente queda pendiente: es evidencia externa, se hace después de S6 y antes del tag, con repo y autorización que indicará el humano; no se cita ningún repo consumidor en el core. Entrada del CHANGELOG enlaza a este worklog (Iteration-019). Sin push ni PR salvo orden posterior."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (revisión, confirmación de commits locales; después publicar el PR de S6; piloto; fusionar #37 y tag v0.5.0)
commit: null
pr: null
rama: feat/linea-0.5.0-06-release
sha: null
resumen_acumulado: "ad hoc — S6 / ARQ-3.13 preparación de la release 0.5.0 en rama local; sin PR/tag"
---

# INIT-arquitectura / Iteration-019

## Línea de decisión

- Release de línea opt-in con cambio incompatible: `0.5.0` (H13 §5). No rompe citas `H00`–`H13` porque H14 se añade sin renumerar.
- Ejemplos y `sdaf.config.example.yaml` pasan a `"0.5.0"` (decisión del humano, 2026-10-12): muestran la línea vigente y el comentario recuerda `"0.4.0"` con pin `v0.4.x` y `"0.3.0"` con pin `v0.3.3`.
- La sección de migración parte de H14 §9: construir la línea base desde los ADRs vigentes y pedir su aprobación humana; sin ella, G0.6 hace STOP.
- Piloto: evidencia externa, después de S6 y antes del tag. No se toca ningún repo externo sin indicación y autorización expresa del humano.
- Trazabilidad ODD: mapeo previo delegado, redacción delegada y verificación repetida por el orquestador.

## Pruebas

`validate-config.py`, `test-validate-config.py`, `validate-examples.py`, `check-version-metadata.py`, `check-history-append-only.py`, `measure-handbook-scaffolding.py`, `check-adrs.py`, `test-adrs.py`, `validate-worklog.py` (Iteration-001 a 019) y `check-local-links.py --strict-anchors --strict-orphans` (copia limpia). markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| CHANGELOG, README, guía de adopción, sdaf-upgrade, ejemplos, índice | IA | Subagente escritor; revisado |
| docs/README.md, esquema de config, extract-handbook-meta.py | IA | Redacción |
