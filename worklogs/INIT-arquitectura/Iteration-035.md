---
pbi: INIT-arquitectura
iteracion: Iteration-035
fecha: 2026-11-08
inicio: 2026-11-08T19:49:24+01:00
fin: 2026-11-08T20:08:22+01:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano en la sesión: «Plantealo como tarea e incluyamos los 3 en un PR. Muestrame la pregunta y las posibles opciones a elegir cuando proceda decidir.» (2026-11-08), sobre los tres defectos menores de materialize.py anotados en Iteration-032."
contexto: "Seguimiento de ARQ-4.4 de INIT-arquitectura: tres defectos de mensajes de scripts/materialize.py vistos al documentarlo (Iteration-032). Ninguno cambia lo que el script escribe ni sus códigos de salida. Entrega en un solo PR."
especificaciones_utilizadas: "odd/tasks/materialize-defectos.md (S1 a S4 y L1 a L3); docs/materializacion.md (tabla de colisiones); docs/iniciativas/INIT-arquitectura.md (ARQ-4.4); Iteration-032 como origen de los hallazgos y Iteration-034 como modelo de cierre"
archivos_leidos: "scripts/materialize.py, scripts/sdaf_packs.py, scripts/validate-pack.py, scripts/validate-config.py; scripts/test-materialize.py, scripts/test-validate-pack.py y scripts/test-validate-config.py; sdaf-pack.schema.json; scripts/testdata/pack-*.yaml y scripts/testdata/materialize/; docs/materializacion.md; docs/iniciativas/INIT-arquitectura.md y README.md; templates/worklog.md; worklogs Iteration-032 y Iteration-034"
archivos_modificados: "scripts/materialize.py, scripts/sdaf_packs.py, scripts/test-materialize.py, scripts/test-validate-pack.py, scripts/test-validate-config.py, docs/iniciativas/INIT-arquitectura.md (plan 0.1.35), docs/iniciativas/README.md y este worklog. docs/materializacion.md no cambia: solo cita el mensaje de skills, que ya era correcto."
origen_cambios: "Redacción de un subagente escritor delegado, revisada por el orquestador; ver cuerpo."
resultado: "Los tres defectos menores de materialize.py quedan corregidos en rama local: la colisión de un prompt con el overlay dice «en un prompt» (la de una skill, «en una skill»); un motivo idéntico del manifiesto ya no sale repetido, ni en materialize.py ni en validate-pack.py ni en validate-config.py --pack-manifest; y los FAIL de un pack de materialize.py muestran la ruta tal como se pasó en --pack. Sin cambio en lo que se escribe ni en los códigos de salida. Plan 0.1.35. Sin tag ni release."
tiempo: PT15M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "El inicio (2026-11-08T19:49:24+01:00) es la hora de la primera orden del escritor en esta tarea; la redacción de la tarea y las decisiones del humano, previas, no se cronometraron. El fin es la hora de cierre de la redacción de este worklog. El tiempo es una estimación honesta de trabajo activo, sin cronometrar, y es menor o igual que la diferencia entre fin e inicio. Las decisiones del humano se tomaron el 2026-11-08 y la hora exacta no se registró. Sin entrada de handbook/CHANGELOG.md hasta ARQ-4.8; sdaf.version no cambia. Este worklog no registra el resultado del CI del PR."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (confirmar el commit, el push y el PR; después revisar y fusionar)
commit: null
pr: null
rama: fix/materialize-mensajes
sha: null
resumen_acumulado: "ad hoc — tres defectos menores de materialize.py corregidos (artículo de la colisión de un prompt, motivo del manifiesto repetido y ruta de pack tal como se pasó); plan 0.1.35 en rama local; sin PR"
---

# INIT-arquitectura / Iteration-035

## Línea de decisión

- Alcance: tres defectos de mensajes anotados en Iteration-032, que `materialize.py` mostraba con un manifiesto o una colisión concretos. Ninguno cambia lo que el script escribe ni sus códigos de salida. Un solo PR, por decisión del humano (2026-11-08).
- Decisiones del humano (2026-11-08, respuestas una a una; la hora exacta no se registró), citadas literalmente:
    - Defecto 2, motivo repetido: «En el modulo compartido (Recomendada)».
    - Defecto 3, ruta mostrada: «La ruta tal como se paso en --pack (Recomendada)».
