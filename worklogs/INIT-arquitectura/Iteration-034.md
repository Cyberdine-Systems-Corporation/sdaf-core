---
pbi: INIT-arquitectura
iteracion: Iteration-034
fecha: 2026-11-08
inicio: 2026-11-08T18:44:53+01:00
fin: 2026-11-08T19:31:57+01:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano en la sesión: «Continua con el siguiente paso» (2026-11-08, tras cerrar ARQ-4.5), que lleva a ARQ-6.2, sexto PBI del camino a v0.6.0."
contexto: "ARQ-6.2 de INIT-arquitectura: scripts/check-architecture.py (coherencia entre la línea base, los ADRs, stack.units y las specs) e input check-architecture en la action validate-sdaf. Entrega en tres PRs: A refactor de módulos compartidos (#84), B el script con su test (#85) y C la action, las docs y el cierre."
especificaciones_utilizadas: "architecture/decisions/ADR-006-ciclo-de-vida-de-adrs.md (§4, vigencia); architecture/decisions/ADR-005-linea-base-arquitectonica.md; handbook/14-architecture-description.md (§3 fila 6 y §6); docs/iniciativas/INIT-arquitectura.md (ARQ-6.2); .github/actions/validate-sdaf/README.md y action.yml (patrón de check-adrs y check-gate0); Iteration-033 como modelo de cierre"
archivos_leidos: "docs/iniciativas/INIT-arquitectura.md y README.md; scripts/check-gate0.py, scripts/sdaf_adrs.py, scripts/sdaf_docs.py, scripts/sdaf_diff.py y scripts/check-adrs.py; scripts/test-gate0.py, scripts/test-adrs.py y scripts/test-docs.py; scripts/check-architecture.py y scripts/test-architecture.py; scripts/testdata/gate0-valido, adrs-ciclo-valido, adrs-consumidor-heredado y architecture-valido; .github/actions/validate-sdaf/action.yml y README.md; .github/workflows/validate.yml; docs/adopcion-y-upgrade.md; architecture/decisions/ADR-006-ciclo-de-vida-de-adrs.md; templates/worklog.md; worklog Iteration-033 como modelo"
archivos_modificados: "PR A (#84, merge cda0d5f): scripts/sdaf_adrs.py, scripts/sdaf_docs.py, scripts/check-gate0.py, scripts/test-adrs.py y scripts/test-docs.py (5 ficheros, +315/−21). PR B (#85, merge 3d61dc7): scripts/check-architecture.py, scripts/test-architecture.py, 8 ficheros de scripts/testdata/architecture-valido/ y .github/workflows/validate.yml (11 ficheros, +792, con size:exception). PR C: .github/actions/validate-sdaf/action.yml y README.md, docs/adopcion-y-upgrade.md, docs/iniciativas/INIT-arquitectura.md (plan 0.1.34), docs/iniciativas/README.md y este worklog."
origen_cambios: "PR A y PR B: redacción de un subagente escritor delegado en cada uno, revisada y verificada por el orquestador. PR C: redacción de un subagente escritor delegado, revisada por el orquestador; ver cuerpo."
resultado: "ARQ-6.2 hecho en lo que depende del agente: #84 y #85 fusionados en main con scripts/check-architecture.py (FAIL por incoherencia grave, AVISO por desfase; sin línea base Approved o con sdaf.version anterior a 0.5.0 avisa y sale 0); el PR C, en rama local, añade el input opt-in check-architecture a la action validate-sdaf (default false, bloqueante al activarse, tras check-adrs y antes de check-gate0), su README, la guía de adopción, el plan 0.1.34 y este worklog. Sin tag ni release: v0.6.0 es ARQ-4.8."
tiempo: PT40M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "El inicio (2026-11-08T18:44:53+01:00) es aproximado: es la hora del commit bb6b41a, el primer instante registrado de la entrega; el mapeo, las seis decisiones del diseño y la redacción previa no se cronometraron. El fin es la hora de cierre de la redacción de este worklog. El tiempo es una estimación honesta de trabajo activo desde ese commit, sin cronometrar (PR A, PR B y PR C), y es menor o igual que la diferencia entre fin e inicio. Las decisiones del humano se tomaron el 2026-11-08 y la hora exacta no se registró. Sin entrada de handbook/CHANGELOG.md hasta ARQ-4.8; sdaf.version no cambia. Este worklog no registra el resultado del CI del PR C."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (confirmar el commit, el push y el PR C; después revisar y fusionar)
commit: null
pr: null
rama: feat/check-architecture-action
sha: null
resumen_acumulado: "ad hoc — ARQ-6.2 coherencia arquitectónica: #84 y #85 fusionados; input check-architecture de la action, docs y plan 0.1.34 en rama local; sin PR C"
---

