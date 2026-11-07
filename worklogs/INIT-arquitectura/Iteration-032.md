---
pbi: INIT-arquitectura
iteracion: Iteration-032
fecha: 2026-11-06
inicio: 2026-11-06T23:50:00+01:00
fin: 2026-11-07T09:32:00+01:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano en la sesión: ejecutar ARQ-4.4 (materialización en el core), cuarto PBI del camino a v0.6.0, tras responder «Adelante con ARQ-4-4» (2026-11-06) una vez cerrado ARQ-4.3, y «Continua con el PR B de ARQ-4.4» (2026-11-07) para la documentación."
contexto: "ARQ-4.4 de INIT-arquitectura: script de materialización multiplataforma con su test y fixtures (PR A, #79) y su contrato y guía de uso, con la actualización de la guía de adopción y del contrato de pack (PR B)."
especificaciones_utilizadas: "architecture/decisions/ADR-007-modelo-de-capas-y-precedencia.md (§1, §5 y §7); handbook/01-sdaf-framework.md §3.3; docs/iniciativas/INIT-arquitectura.md (ARQ-4.4); docs/contrato-pack-stack.md; docs/adopcion-y-upgrade.md; Iteration-031 como modelo de cierre"
archivos_leidos: "architecture/decisions/ADR-007-modelo-de-capas-y-precedencia.md; handbook/01-sdaf-framework.md; docs/contrato-pack-stack.md; docs/adopcion-y-upgrade.md; docs/README.md; docs/mapa-navegacion.md; mkdocs/mkdocs.yml; scripts/materialize.py, scripts/test-materialize.py y scripts/testdata/materialize/; scripts/sdaf_packs.py; scripts/validate-config.py; docs/iniciativas/INIT-arquitectura.md y README.md; worklog Iteration-031 como modelo"
archivos_modificados: "PR A (#79, a8771c7): scripts/materialize.py, scripts/test-materialize.py, 18 fixtures en scripts/testdata/materialize/ y .github/workflows/validate.yml (+2 líneas). PR B: docs/materializacion.md (nuevo), docs/adopcion-y-upgrade.md, docs/contrato-pack-stack.md, docs/README.md, docs/mapa-navegacion.md, mkdocs/mkdocs.yml, docs/iniciativas/INIT-arquitectura.md (plan 0.1.31), docs/iniciativas/README.md y este worklog."
origen_cambios: "Script, test y fixtures (#79): redacción de un subagente escritor delegado, revisada y verificada por el orquestador. Documentación (PR B): redacción de un subagente escritor delegado, revisada por el orquestador; ver cuerpo."
resultado: "ARQ-4.4 hecho: #79 fusionado en main (merge a8771c7) con scripts/materialize.py, su test y los fixtures; el PR B, en rama local, añade docs/materializacion.md, actualiza la guía de adopción (que deja de remitir a un script de un consumidor) y el contrato de pack (ruta normada y «Qué no existe todavía»), la navegación, el plan 0.1.31 y este worklog. Sin tag ni release: v0.6.0 es ARQ-4.8. Siguen sin existir el contraste de los extension_ids de un manifiesto con el catálogo del core y un input de la action validate-sdaf para pasar manifiestos."
tiempo: PT30M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "El inicio (2026-11-06T23:50:00+01:00) es aproximado: es la hora del commit c1d91a5, el primer instante registrado de la entrega; el mapeo, el diseño y la redacción del script previos no se cronometraron. El fin es la hora de cierre de la redacción de este worklog. El tiempo es una estimación honesta de trabajo activo desde ese commit, sin cronometrar (la fusión de #79 y la documentación del PR B), y es menor o igual que la diferencia entre fin e inicio. Las decisiones del humano se tomaron el 2026-11-06 y la hora exacta no se registró. Sin CHANGELOG ni entrada de handbook/CHANGELOG.md hasta ARQ-4.8; sdaf.version no cambia. Este worklog no registra el resultado del CI de ningún PR."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (confirmar el commit local; después publicar el PR)
commit: null
pr: null
rama: docs/materializacion
sha: null
resumen_acumulado: "ad hoc — ARQ-4.4 materialización en el core: #79 fusionado; docs (docs/materializacion.md, guía de adopción, contrato de pack, plan 0.1.31) en rama local; sin PR B"
---

