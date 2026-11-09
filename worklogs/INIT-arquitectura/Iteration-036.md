---
pbi: INIT-arquitectura
iteracion: Iteration-036
fecha: 2026-11-09
inicio: 2026-11-09T09:52:00+01:00
fin: 2026-11-09T10:12:07+01:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano en la sesión: «Continua con ARQ-4.6» (2026-11-09), sobre el PBI ARQ-4.6 de INIT-arquitectura (escenarios y documentación)."
contexto: "ARQ-4.6 de INIT-arquitectura: los ejemplos 09 (varios packs y overlay) y 10 (varias unidades de código) que cierran el hallazgo H-6 junto con ARQ-4.5, y la migración de los ejemplos con pack del alias stack.pack a stack.packs. Entrega en un solo PR."
especificaciones_utilizadas: "odd/tasks/arq-4-6-ejemplos.md (S1 a S7 y L1 a L4); docs/iniciativas/INIT-arquitectura.md (ARQ-4.6, tabla de hallazgos y H-6); ADR-007 §5 y §8 (overlay y unidades); sdaf.config.schema.yaml (stack.packs, stack.overlay.replaces y stack.units); Iteration-035 como modelo de cierre"
archivos_leidos: "examples/01 a 08 y examples/README.md; configuracion/escenarios.md; docs/contrato-pack-stack.md y docs/materializacion.md; scripts/validate-config.py, scripts/validate-examples.py y scripts/test-validate-config.py; scripts/check-architecture.py (docstring); scripts/testdata/config-packs-varios.yaml, config-overlay-valido.yaml, config-units-valida.yaml, pack-valido.yaml y pack-otro.yaml; sdaf.config.schema.yaml; docs/iniciativas/INIT-arquitectura.md y README.md; templates/architecture-description.md; worklog Iteration-035"
archivos_modificados: "examples/04-pack-stack.yaml, examples/05-fusiones-mvp.yaml, examples/07-pack-frontend.yaml, examples/08-completo.yaml, examples/09-varios-packs.yaml (nuevo), examples/10-varias-unidades.yaml (nuevo), examples/README.md, configuracion/escenarios.md, docs/contrato-pack-stack.md, scripts/test-validate-config.py, docs/iniciativas/INIT-arquitectura.md (plan 0.1.36), docs/iniciativas/README.md y este worklog."
origen_cambios: "Redacción de un subagente escritor delegado, revisada por el orquestador; ver cuerpo."
resultado: "Los ejemplos 09 (core, dos packs ficticios y overlay con sustitución explícita) y 10 (tres unidades, una sin tests) existen y validan sin avisos, el 09 también con los manifiestos de sus dos packs. Los ejemplos 04, 05, 07 y 08 pasan del alias stack.pack a stack.packs conservando el pack real y las rutas, así que ningún ejemplo emite el aviso de alias. Se actualizan el README de ejemplos, la página de escenarios y el contrato de pack. Plan 0.1.36 con ARQ-4.6 hecho (32 de 34 PBIs) y H-6 cerrado. Sin tag ni release."
tiempo: PT15M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "El inicio (2026-11-09T09:52:00+01:00) es la hora aproximada de la primera orden del escritor en esta tarea; la redacción de la tarea, el mapeo previo y las decisiones del humano, anteriores, no se cronometraron. El fin es la hora de cierre de la redacción de este worklog. El tiempo es una estimación honesta de trabajo activo, sin cronometrar, y es menor o igual que la diferencia entre fin e inicio. Las decisiones del humano se tomaron el 2026-11-09 y la hora exacta no se registró. Sin entrada de handbook/CHANGELOG.md hasta ARQ-4.8; sdaf.version no cambia. Este worklog no registra el resultado del CI del PR."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (confirmar el commit, el push y el PR; después revisar y fusionar)
commit: null
pr: null
rama: feat/ejemplos-09-10
sha: null
resumen_acumulado: "ad hoc — ARQ-4.6: ejemplos 09 (varios packs y overlay) y 10 (varias unidades), ejemplos 04, 05, 07 y 08 migrados a stack.packs y documentación; plan 0.1.36 en rama local; sin PR"
---