# INIT-arquitectura / Iteration-034

## Línea de decisión

- Decisiones del humano sobre el diseño (2026-11-08, respuestas una a una; la hora exacta no se registró), citadas literalmente:
    - 1, gravedad: «FAIL por incoherencia grave, aviso por desfase (Recomendada)».
    - 2, vigencia de un ADR: «ADR-006 literal, leyendo los ADRs, con estados heredados (Recomendada)».
    - 3, cuando no se puede comprobar: «Aviso y salir 0, sin duplicar G0.6 (Recomendada)».
    - 4, specs: «Todas las specs; sin campo Unidades = aviso (Recomendada)».
    - 5, action: «Input check-architecture, opt-in, tras check-adrs (Recomendada)».
    - 6, lógica compartida: «Mover a los modulos compartidos, sin cambiar gate0 (Recomendada)».
- Diseño: es `FAIL` una unidad de `stack.units` o de una spec que no figura en la línea base, y un ADR sustituido listado en la sección 6 de la línea base («Decisiones vigentes»); es `AVISO` un ADR vigente que falta en esa sección. «Vigente» es ADR-006 §4: estado Aceptado (o su equivalente heredado) y sin «Sustituido por», leído de los ficheros ADR y no del índice. Una línea base ausente, ilegible o en Draft, o una `sdaf.version` anterior a `0.5.0`, es `AVISO` con salida 0 sin comprobar nada. Se comprueban todas las specs bajo `specs/`; los placeholders se ignoran. El input de la action es opt-in (default `"false"`), con el mismo patrón que `check-adrs` y `check-gate0` (`if: inputs.check-architecture == 'true'`, valores por `env:`), sin flags ni inputs nuevos.
- Entrega en tres PRs a `main`:
    - PR A (#84, merge `cda0d5f`): `adr_index` pasa de `check-gate0.py` a `sdaf_adrs.py`, con la función de vigencia de ADRs; el lector de la sección 6 de la línea base y el recorrido del campo `Unidades` de las specs, a `sdaf_docs.py`; `check-gate0.py` los importa sin cambiar salida ni códigos de salida; pruebas nuevas en `test-adrs.py` y `test-docs.py`; 5 ficheros, +315/−21.
    - PR B (#85, merge `3d61dc7`): `scripts/check-architecture.py`, `scripts/test-architecture.py` (67 casos), el fixture `scripts/testdata/architecture-valido/` (8 ficheros) y un paso en `validate.yml` para su test; 11 ficheros, +792, con `size:exception` declarada.
    - PR C (este): el input `check-architecture` en `action.yml` (paso entre `check-adrs` y `check-gate0`), su README, una sección en la guía de adopción, el plan 0.1.34, el índice y este worklog.
- Decisiones menores por defecto, como propuesta del asistente no objetada por el humano y reabrible:
    - Una `sdaf.config.yaml` ilegible es `FAIL`, como en `check-gate0`; un ADR listado en la sección 6 que no existe es `FAIL`; un ADR listado que existe, no está sustituido pero tampoco es vigente (Propuesto, Rechazado, Deprecado) es `AVISO`; la sección 6 ausente es `AVISO`; con el atajo `src_path`/`tests_path` no hay nombres de unidad que cotejar. Un fichero que no es UTF-8 sigue siendo `FAIL` por documento.
    - `check-architecture.py` no se ejecuta sobre el propio core en `validate.yml` (el core no tiene línea base ni specs): solo su test.
    - La vigencia (`adr_vigencia`) no evalúa `Caducidad`: una Excepción vencida con Estado Aceptado sigue vigente, porque ADR-006 §4 solo exige Aceptado y sin «Sustituido por». Un «Sustituido por» sin ADR legible (p. ej. TBD) cuenta como sin sustituto; `check-adrs` ya lo marca.
    - La sección 6 sin tabla ni `N/A` cuenta como sin ADRs listados; un ADR Aceptado con «Sustituido por» no es vigente y, si está listado, es `FAIL` por sustituido.
    - `check_line` (el corte por `sdaf.version`) se copió de `check-gate0.py` porque el guion del nombre del fichero impide importarlo.
    - PR C: el catálogo `sdaf.config.schema.yaml`, las skills, las plantillas y el handbook no se tocan; el ejemplo de uso del README de la action lleva un marcador en lugar de un tag, porque ningún tag publicado incluye el input.
- Revisión del orquestador (PR A y PR B), resumida: se leyó el diff completo de cada uno y se repitieron las suites. En el PR A, comprobación diferencial de `check-gate0.py` con 74 casos y 0 diferencias, y sondas propias de la vigencia sobre el fixture de ciclo de ADRs y de la lectura de la sección 6 y de las unidades de las specs sobre el de Gate 0. En el PR B, sondas propias sobre una copia del fixture: un ADR sustituido listado es `FAIL`; uno vigente omitido, `AVISO`; una unidad inexistente en la config o en una spec, `FAIL`; una línea base Draft o una `sdaf.version` `0.4.0`, `AVISO` con salida 0; una config rota, `FAIL` con salida 1; el atajo con `0.6.0`, sin cotejo; y sin `--root` sobre el propio core, `AVISO` con salida 0.
- Qué no hace: no se ejecuta sobre el propio core; no cambia ninguna skill, capítulo del handbook ni plantilla; no evalúa fechas de caducidad; no aprueba nada ni sustituye la revisión de la persona responsable.
- Límites, sin tocar: el ejemplo con varias unidades (`examples/` 10) llega con ARQ-4.6, que cierra H-6; `handbook/CHANGELOG.md` y los capítulos del handbook, en ARQ-4.8; los defectos menores de `materialize.py` vistos en Iteration-032 siguen sin corregir. El input solo estará disponible desde la línea 0.6.0, que no está publicada.

## Pruebas

- PR A (#84): RED real (`AttributeError` tras 47 y 40 casos correctos); GREEN con `test-docs` 61, `test-adrs` 56 y `test-gate0` 66 sin tocar casos previos, `test-diff` 92 y `test-worklog` 23; 10 mutaciones del escritor detectadas (una vacua, rehecha). Diferencial del escritor: 74 casos, 0 diferencias. El orquestador repitió las cinco suites, `check-adrs`, `check-version-metadata` y `check-history-append-only` con resultado correcto.
- PR B (#85): RED real (65 casos fallando con el script ausente); GREEN con `test-architecture` 67 casos; 18 mutaciones del escritor detectadas (2 supervivientes corregidas con casos nuevos y 1 vacua rehecha). El orquestador repitió `test-architecture`, `test-gate0`, `test-adrs`, `test-docs`, `test-diff` y `test-worklog`, además de `check-adrs`, `check-version-metadata` y `check-history-append-only`, todo correcto, y sondó a mano los casos descritos arriba.
- PR C (contrato público de la action y documentación, sin RED/GREEN: no hay cambio de scripts ni de tests): comprobaciones de los checks del repo sobre el árbol de trabajo: `check-version-metadata.py` (69 ficheros), `check-history-append-only.py` (69 artefactos), `check-adrs.py` (9 ADRs), `test-adrs.py`, `test-dates.py`, `validate-worklog.py` (Iteration-034 y, con `--plantilla`, la plantilla), `check-worklog-presence.py`, `measure-handbook-scaffolding.py` (andamiaje extraído, 18 capítulos), `validate-config.py` y `validate-examples.py`, todos con código de salida 0; `action.yml` cargado con PyYAML (YAML válido, el paso «Coherencia arquitectónica» va entre «ADRs del consumidor» y «Gate 0», con `if: inputs.check-architecture == 'true'`, el valor por `env:` y el input con default `false`); el comando del paso ejecutado tal cual sobre una copia del fixture `architecture-valido` con salida 0 y cuatro líneas OK; y, sobre copia limpia fuera del repo, `check-local-links.py --strict-anchors --strict-orphans` (144 ficheros markdown, anclas internas correctas, sin huérfanos) y `mkdocs build --strict` con código de salida 0 y sin avisos de documentación (solo el aviso informativo de la propia herramienta sobre su próxima versión mayor). No se ejecutaron los tests de scripts de los PRs A y B en este PR: no los toca.
- La búsqueda de abstracción sobre el diff del PR C no encuentra nombres de estilo, notación, stack, herramienta ni de ningún consumidor en lo añadido.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| scripts/sdaf_adrs.py, scripts/sdaf_docs.py, scripts/check-gate0.py, scripts/test-adrs.py, scripts/test-docs.py | IA, redacción revisada | Subagente escritor (PR A, #84) |
| scripts/check-architecture.py, scripts/test-architecture.py, scripts/testdata/architecture-valido/, .github/workflows/validate.yml | IA, redacción revisada | Subagente escritor (PR B, #85) |
| .github/actions/validate-sdaf/action.yml, .github/actions/validate-sdaf/README.md, docs/adopcion-y-upgrade.md | IA, redacción revisada | Subagente escritor; input opt-in y guía |
| docs/iniciativas/INIT-arquitectura.md, docs/iniciativas/README.md | IA, redacción revisada | Subagente escritor; plan 0.1.34 e índice |