# INIT-arquitectura / Iteration-032

## Línea de decisión

- Decisiones del humano (2026-11-06, respuestas una a una; la hora exacta no se registró), citadas literalmente:
    - D1, ruta de los aportes de un pack: «Convención fija como en el core (Recomendada)».
    - D2, localizar el core y los packs: «Argumentos de CLI con defaults (Recomendada)».
    - D3, marca de origen de las copias: «Fichero lateral de registro (Recomendada)».
    - D4, qué se materializa: «Solo agents, prompts y skills (Recomendada)».
    - D5, dónde se detecta la colisión pack/overlay: «Solo en materialize.py (Recomendada)».
    - D6, re-ejecución: «Reemplaza solo lo propio y aborta ante conflicto (Recomendada)».
- Diseño: el orden es core, después los packs (el de `--pack`) y por último el overlay, que el script no crea: es lo que ya hay en el destino como fichero o directorio real. La convención de rutas es la misma en el core y en cada pack (`agents/<id>-agent.md`, `prompts/agents/<id>-agent.md`, `skills/<id>/SKILL.md`) y no cambia `sdaf-pack.schema.json`. El registro lateral `.sdaf-origin` guarda destino, capa, origen, tipo y sha256 de cada enlace o copia sin tocar el contenido copiado. Con `--mode auto` se prefiere el enlace simbólico relativo y se cae a copia; nunca se crean junctions. La colisión se detecta antes de escribir y solo en `materialize.py`: `validate-config.py` no cambia. La excepción del overlay (`stack.overlay.replaces`) cubre solo el contrato de agente de un id de extensión; el núcleo, las skills y los prompts son siempre error.
- Entrega en dos PRs a `main`:
    - #79 (script, test y fixtures: `materialize.py` 571 líneas, `test-materialize.py` 689 líneas con 45 casos, 18 fixtures y +2 líneas en `validate.yml`; +1307/−0; merge `a8771c7`, `size:exception` declarada en la descripción).
    - PR B (este): `docs/materializacion.md` (contrato y guía de uso), guía de adopción, contrato de pack, navegación (`docs/README.md`, `docs/mapa-navegacion.md`, `mkdocs/mkdocs.yml`), plan 0.1.31 e índice.
- Hallazgo de la revisión del PR A: un registro `.sdaf-origin` manipulado, con un destino como `skills/.`, pasaba la validación de convención y, si el hash coincidía, el script podía borrar el directorio `skills/` entero. Se cerró con un test previo en rojo y el arreglo (el registro rechaza destinos con partes vacías, `.` o `..`). El docstring pasó a decir «reglas de editor» en lugar de nombrar una ruta concreta.
- Decisiones menores por defecto, como propuesta del asistente no objetada por el humano y reabrible:
    - El handbook H01 no se toca ni sube de versión: añadir un enlace en §3.3 al documento nuevo no cambia su significado y evitaría una versión `0.5.0` sin cambio normativo; la cita al documento nuevo vive en el contrato de pack y en la guía.
    - El paso 5 de `skills/sdaf-bootstrap` queda como seguimiento: habla de `stack.pack` y de un script de un consumidor, y es una skill Approved; subir su versión y aprobarla es del humano.
    - Los enlaces simbólicos reales solo se ejercitaron en Linux; en Windows nativo, sin permiso para crearlos, el test usa copia y salta 4 casos.
