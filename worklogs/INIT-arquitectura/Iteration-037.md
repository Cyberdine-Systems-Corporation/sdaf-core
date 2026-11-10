---
pbi: INIT-arquitectura
iteracion: Iteration-037
fecha: 2026-11-10
inicio: 2026-11-10T18:20:00+01:00
fin: 2026-11-10T18:44:00+01:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano en la sesión: «Adelante a todo» (2026-11-10), tras el informe del piloto de la línea 0.6.0, que propuso un PR para el hallazgo A1 con la guía y el mensaje y decisiones sobre A2 y A4."
contexto: "Piloto de la línea 0.6.0 (paso 2 del orden de ARQ-4.7, prerrequisito de ARQ-4.8) y primer PR de sus hallazgos genéricos: A1 (bloqueante), A3 y A5. Entrega en un solo PR."
especificaciones_utilizadas: "odd/tasks/piloto-0-6-0.md (L1 y L2) y odd/tasks/piloto-hallazgos.md (PR1); docs/iniciativas/INIT-arquitectura.md (sección 8, regla del piloto); Iteration-036 como modelo de cierre"
archivos_leidos: "docs/adopcion-y-upgrade.md; docs/materializacion.md; docs/contrato-pack-stack.md (encabezados); scripts/materialize.py y scripts/test-materialize.py; scripts/testdata/materialize/ (fixtures); scripts/validate-config.py, scripts/sdaf_diff.py, scripts/sdaf_docs.py y scripts/check-gate0.py (para verificar las afirmaciones de la guía); .github/actions/validate-sdaf/README.md; docs/iniciativas/INIT-arquitectura.md y README.md; worklog.schema.json; worklog Iteration-036"
archivos_modificados: "docs/adopcion-y-upgrade.md, docs/materializacion.md, scripts/materialize.py, scripts/test-materialize.py, docs/iniciativas/INIT-arquitectura.md (plan 0.1.37), docs/iniciativas/README.md y este worklog."
origen_cambios: "Redacción de un subagente escritor delegado, revisada por el orquestador; ver cuerpo."
resultado: "Un consumidor de 0.5.x que ya materializó agentes, prompts y skills por otro medio tiene ahora un procedimiento verificado para migrar a 0.6.0 (sección «Migrar de 0.5.x a 0.6.0» de la guía de adopción y sección «Migrar aportes ya materializados» de la guía de materialización), y los FAIL de colisión con el overlay y de enlace sin registro de materialize.py terminan con una pista hacia esa sección, sin cambiar el texto anterior, los códigos de salida ni lo que se escribe. Cubre A1, A3 y A5. Plan 0.1.37; ARQ-4.8 sigue pendiente. Sin tag ni release."
tiempo: PT20M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "El inicio (2026-11-10T18:20:00+01:00) es la hora aproximada de la primera orden del escritor en esta tarea; la redacción de la tarea, el piloto y las decisiones del humano, anteriores, no se cronometraron. El fin es la hora de cierre de la redacción de este worklog. El tiempo es una estimación honesta de trabajo activo, sin cronometrar, y es menor o igual que la diferencia entre fin e inicio. La hora exacta de la decisión del humano («Adelante a todo», 2026-11-10) no se registró. Sin entrada de handbook/CHANGELOG.md hasta ARQ-4.8; sdaf.version no cambia. Este worklog no registra el resultado del CI del PR."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (confirmar el commit, el push y el PR; después revisar y fusionar)
commit: null
pr: null
rama: fix/migracion-0-5-a-0-6
sha: null
resumen_acumulado: "ad hoc — piloto de la línea 0.6.0: guía de migración de 0.5.x a 0.6.0 (A1, A3 y A5), pista de migración en los FAIL de colisión de materialize.py y plan 0.1.37 en rama local; sin PR"
---

# INIT-arquitectura / Iteration-037

## Línea de decisión