# INIT-arquitectura / Iteration-036

## Línea de decisión

- Alcance: el PBI ARQ-4.6 del plan (`examples/09-varios-packs.yaml`, `examples/10-varias-unidades.yaml`, `examples/README.md` y `scripts/validate-examples.py`), que cierra H-6 junto con ARQ-4.5. Un solo PR.
- Decisiones del humano (2026-11-09, respuestas una a una; la hora exacta no se registró), citadas literalmente:
    - Decisión 1: «Migrar los cuatro a stack.packs (Recomendada)».
    - Decisión 2: «"0.5.0" en ambos (Recomendada)».
    - Decisión 3: «Ficticios: sdaf-stack-example y sdaf-stack-other (Recomendada)».
    - Decisión 4: «Dentro del 09, junto a los dos packs (Recomendada)».
    - Decisión 5: «No tocar el script; test que valida el 09 con manifiestos (Recomendada)».
    - Decisión 6: «Tres unidades 'Unidad A/B/C', una sin tests (Recomendada)».
- Decisiones por defecto, como propuesta del asistente no objetada por el humano y reabrible: se actualizan `examples/README.md`, `configuracion/escenarios.md` y `docs/contrato-pack-stack.md` (cita los escenarios 04, 07 y 08); el plan lleva una fila nueva y este worklog se añade en el mismo PR.
- Migración (decisión 1): `stack.pack: sdaf-stack-dotnet@0.3.0` pasa a `stack.packs` con ese único elemento en 04, 05, 07 y 08, que conservan el pack real, sus rutas y todo lo demás; en 08 la cabecera nombra `packs` en lugar de `pack`. El alias sigue cubierto por los fixtures `config-alias*.yaml`, que no se tocan.
- Ejemplo 09 (decisiones 2, 3 y 4): `sdaf.version` `"0.5.0"`, `stack.packs` con `sdaf-stack-example@0.1.0` y `sdaf-stack-other@0.2.0` (los de `scripts/testdata/pack-valido.yaml` y `pack-otro.yaml`), `src_path` y `tests_path`, y `stack.overlay.replaces` con `example-extension`. `agents.active` declara los activos habituales del núcleo y los dos ids de extensión (`example-extension`, `other-extension`), así que I4 se cumple con los manifiestos de ambos packs y no se concluye sin ellos. Los comentarios de cabecera dicen que los ids son ficticios.
- Ejemplo 10 (decisión 6): `sdaf.version` `"0.5.0"`, `stack.packs: []` y tres unidades «Unidad A» (`apps/api`, `tests/api`), «Unidad B» (`apps/web`, `tests/web`) y «Unidad C» (`libs/core`, sin `tests`), sin `src_path` ni `tests_path`. Los nombres son los de la plantilla de línea base y `check-architecture.py` (ARQ-6.2) los coteja con ella.
- Decisión 5: `scripts/validate-examples.py` no se toca; envuelve `validate-config.py`, que valida `examples/*.yaml`, así que 09 y 10 entran solos. `scripts/test-validate-config.py`: el caso de los ejemplos exige que ninguno emita el aviso de alias, que existan 09 y 10 y que el 09 valide con los dos `--pack-manifest` (también con `--strict-i4`) sin avisos; el 10, sin avisos.
- Qué no cambia: `scripts/validate-examples.py`; los ejemplos 01, 02, 03 y 06 (`pack: null`); `sdaf.config.example.yaml`; el catálogo `sdaf.config.schema.yaml`; las skills, los capítulos del handbook y las plantillas; `handbook/CHANGELOG.md`; los fixtures de `scripts/testdata/`.
- H-6 queda cerrado con ARQ-4.5 y ARQ-4.6; H-5 sigue abierto hasta ARQ-4.7. Siguiente trabajo: ARQ-4.7 (decisión J autorizada solo para lectura y cambio local; publicar en el repo del pack pide una autorización nueva) y ARQ-4.8.
- Documentación: `examples/README.md` (tabla y diagrama con 09 y 10, sección `stack.packs` con la nota del alias obsoleto, sección nueva `stack.overlay.replaces`, `stack.units` apuntando al ejemplo 10 y sin la frase «llegará con ARQ-4.6»), `configuracion/escenarios.md` (índice y secciones 09 y 10) y `docs/contrato-pack-stack.md` (escenarios 04, 07, 08 y 09).