- Decisiones por defecto, como propuesta del asistente no objetada por el humano y reabrible: el artículo de la colisión de un prompt se corrige sin consulta; el mensaje «core: no existe el directorio …» no se toca; el worklog y el plan 0.1.35 llevan una fila nueva en este mismo PR.
- Defecto 1: la colisión de un prompt con el overlay decía «en una prompt». `overlay_decision` construye ahora «en una skill» o «en un prompt» con el artículo incluido. El resto del mensaje no cambia.
- Defecto 2, causa real: `jsonschema` emite un error `required` por cada propiedad ausente, y `schema_reason` nombra todas las ausentes en cada uno de ellos. Con `core` y `provides` ausentes salían dos errores con el mismo texto; con las cuatro ausentes, cuatro. Estaba en `sdaf_packs.manifest_issues`, que comparten `validate-pack.py`, `validate-config.py` (`--pack-manifest`) y `materialize.py`, y por eso afectaba a los tres. Se conserva la primera aparición de cada motivo del schema, en el mismo orden; ningún motivo distinto se pierde y los motivos de coherencia (`semantic_issues`) no se tocan.
- Defecto 3: `resolve_layers` mostraba la ruta resuelta (`label_of`), que es absoluta cuando el pack queda fuera del repo del core. Ahora muestra el texto de `--pack` sin barras finales y, para el manifiesto, `<ruta>/sdaf-pack.yaml`; también en «el pack … ya se pasó desde <ruta>». `sdaf_packs.label_of` no cambia: `validate-pack.py`, `validate-config.py` y el core siguen mostrando la ruta relativa al repo. El mensaje «core: no existe el directorio …» no se toca: imprime la ruta resuelta del core (por defecto `<consumer-root>/.sdaf`), que el usuario no siempre escribe y que ayuda a ver cuál se buscó.
- Qué no cambia: lo que `materialize.py` escribe, el contenido de `.sdaf-origin`, los códigos de salida, la salida de los scripts con un manifiesto sin motivos repetidos ni la de `validate-pack.py` y `validate-config.py` con rutas, el orden de los motivos y la ayuda de los comandos.
- Documentación: `docs/materializacion.md` solo cita el mensaje de skills (ya correcto), no el de prompts ni los FAIL de pack con rutas, y no cambia.

## Pruebas

- RED real antes de implementar: `test-materialize.py` con 11 casos nuevos fallando (el prompt y las rutas relativa y absoluta de pack inexistente, sin manifiesto, manifiesto inválido con motivo repetido, y id repetido); `test-validate-pack.py` con 2 fallando (motivo repetido con dos y con cuatro propiedades ausentes); `test-validate-config.py` con 1 fallando (el mismo caso con `--pack-manifest`, ejecutado contra el `sdaf_packs.py` anterior).
- GREEN: `test-materialize.py` 51 casos correctos y 0 fallos (4 saltados por enlaces simbólicos no disponibles); `test-validate-pack.py` 65 correctos y 0 fallos; `test-validate-config.py` 187 correctos y 0 fallos. Casos previos sin tocar.
- 7 mutaciones propias detectadas: no deduplicar; deduplicar perdiendo un motivo distinto (uno por tipo de error); volver al artículo antiguo; usar `label_of(root)` otra vez; no quitar las barras finales; usar `label_of(manifest)` para el manifiesto; mostrar la ruta resuelta en «ya se pasó desde».
- Diferencial contra una copia de `HEAD` (stdout, stderr y código de salida): 102 comparaciones, 79 iguales y 23 distintas; 0 diferencias de código de salida. `validate-pack.py` y `validate-config.py --pack-manifest` sobre todos los manifiestos de `scripts/testdata/` y la plantilla, y `validate-config.py` sobre `examples/` y `sdaf.config.example.yaml`: sin diferencias (ningún fixture repetía una línea). `materialize.py` sobre 20 casos de los fixtures con rutas de pack relativas y absolutas, FAIL incluidos, más 3 con packs dentro del repo: las únicas diferencias son la línea repetida que desaparece, el artículo del prompt y la ruta de pack mostrada como se pasó; el árbol escrito es idéntico salvo en el caso con packs del repo, donde `origin` de `.sdaf-origin` cambia solo porque la copia base está en otro directorio (artefacto de la comprobación). Con manifiestos improvisados, `validate-pack.py` y `validate-config.py` dejan de repetir la línea y conservan los demás motivos.
- Comprobaciones del repo sobre el árbol de trabajo, todas con código de salida 0: `test-gate0.py`, `test-adrs.py`, `test-docs.py`, `test-diff.py`, `test-architecture.py`, `check-version-metadata.py` (69 ficheros), `check-history-append-only.py` (69 artefactos), `check-adrs.py` (9 ADRs), `measure-handbook-scaffolding.py`, `validate-worklog.py` (Iteration-035 y, con `--plantilla`, la plantilla), `validate-config.py` y `validate-examples.py`; sobre una copia limpia fuera del repo, `check-local-links.py --strict-anchors --strict-orphans` y `mkdocs build --strict`.
- Búsqueda de abstracción sobre el diff: no aparecen nombres de estilo, notación, stack, herramienta ni de ningún consumidor.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| scripts/materialize.py, scripts/sdaf_packs.py | IA, redacción revisada | Subagente escritor; artículo, motivos sin repetir y ruta tal como se pasó |
| scripts/test-materialize.py, scripts/test-validate-pack.py, scripts/test-validate-config.py | IA, redacción revisada | Subagente escritor; un test por defecto |
| docs/iniciativas/INIT-arquitectura.md, docs/iniciativas/README.md | IA, redacción revisada | Subagente escritor; plan 0.1.35 e índice |
