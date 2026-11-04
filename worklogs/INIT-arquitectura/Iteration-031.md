---
pbi: INIT-arquitectura
iteracion: Iteration-031
fecha: 2026-11-04
inicio: 2026-11-04T23:24:56+01:00
fin: 2026-11-04T23:51:30+01:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano en la sesión: ejecutar ARQ-4.3 (overlay y resolución por id), tercer PBI del camino a v0.6.0, tras responder «Continua con el siguiente paso» una vez cerrado ARQ-4.2 (2026-11-04)."
contexto: "ARQ-4.3 de INIT-arquitectura: stack.overlay.replaces con la regla de ADR-007 §5 en el schema y el validador (PR #77) y la norma de capas y resolución por id en H01 §3.3 con el contrato de pack, AGENTS.md.template, glosario, plan y worklog (PR de cierre)."
especificaciones_utilizadas: "architecture/decisions/ADR-007-modelo-de-capas-y-precedencia.md (§1, §2, §5 y §7); architecture/decisions/ADR-004-tooling-externo-de-agentes.md; docs/iniciativas/INIT-arquitectura.md (ARQ-4.3); docs/contrato-pack-stack.md; handbook/01-sdaf-framework.md; Iteration-030 como modelo de cierre"
archivos_leidos: "architecture/decisions/ADR-007-modelo-de-capas-y-precedencia.md; handbook/01-sdaf-framework.md y su sidecar; handbook/B-glossary.md y su sidecar; handbook/index.yaml; AGENTS.md.template; docs/contrato-pack-stack.md; sdaf.config.schema.json y .yaml; scripts/validate-config.py y los fixtures config-overlay-*.yaml; examples/README.md; configuracion/escenarios.md; docs/iniciativas/INIT-arquitectura.md y README.md; worklog Iteration-030 como modelo"
archivos_modificados: "PR #77: sdaf.config.schema.json y .yaml, scripts/validate-config.py, scripts/test-validate-config.py y 9 fixtures scripts/testdata/config-overlay-*.yaml. PR de cierre: handbook/01-sdaf-framework.md y su sidecar (0.4.0), handbook/B-glossary.md y su sidecar (0.3.4), handbook/index.yaml, AGENTS.md.template (0.5.2), docs/contrato-pack-stack.md, examples/README.md, configuracion/escenarios.md, docs/iniciativas/INIT-arquitectura.md (plan 0.1.30), docs/iniciativas/README.md y este worklog."
origen_cambios: "Scripts, schema, fixtures y pruebas (#77): redacción de un subagente escritor delegado, revisada y verificada por el orquestador. Documentación (PR de cierre): redacción de un subagente escritor delegado, revisada por el orquestador; ver cuerpo."
resultado: "ARQ-4.3 hecho: #77 fusionado en main (merge 5f25280) con stack.overlay.replaces y la regla de ADR-007 §5 en el validador; el PR de cierre, en rama local, añade H01 0.4.0 §3.3 (capas y resolución por id), la sección «Resolución por id» del contrato de pack, AGENTS.md.template 0.5.2, el glosario 0.3.4, la desambiguación de «overlay» en examples/ y configuracion/, el plan 0.1.30 y este worklog. Sin tag ni release: v0.6.0 es ARQ-4.8. La colisión entre un pack y el overlay y la materialización siguen sin existir (ARQ-4.4)."
tiempo: PT20M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "El inicio (2026-11-04T23:24:56+01:00) es aproximado: es la hora del commit de #77 (e8967d2), el primer instante registrado de la entrega; el mapeo y el diseño previos no se cronometraron. El fin es la hora de cierre de la redacción de este worklog. El tiempo es una estimación honesta de trabajo activo desde ese commit, sin cronometrar, y es menor o igual que la diferencia entre fin e inicio. Las decisiones del humano se tomaron el 2026-11-04 y la hora exacta no se registró. Sin CHANGELOG ni entrada de handbook/CHANGELOG.md hasta ARQ-4.8; sdaf.version no cambia. Este worklog no registra el resultado del CI de ningún PR."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (confirmar el commit local; después publicar el PR)
commit: null
pr: null
rama: docs/capas-resolucion-por-id
sha: null
resumen_acumulado: "ad hoc — ARQ-4.3 overlay y resolución por id: #77 fusionado; docs de cierre (H01 0.4.0, contrato, AGENTS.md.template 0.5.2, glosario 0.3.4, plan 0.1.30) en rama local; sin PR de cierre"
---

# INIT-arquitectura / Iteration-031

## Línea de decisión

- Decisiones del humano (2026-11-04, respuestas una a una; la hora exacta no se registró), citadas literalmente:
    - D1, lugar de la norma: «H01 (norma) + contrato (mecanismo) (Recomendada)».
    - D2, declarar la sustitución: «stack.overlay.replaces, opcional (Recomendada)».
    - D3, alcance del validador: «Solo la regla central de §5 (Recomendada)».
    - D4, skills y prompts: «No: la colisión es siempre error (Recomendada)».
    - D5, reparto: «Primero schema y validador, luego docs (Recomendada)».
    - D6, `core: ">=X.Y.Z <=X.Y.Z"` como versión única: «Mantenerlo aceptado (Recomendada)». Cierra el visto bueno que quedaba pendiente desde ARQ-4.1.