- Decisión J cerrada (2026-11-06, respuestas del humano a cinco preguntas; hora no registrada): autorización sobre el repo del pack de referencia, rama `main`, solo las fases de lectura y de cambio local, con la sesión de `gh` ya autenticada, hasta la fusión del PR de ARQ-4.7 y con confirmación expresa antes de cada commit, push y PR. Publicar en ese repo (push y PR) y su release no están autorizados y piden una autorización nueva. En este PR solo se usó la lectura, para contrastar que ese repo ya usa la convención de rutas.
- Defectos menores de `materialize.py` vistos al documentar, sin corregir (no cambian el comportamiento): el mensaje de colisión de un prompt dice «en una prompt»; con un manifiesto inválido se repite la misma línea `FAIL` varias veces; y en los `FAIL` de un pack fuera del repo del core se imprime la ruta absoluta.
- Límite, sin tocar: el contraste de los `extension_ids` de un manifiesto con el catálogo de ids del core; un input de la action `validate-sdaf` para pasar manifiestos; `stack.units` (4.5); `examples/` 09 y 10 (4.6); repo del pack de referencia (4.7); release y bumps de línea (4.8).

## Pruebas

- #79: RED con el script ausente (38 `FAIL`; no fue TDD estricto: el borrador del script precedió al test); GREEN con 0 fallos y 45 casos. En Windows nativo, 41 correctos y 4 saltados (sin enlaces simbólicos); en Linux, 0 saltados con enlaces reales. 10 mutaciones del escritor detectadas. El orquestador repitió `test-materialize`, `test-validate-config` y `test-validate-pack` (0 fallos) y comprobó con sondas propias que `--dry-run` no escribe, que la repetición es idempotente por hash del árbol, que un overlay real sobre un id del núcleo es `FAIL`, que un id de extensión sin `replaces` es `FAIL` y con `replaces` conserva el overlay, y que ante un `FAIL` no se escribe nada. `validate-config.py`, `sdaf_packs.py` y los schemas no cambian.
- PR B (solo documentación, sin RED/GREEN: no hay cambio de comportamiento; comprobaciones estructurales y de los checks del repo sobre el árbol de trabajo): `check-version-metadata.py` (69 ficheros), `check-history-append-only.py`, `check-adrs.py`, `test-adrs.py`, `test-dates.py`, `test-docs.py`, `test-gate0.py`, `test-worklog.py`, `test-validate-config.py` (0 fallos), `test-validate-pack.py` (0 fallos), `test-materialize.py` (0 fallos, 4 saltados en Windows nativo), `validate-config.py`, `measure-handbook-scaffolding.py` (andamiaje extraído, 18 capítulos), `check-worklog-presence.py`, `validate-worklog.py` (Iteration-032 y la plantilla) y `check-local-links.py --strict-anchors --strict-orphans` sobre copia limpia (142 ficheros markdown, sin huérfanos). `mkdocs build --strict` sobre la misma copia termina con código 0 y sin avisos nuevos. Búsqueda de abstracción sobre el diff: sin nombres de stack, producto, herramienta ni del consumidor del piloto en lo añadido. Los ejemplos y mensajes de `docs/materializacion.md` se copiaron de ejecuciones reales de `materialize.py` con los fixtures en un directorio temporal fuera del repo, en Windows (copia) y en Linux (enlaces simbólicos relativos).

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| scripts/materialize.py, scripts/test-materialize.py, scripts/testdata/materialize/, .github/workflows/validate.yml | IA, redacción revisada | Subagente escritor (#79) |
| docs/materializacion.md | IA, redacción revisada | Subagente escritor; documento nuevo |
| docs/adopcion-y-upgrade.md, docs/contrato-pack-stack.md | IA, redacción revisada | Subagente escritor; sección «Materialización en el consumidor», «Fuera de 0.5.x», ruta normada y «Qué no existe todavía» |
| docs/README.md, docs/mapa-navegacion.md, mkdocs/mkdocs.yml | IA, redacción revisada | Subagente escritor; navegación |
| docs/iniciativas/INIT-arquitectura.md, docs/iniciativas/README.md | IA, redacción revisada | Subagente escritor; plan 0.1.31 e índice |
