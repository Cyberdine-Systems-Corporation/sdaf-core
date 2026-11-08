---
pbi: INIT-arquitectura
iteracion: Iteration-033
fecha: 2026-11-07
inicio: 2026-11-07T10:31:20+01:00
fin: 2026-11-07T18:34:30+01:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano en la sesión: ejecutar ARQ-4.5 (unidades de código), quinto PBI del camino a v0.6.0, tras preguntar «Que decisiones hay que tomar para continuar con ARQ-4.5?» y responder «Si» al mapeo (2026-11-07)."
contexto: "ARQ-4.5 de INIT-arquitectura: stack.units en la config con su validación (PR A, #81), lectura de todas las unidades en sdaf_diff para Gate 0 y la comprobación de worklog (PR B, #82) y las skills sdaf-gate0 y sdaf-bootstrap, la documentación y el cierre (PR C)."
especificaciones_utilizadas: "architecture/decisions/ADR-007-modelo-de-capas-y-precedencia.md (§8); architecture/decisions/ADR-005-linea-base-arquitectonica.md; docs/iniciativas/INIT-arquitectura.md (ARQ-4.5); sdaf.config.schema.json y sdaf.config.schema.yaml; docs/materializacion.md; Iteration-032 como modelo de cierre"
archivos_leidos: "architecture/decisions/ADR-007-modelo-de-capas-y-precedencia.md; docs/iniciativas/INIT-arquitectura.md y README.md; sdaf.config.schema.json y sdaf.config.schema.yaml; scripts/validate-config.py, scripts/sdaf_diff.py, scripts/sdaf_packs.py, scripts/check-worklog-presence.py y scripts/check-gate0.py; skills/sdaf-gate0/SKILL.md y skills/sdaf-bootstrap/SKILL.md con su historial en git; skills/README.md; scripts/check-version-metadata.py; docs/adopcion-y-upgrade.md; docs/contrato-pack-stack.md; docs/materializacion.md; examples/README.md; .github/actions/validate-sdaf/README.md; configuracion/escenarios.md; worklog Iteration-032 como modelo"
archivos_modificados: "PR A (#81, merge 9fb75c6): sdaf.config.schema.json, sdaf.config.schema.yaml, scripts/validate-config.py, scripts/test-validate-config.py y 7 fixtures config-units-*.yaml en scripts/testdata/ (11 ficheros, +362/−5), más el arreglo 951e3df de sdaf.config.schema.yaml (+8/−10). PR B (#82, merge 83d8fc1): scripts/sdaf_diff.py, scripts/check-worklog-presence.py, scripts/check-gate0.py, scripts/test-diff.py (nuevo), scripts/test-worklog.py, scripts/test-gate0.py y .github/workflows/validate.yml (7 ficheros, +388/−15). PR C: skills/sdaf-gate0/SKILL.md, skills/sdaf-bootstrap/SKILL.md, skills/README.md, docs/adopcion-y-upgrade.md, docs/contrato-pack-stack.md, examples/README.md, .github/actions/validate-sdaf/README.md, docs/iniciativas/INIT-arquitectura.md (plan 0.1.32), docs/iniciativas/README.md y este worklog."
origen_cambios: "PR A y PR B: redacción de un subagente escritor delegado en cada uno, revisada y verificada por el orquestador. PR C: redacción de un subagente escritor delegado, revisada por el orquestador; ver cuerpo."
resultado: "ARQ-4.5 hecho en lo que depende del agente: #81 y #82 fusionados en main con stack.units en la config (schema y validador), load_units en sdaf_diff y su uso en check-worklog-presence y check-gate0; el PR C, en rama local, sube sdaf-gate0 a 0.4.1 y sdaf-bootstrap a 0.6.0, ambas en Draft, actualiza las docs que ARQ-4.5 resuelve, el plan 0.1.32 y este worklog. Las dos skills quedan pendientes de aprobación humana: el agente no las aprueba; la aprobación se registrará en un segundo commit por orden expresa del humano. Sin tag ni release: v0.6.0 es ARQ-4.8. Sigue sin existir la comprobación de los nombres de unidad contra la línea base (ARQ-6.2)."
tiempo: PT3H30M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "El inicio (2026-11-07T10:31:20+01:00) es aproximado: es la hora del commit 438760a, el primer instante registrado de la entrega; el mapeo, las siete decisiones del diseño y la redacción previa no se cronometraron. El fin es la hora de cierre de la redacción de este worklog. El tiempo es una estimación honesta de trabajo activo desde ese commit, sin cronometrar (PR A con su arreglo, PR B y PR C), y es menor o igual que la diferencia entre fin e inicio. Las decisiones del humano se tomaron el 2026-11-07 y la hora exacta no se registró. Este worklog se escribe antes de la aprobación de las skills y no afirma que estén aprobadas. Sin entrada de handbook/CHANGELOG.md hasta ARQ-4.8; sdaf.version no cambia. Este worklog no registra el resultado del CI del PR C."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (revisar el diff de las skills y, con orden expresa, el segundo commit con su aprobación; después confirmar el commit local y publicar el PR)
commit: null
pr: null
rama: feat/units-skills-docs
sha: null
resumen_acumulado: "ad hoc — ARQ-4.5 unidades de código: #81 y #82 fusionados; skills sdaf-gate0 0.4.1 y sdaf-bootstrap 0.6.0 en Draft, docs y plan 0.1.32 en rama local; sin PR C"
---