- Alcance: el primer PR de los hallazgos del piloto de la línea `0.6.0`. Entran A1 (bloqueante), A3 y A5. No entra el modo `--adopt` (registrar un enlace sin registro cuyo destino resuelto coincide con el origen planificado): cambiaría el contrato de `materialize.py` ya cerrado y pide validación con enlaces reales en Linux, así que queda para `0.6.1`.
- Piloto (tramo 1): solo lectura, sobre una copia hecha con `git archive HEAD` del clon local de un consumidor real, sin escribir en él y sin red; los scripts del core se ejecutaron sobre la copia y el scratch se borró tras leer el informe. Según el plan (sección 8), el piloto es evidencia externa: sus hallazgos entran al core como cambios genéricos y este worklog no nombra al consumidor ni a su producto.
- Hallazgos y clasificación:
    - A1, bloquea `v0.6.0`: con los aportes ya materializados por la vía que documentaba la guía de `0.5.x` (enlaces simbólicos `120000` o copias, sin `.sdaf-origin`), `materialize.py` da `FAIL` en todos los destinos, porque lo no registrado lo trata como overlay; la guía no tenía paso de migración y el mensaje de colisión de pack sugería `stack.overlay.replaces` para ficheros que no eran un overlay intencionado. Entra en este PR.
    - A2, no bloquea: con manifiestos y `--strict-i4`, un id de extensión que solo aporta el overlay sigue dando `FAIL` en I4; ni el contrato local ni `stack.overlay.replaces` lo retiran, lo que contradice la invariante 4 del catálogo («packs o contratos locales»), y la action no pasa manifiestos, así que la CI no lo ve. Pendiente de decisión del humano; PR aparte (I4 con manifiestos y contratos locales).
    - A3, documentación: con `stack.units`, los ficheros transversales bajo `src/` o `tests/` que no caen en ninguna unidad dejan de exigir worklog. Entra en este PR como nota de la guía.
    - A4, ruido: `check-architecture` emite un `AVISO` por cada spec sin «Unidades» y tapa el relevante. PR aparte (agrupar en una línea con el recuento; los `FAIL` por spec no cambian).
    - A5, documentación: `materialize.py` no crea los espejos de editor (documentado fuera de alcance) y faltaba decir quién espeja las skills nuevas; `check-gate0` es opt-in y exige PBIs con la plantilla de `0.5.x`. Entra en este PR como nota de la guía.
    - B, deuda del consumidor (suya, no entra al core): línea base sin el ADR vigente más reciente, specs Approved sin el campo Unidades, PBIs anteriores a la plantilla, un stub sin contrato ni pack, y la subida de submódulos, del pin de la action y de los textos al migrar.
    - C, pack de referencia: sin hallazgos (su manifiesto valida y coincide con los ficheros).
    - D, copia: artefactos de la copia de trabajo (enlaces no creados por `git archive` en Windows sin privilegio, submódulos vacíos, rutas de origen raras); no son hallazgos.
- Decisión del orquestador y del humano: PR1 = A1 + A3 + A5; PR2 = A4; PR3 = A2 (a la espera de la decisión del humano); `--adopt` para `0.6.1`. Instrucción del humano: «Adelante a todo» (2026-11-10).
- Pista de migración en `scripts/materialize.py`: la constante `MIGRATION_HINT` se añade al **final** de los `FAIL` de colisión con el overlay (núcleo, contrato de agente de extensión, skill y prompt) y de enlace simbólico sin registro. El texto anterior queda intacto, incluida la sugerencia de `stack.overlay.replaces` para el agente de extensión (correcta si el fichero es un overlay intencionado). No la llevan la colisión entre capas, el elemento registrado y modificado ni el resto de `FAIL`. Los códigos de salida y lo que se escribe no cambian.
- Guía de adopción: sección «Migrar de 0.5.x a 0.6.0» (qué cambia, pasos, procedimiento para quien ya materializó con la salida literal de cada paso y notas A3 y A5) y enlace desde «Materialización en el consumidor». Guía de materialización: sección «Migrar aportes ya materializados» (ancla estable), nota bajo la tabla de colisiones con el texto literal de la pista y una celda de la tabla de re-ejecución; el modo `--adopt` se menciona solo como idea futura.
- Qué no cambia: `scripts/validate-config.py` y el resto de scripts, los schemas, las skills, los capítulos del handbook, las plantillas, la action, `handbook/CHANGELOG.md` y los fixtures de `scripts/testdata/`.