## Pruebas

- RED real antes de crear 09 y 10 y de migrar: `test-validate-config.py` con 187 casos correctos y 9 fallando (la existencia de 09 y 10, el aviso de alias que aún emitían 04, 05, 07 y 08, y los tres casos nuevos de 09 con manifiestos y de 10).
- GREEN: `test-validate-config.py` con 194 casos correctos y 0 fallos.
- Mutaciones propias detectadas, sobre una copia fuera del repo: el 07 vuelve al alias; el 10 mezcla `src_path`; el 09 sustituye un id del núcleo en el overlay; el 09 cambia la versión de un pack y deja de casar con su manifiesto; el 09 pierde `example-extension` de `agents`; el 09 usa un id de extensión que ningún manifiesto aporta; el 10 desaparece. Quitar `other-extension` de `agents` no se detecta, y es correcto: un id que aporta un pack y la config no usa no es un error.
- Diferencial contra una copia de `HEAD` (stdout, stderr y código de salida): 82 comparaciones de `validate-config.py` (sin argumentos y con `--strict-i4`, y cada fichero con y sin `--strict-i4`) sobre `examples/01` a `08`, `sdaf.config.example.yaml` y los `scripts/testdata/config-*.yaml`; 72 iguales y 10 distintas, 0 diferencias de código de salida. Las únicas diferencias son el aviso de alias que desaparece de 04, 05, 07 y 08 y, en las ejecuciones sin ruta, los dos `OK` nuevos de 09 y 10.
- Comprobaciones del repo sobre el árbol de trabajo, todas con código de salida 0: `validate-config.py` y `validate-examples.py` (los diez ejemplos y `sdaf.config.example.yaml`, sin aviso de alias), `test-validate-pack.py`, `test-materialize.py` (4 saltados por enlaces simbólicos no disponibles), `check-version-metadata.py` (69 ficheros), `check-history-append-only.py` (69 artefactos), `check-adrs.py` (9 ADRs), `test-adrs.py`, `test-dates.py`, `validate-worklog.py` (Iteration-036 y, con `--plantilla`, la plantilla), `check-worklog-presence.py` y `measure-handbook-scaffolding.py`; sobre una copia limpia fuera del repo, `check-local-links.py --strict-anchors --strict-orphans` y `mkdocs build --strict`.
- Búsqueda de abstracción sobre el diff: no aparecen nombres de estilo, notación, stack, herramienta ni de ningún consumidor nuevos (el `sdaf-stack-dotnet` de 04, 05, 07 y 08 es previo y se conserva).

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| examples/04, 05, 07 y 08 | IA, redacción revisada | Subagente escritor; migración a `stack.packs` |
| examples/09-varios-packs.yaml, examples/10-varias-unidades.yaml | IA, redacción revisada | Subagente escritor; ids ficticios y nombres de la línea base |
| scripts/test-validate-config.py | IA, redacción revisada | Subagente escritor; RED observado antes de crear los ejemplos |
| examples/README.md, configuracion/escenarios.md, docs/contrato-pack-stack.md | IA, redacción revisada | Subagente escritor; tabla, diagrama y secciones |
| docs/iniciativas/INIT-arquitectura.md, docs/iniciativas/README.md | IA, redacción revisada | Subagente escritor; plan 0.1.36 e índice |