# INIT-arquitectura / Iteration-033

## Línea de decisión

- Decisiones del humano sobre el diseño (2026-11-07, respuestas una a una; la hora exacta no se registró), citadas literalmente:
    - 1, coexistencia de `stack.units` con el atajo: «Error si conviven (Recomendada)».
    - 2, nombre de la unidad: «Texto libre, único y sin espacios en los extremos (Recomendada)».
    - 3, rutas: «Relativas, sin '..'; tests opcional; solape = aviso (Recomendada)».
    - 4, comprobación de worklog: «Union de unidades y algun worklog (Recomendada)».
    - 5, lectura en los scripts: «load_units en sdaf_diff + lectura endurecida (Recomendada)».
    - 6, skills: «Ambas, en un PR aparte, y tu las apruebas (Recomendada)».
    - 7, versión: «Aceptarla en cualquier sdaf.version (Recomendada)».
- Decisiones del humano sobre el PR C (2026-11-07, respuestas una a una; la hora exacta no se registró), citadas literalmente:
    - 1, `sdaf-gate0`: «Patch, 0.4.1 (Recomendada)».
    - 2, `sdaf-bootstrap`: «Los tres pasos, minor 0.6.0 (Recomendada)» (los pasos 2, 5 y 6).
    - 3, paso 5 de `sdaf-bootstrap`: «Condicionado por version (Recomendada)»: con `sdaf.version` `0.6.0` o superior, `scripts/materialize.py`; con una anterior, a mano según la guía de adopción.
    - 4, aprobación: «En este PR, en un segundo commit (Recomendada)»: se suben las versiones en Draft, el humano revisa el diff y, con orden expresa, el agente transcribe la aprobación con fecha y hora en un segundo commit. El agente no declara Approved ninguna skill.