## Pruebas

- RED real antes de implementar: `test-materialize.py` con 55 casos correctos y 7 fallando (los cinco tipos de `FAIL` con la pista exacta, el enlace sin registro simulado y el `--dry-run` sobre aportes materializados sin registro); el enlace sin registro con enlaces reales se salta en este sistema, sin privilegio de enlaces.
- GREEN: `test-materialize.py` con 62 casos correctos, 0 fallos y 5 saltados (enlaces simbólicos no disponibles).
- Mutaciones propias detectadas (8), sobre una copia fuera del repo: el `FAIL` del núcleo sin la pista; la pista en la colisión entre capas; el ancla de la pista cambiada; la pista en el elemento registrado y modificado; la pista en medio del mensaje del agente de extensión; el enlace sin registro sin la pista; el `FAIL` de skill y de prompt sin la pista; la pista duplicada en el enlace sin registro.
- Diferencial contra una copia de `HEAD` (`git archive`): 33 escenarios de `materialize.py` sobre los fixtures de `scripts/testdata/materialize/` (éxito, `--dry-run`, idempotencia, quitar un pack, todos los `FAIL` de colisión, de manifiesto y de entrada, la migración y el enlace sin registro simulado), comparando salida, código de salida y árbol. 0 diferencias de código de salida y 0 de árbol. Las únicas diferencias de salida son la pista añadida al final de 28 líneas `FAIL` de 10 escenarios, y ninguna otra línea cambia.
- Procedimiento de migración probado sobre un repo sintético (fixtures del test con el core simulado y un pack ficticio, `git init` en un directorio temporal): `--dry-run` con 7 `FAIL` con la pista, `git rm` de esos destinos, `--dry-run` con 7 acciones de crear, ejecución real con 7 elementos materializados y segunda ejecución con `sin cambios`; lo propio del consumidor (`agents/local-agent.md`, `skills/local-skill/`) queda donde estaba. Es la salida que reproduce la guía.
- Comprobaciones del repo sobre el árbol de trabajo, todas con código de salida 0: `test-materialize.py` (62 casos, 5 saltados por enlaces simbólicos no disponibles), `test-validate-pack.py` (65), `test-architecture.py` (67), `test-docs.py` (61), `test-adrs.py` (56), `test-gate0.py` (66), `check-version-metadata.py` (69 ficheros), `check-history-append-only.py` (69 artefactos), `check-adrs.py` (9 ADRs), `validate-worklog.py` (Iteration-037 y, con `--plantilla`, la plantilla), `check-worklog-presence.py`, `measure-handbook-scaffolding.py`, `validate-config.py` y `validate-examples.py`; sobre una copia limpia fuera del repo, `check-local-links.py --strict-anchors --strict-orphans` y `mkdocs build --strict`.
- Búsqueda de abstracción sobre el diff: no aparecen nombres de estilo, notación, stack, herramienta ni de ningún consumidor del piloto; los ids de los ejemplos son los ficticios de los fixtures.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| docs/adopcion-y-upgrade.md, docs/materializacion.md | IA, redacción revisada | Subagente escritor; la salida literal procede de la ejecución real |
| scripts/materialize.py, scripts/test-materialize.py | IA, redacción revisada | Subagente escritor; RED observado antes de implementar |
| docs/iniciativas/INIT-arquitectura.md, docs/iniciativas/README.md | IA, redacción revisada | Subagente escritor; plan 0.1.37 e índice |