- El resto se aplicó por defecto, como propuesta del asistente no objetada por el humano y reabrible: un «id de extensión» es cualquier id que no esté entre los ids del núcleo (como ya hace I4); `replaces` sin packs declarados no avisa; I4 no cambia.
- Diseño: `stack.overlay` es un objeto opcional sin otras claves, con `replaces` como lista de cadenas sin repetidos. `validate-config.py` rechaza un id del núcleo y un id que `agents.active`, `agents.stubs` o `agents.fusions` (claves y miembros) no declaran. La detección de la colisión entre un pack y el overlay no se implementa: en un consumidor los `agents/<id>-agent.md` suelen ser enlaces materializados y darían falsos positivos; queda para ARQ-4.4.
- Entrega en dos PRs a `main`:
    - #77 (schema y validador: `stack.overlay.replaces`, comprobación de ADR-007 §5, 22 casos de prueba y 9 fixtures; +294/−2; merge `5f25280`).
    - PR de cierre (este): norma en H01 0.4.0 §3.3, mecanismo en el contrato de pack, remisión en `AGENTS.md.template` 0.5.2, glosario 0.3.4, desambiguación de «overlay» en `examples/README.md` y `configuracion/escenarios.md`, plan 0.1.30 e índice.
- Bumps: H01 0.3.0 → 0.4.0 (cambio de significado: sección nueva §3.3, minor); `AGENTS.md.template` 0.5.1 → 0.5.2 (patch, sin cambio de norma); glosario 0.3.3 → 0.3.4 (patch: «Pack de stack» deja de definirse como overlay, entrada nueva «Overlay (consumidor)» y «Overlay (H12)» desambiguado); `handbook/index.yaml` acompaña las versiones de H01 y del glosario. El contrato de pack no lleva versión. Sin entrada en `handbook/CHANGELOG.md`: se escribe una sola vez con la release (ARQ-4.8).
- «Overlay» tenía tres sentidos en el repo: la capa del consumidor (ADR-007 §1), el control N/A de H12 y, heredado, el pack. Se corrigió el sentido heredado (pack) en el glosario, `examples/README.md` y `configuracion/escenarios.md`; el del diagrama de decisión de `examples/README.md` («¿Qué overlay?», que ofrece pack, fusiones y agentes desacoplados) pasa a «¿Qué variante?», porque no todas sus ramas son un pack.
- Límite, sin tocar: la colisión entre un pack y el overlay y la materialización (ARQ-4.4); el contraste de los `extension_ids` de un manifiesto con el catálogo de ids del core sigue sin existir; `stack.units` (4.5); `examples/` 09 y 10 (4.6); repo del pack de referencia (4.7); release y bumps de línea (4.8).
- Duda de ARQ-4.1 y ARQ-4.2 resuelta: `core: ">=X.Y.Z <=X.Y.Z"` (versión única) queda **aceptado** por el humano (D6).

## Pruebas

- #77: RED con 21 de 22 casos fallando; GREEN con 139 casos. Comprobación diferencial del commit base frente al nuevo: 50 casos del escritor y 56 del orquestador (ejemplos, ejemplo canónico y fixtures previos, con y sin `--strict-i4`), sin diferencias. 4 mutaciones del escritor detectadas.
- PR de cierre (solo documentación, sin RED/GREEN: no hay cambio de comportamiento; comprobaciones estructurales y de los checks del repo sobre el árbol de trabajo): `check-version-metadata.py` (cabeceras de H01 0.4.0, glosario 0.3.4 y `AGENTS.md.template` 0.5.2 coherentes con sus historiales; 69 ficheros), `check-history-append-only.py` (las filas previas no cambian), `check-adrs.py`, `test-adrs.py`, `test-dates.py`, `test-docs.py`, `test-gate0.py`, `test-worklog.py`, `test-validate-config.py` (0 fallos), `test-validate-pack.py` (0 fallos), `validate-pack.py` (plantilla), `validate-config.py`, `validate-examples.py` (solo los avisos de alias ya conocidos de los ejemplos 04, 05, 07 y 08), `measure-handbook-scaffolding.py` (andamiaje extraído, 18 capítulos), `validate-worklog.py` (Iteration-031) y `check-local-links.py --strict-anchors --strict-orphans` sobre copia limpia. Los mensajes que cita el contrato de pack se contrastaron ejecutando `validate-config.py` con los fixtures reales `config-overlay-nucleo.yaml` y `config-overlay-no-declarado.yaml`, y el ejemplo del contrato valida con `OK`. Búsqueda de abstracción sobre §3.3 de H01 y la sección del contrato: sin nombres de estilo, notación, stack ni producto. markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| sdaf.config.schema.json, sdaf.config.schema.yaml | IA, redacción revisada | Subagente escritor (#77) |
| scripts/validate-config.py, scripts/test-validate-config.py, scripts/testdata/ | IA, redacción revisada | Subagente escritor (#77) |
| handbook/01-sdaf-framework.md, handbook/_meta/01-sdaf-framework.yaml | IA, redacción revisada | Subagente escritor; §3.3 (0.4.0) |
| handbook/B-glossary.md, handbook/_meta/B-glossary.yaml, handbook/index.yaml | IA, redacción revisada | Subagente escritor; glosario 0.3.4 |
| AGENTS.md.template, docs/contrato-pack-stack.md | IA, redacción revisada | Subagente escritor; 0.5.2 y sección «Resolución por id» |
| examples/README.md, configuracion/escenarios.md | IA, redacción revisada | Subagente escritor; desambiguación de «overlay» |
| docs/iniciativas/INIT-arquitectura.md, docs/iniciativas/README.md | IA, redacción revisada | Subagente escritor; plan 0.1.30 e índice |