- Diseño: `stack.units` es una lista de objetos con `name`, `src` y, opcional, `tests` (ADR-007 §8). `src_path` y `tests_path` siguen siendo el atajo de una sola unidad, sin aviso de obsoleto y sin endurecerse (sería incompatible). Las reglas de nombre y de rutas valen solo para `units` y se aplican con cualquier `sdaf.version`. `sdaf_diff.load_units` lee las unidades y `load_product_prefixes` la usa, de modo que `check-worklog-presence` y `check-gate0` cubren todas las unidades. Una config con `stack.units` y un atajo es un error del validador.
- Entrega en tres PRs a `main`:
    - PR A (#81, merge `9fb75c6`): schema, catálogo, validador, test y 7 fixtures; 11 ficheros, +362/−5, más el arreglo `951e3df` (+8/−10).
    - PR B (#82, merge `83d8fc1`): `sdaf_diff.py`, los dos comprobadores, `test-diff.py` nuevo, `test-worklog.py`, `test-gate0.py` y un paso en `validate.yml`; 7 ficheros, +388/−15.
    - PR C (este): las dos skills, `skills/README.md`, las docs que ARQ-4.5 resuelve, el plan 0.1.32, el índice y este worklog.
- Hallazgo e incidente (PR A): el ejemplo de `stack.units` que se añadió al catálogo `sdaf.config.schema.yaml` llevaba vallas de código. El catálogo se incrusta en un bloque de código de `configuracion/schema.md`, así que esas vallas cerraban el bloque exterior y el resto del catálogo, con enlaces relativos a la raíz, pasaba a ser markdown: el job `docs-build` del #81 falló con 3 avisos de enlaces en `--strict`. Nadie había ejecutado `mkdocs build` antes de proponer el commit. Se reprodujo con el árbol del commit `438760a` (código de salida 1, las mismas 3 advertencias) y se arregló en `951e3df` con el ejemplo con sangría y sin vallas; la compilación estricta sobre una copia limpia terminó con código 0 y sin avisos, y el #81 se fusionó con el CI en verde. Lección: ejecutar `mkdocs build --strict` antes de proponer un commit que toque el catálogo o las docs; el catálogo no admite vallas propias.
- Decisiones menores por defecto, como propuesta del asistente no objetada por el humano y reabrible:
    - Lectura endurecida (PR B): una excepción controlada `ConfigUnreadable` en `load_units` cubre el YAML roto, la raíz o el `stack` que no son un mapa y `units` vacía o mal formada; los comprobadores la convierten en `FAIL` con salida 1 y sin traceback, y `check-gate0` imprime el motivo. Si la config declara `units` y el atajo, el lector usa `units` (el validador ya rechaza la mezcla). Una unidad sin `tests` no añade el prefijo `tests/` por defecto; el atajo sigue dando `src/` y `tests/`; sin config rigen los prefijos por defecto.
    - Del escritor del PR A: se tolera la barra final en una ruta; la coexistencia se detecta por la presencia de la clave; los nombres distinguen mayúsculas; una ruta inválida no entra en la comprobación de solape.
    - Del escritor del PR B: un `stack` o una raíz falsos que no son un mapa (lista vacía, texto vacío, cero) pasan de usar los valores por defecto a ser ilegibles; ninguna config actual lo ejerce y el validador ya las rechaza.
    - PR C: `handbook/CHANGELOG.md` no se toca (se escribe una vez en la release; su nota de limitación se cierra en ARQ-4.8); el catálogo `sdaf.config.schema.yaml` no se toca (se incrusta en mkdocs y no admite vallas propias); `skills/README.md` sube a 0.3.7 y muestra las dos skills en Draft; `configuracion/escenarios.md` no se modifica porque su escenario de rutas custom sigue siendo exacto; `examples/README.md` documenta `stack.units` pero no inventa un ejemplo, que llega con ARQ-4.6.
- Skills en Draft: `sdaf-gate0` pasa a 0.4.1 (el disparador admite las rutas de cualquier unidad de `stack.units` o, en su defecto, `src_path` y `tests_path`; el paso 10 registra `sdaf-gate0@0.4.1`; sin cambio de gates) y `sdaf-bootstrap` a 0.6.0 (paso 2 con `stack.units` o el atajo sin mezclarlos; paso 5 con `stack.packs`, el alias `stack.pack` obsoleto, `scripts/materialize.py` desde la línea 0.6.0 y a mano con una anterior; paso 6 sin código de producto en las rutas de código de la config sin Gate 0; cita `sdaf-bootstrap@0.6.0`). Ambas quedan con Estado Draft y Fecha igual a la fila más reciente de su historial, como exige `check-version-metadata.py`. Este worklog se escribe antes de la aprobación: no afirma que estén aprobadas. La aprobación se registrará en un segundo commit, por orden expresa del humano, con su fecha y hora. Con ello el paso 5 de `sdaf-bootstrap`, que quedó como seguimiento en Iteration-032, queda resuelto en esta versión.
- Límite, sin tocar: ARQ-6.2 comprueba los nombres de unidad contra la línea base (el validador no lo hace); el ejemplo con varias unidades (`examples/` 10) llega con ARQ-4.6; `handbook/CHANGELOG.md` y los capítulos del handbook, en ARQ-4.8; los defectos menores de `materialize.py` vistos en Iteration-032 siguen sin corregir. H-6 sigue abierto hasta ARQ-4.6.

## Pruebas

- PR A (#81): RED real con 45 casos fallando; GREEN con 0 fallos y 186 casos correctos; 9 mutaciones del escritor detectadas; comprobación diferencial del escritor sobre 33 ficheros sin diferencias. El orquestador repitió `test-validate-config` (0 fallos), `test-validate-pack`, `check-version-metadata` y `check-history-append-only`, y sondó a mano casos como `units` que no es lista, un elemento que no es objeto, un nombre numérico, una ruta con `..` o con letra de unidad, la barra invertida y `apps/api` frente a `apps/api2`, todo sin trazas; la comparación contra `HEAD` en 5 configs dio resultados iguales. Después del merge se detectó el fallo de `docs-build` descrito arriba.
- PR B (#82): RED real (`test-diff` por ImportError, 8 casos de worklog y 7 de Gate 0); GREEN con 0 fallos; 13 mutaciones del escritor detectadas. Diferencial del escritor: 34 configs, 420 ejecuciones y 18 diferencias, todas el mensaje intencionado de una config ilegible (raíz que es una lista y YAML roto). El orquestador repitió `test-diff` (92 casos), `test-worklog` (23), `test-gate0` (66) y `test-docs` (47), y sondó de extremo a extremo con `--cwd` dos unidades con barra invertida final, el atajo frente al código anterior, `apps/api2` y `libs/core2` sin coincidencia, `src/` fuera de `units` sin producto y un YAML roto con `FAIL` limpio y salida 1. Un `.md` no se tocó en ese PR, así que no hizo falta `mkdocs build`.
- PR C (solo documentación y contrato de skills, sin RED/GREEN: no hay cambio de comportamiento ni de scripts): comprobaciones de los checks del repo sobre el árbol de trabajo: `check-version-metadata.py` (69 ficheros; las dos skills en Draft con la fecha de cabecera igual a la fila más reciente de su historial), `check-history-append-only.py` (69 artefactos), `check-adrs.py` (9 ADRs), `test-adrs.py`, `test-dates.py`, `validate-worklog.py` (Iteration-033 y, con `--plantilla`, la plantilla), `check-worklog-presence.py`, `measure-handbook-scaffolding.py` (andamiaje extraído, 18 capítulos), `validate-config.py` y `validate-examples.py`, todos con código de salida 0; y, sobre copia limpia fuera del repo, `check-local-links.py --strict-anchors --strict-orphans` (143 ficheros markdown, anclas internas correctas, sin huérfanos) y `mkdocs build --strict` con código de salida 0 y sin avisos de documentación (solo el aviso informativo de la propia herramienta sobre su próxima versión mayor). No se ejecutaron los tests de scripts: este PR no los toca.
- La búsqueda de abstracción sobre el diff del PR C no encuentra nombres de stack, producto, herramienta ni de ningún consumidor en lo añadido.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| sdaf.config.schema.json, sdaf.config.schema.yaml, scripts/validate-config.py, scripts/test-validate-config.py, scripts/testdata/config-units-*.yaml | IA, redacción revisada | Subagente escritor (PR A, #81); el arreglo `951e3df` del catálogo es del orquestador |
| scripts/sdaf_diff.py, scripts/check-worklog-presence.py, scripts/check-gate0.py, scripts/test-diff.py, scripts/test-worklog.py, scripts/test-gate0.py, .github/workflows/validate.yml | IA, redacción revisada | Subagente escritor (PR B, #82) |
| skills/sdaf-gate0/SKILL.md, skills/sdaf-bootstrap/SKILL.md | IA, redacción revisada | Subagente escritor; versiones nuevas en Draft, pendientes de aprobación humana |
| skills/README.md, docs/adopcion-y-upgrade.md, docs/contrato-pack-stack.md, examples/README.md, .github/actions/validate-sdaf/README.md | IA, redacción revisada | Subagente escritor; catálogo de skills y docs que ARQ-4.5 resuelve |
| docs/iniciativas/INIT-arquitectura.md, docs/iniciativas/README.md | IA, redacción revisada | Subagente escritor; plan 0.1.32 e índice |
