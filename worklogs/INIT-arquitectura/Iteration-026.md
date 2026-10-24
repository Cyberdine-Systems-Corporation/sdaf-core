---
pbi: INIT-arquitectura
iteracion: Iteration-026
fecha: 2026-10-24
inicio: 2026-10-24T19:34:29+02:00
fin: 2026-10-24T20:18:00+02:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano en la sesión: ejecutar ARQ-6.1 (Gate 0 semiautomático) como siguiente paso del bloque 6 («Siguiente paso», 2026-10-24) con el diseño B recomendado («APlicalo», 2026-10-24)."
contexto: "ARQ-6.1 de INIT-arquitectura: comprobaciones mecánicas de Gate 0 (check-gate0.py), módulos de lectura compartidos y su input opt-in en la action validate-sdaf, con guía para el consumidor."
especificaciones_utilizadas: "handbook/05-development-workflow.md (Gate 0 y excepción de adopción); handbook/14-architecture-description.md §6 y §7; handbook/13-enmienda-excepciones-ciclo-de-vida.md §3; skills/sdaf-gate0/SKILL.md; templates/pbi.md; docs/iniciativas/INIT-arquitectura.md (ARQ-6.1)"
archivos_leidos: "scripts/check-worklog-presence.py, check-adrs.py, sdaf_adrs.py y validate-worklog.py; templates/pbi.md; skills/sdaf-gate0/SKILL.md; worklog.schema.json; .github/actions/validate-sdaf/ (action.yml y README.md); docs/adopcion-y-upgrade.md; plan de la iniciativa; worklog Iteration-025; plantilla de worklog"
archivos_modificados: "scripts/sdaf_diff.py, scripts/sdaf_docs.py y scripts/check-gate0.py (nuevos); scripts/check-worklog-presence.py, check-adrs.py y sdaf_adrs.py (refactor sin cambio de comportamiento); scripts/test-docs.py y test-gate0.py (nuevos); scripts/testdata/gate0-valido/ (fixture nuevo); .github/workflows/validate.yml (dos pasos de prueba); .github/actions/validate-sdaf/action.yml y README.md; docs/adopcion-y-upgrade.md; docs/iniciativas/INIT-arquitectura.md (plan 0.1.25); docs/iniciativas/README.md; este worklog."
origen_cambios: "Scripts, pruebas, fixture, action y docs: redacción de subagentes escritores delegados, revisada y verificada por el orquestador; ver cuerpo."
resultado: "check-gate0.py hace las comprobaciones mecánicas de G0.1, G0.2, G0.4, G0.5 y G0.6 del PBI en curso, es bloqueante y no aprueba nada (#61 y #62, fusionados); la action validate-sdaf gana los inputs check-gate0 y gate0-pbi, desactivados por defecto, con guía en adopcion-y-upgrade.md (PR de cierre, en rama local). Pendiente de publicar como parche junto a ARQ-6.3."
tiempo: PT40M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "El inicio (19:34:29) es la hora del primer commit de la serie (4650ae4); el mapeo y el diseño previos no se cronometraron. El tiempo es una estimación de trabajo activo y es menor o igual que la diferencia entre fin e inicio. Sin tag ni Release todavía: se publicará como parche junto a ARQ-6.3, con confirmación aparte. No se ha ejecutado check-gate0.py sobre el core (no tiene backlog/, specs/ ni architecture/description.md): en el CI del core solo corre test-gate0.py sobre el fixture. Este worklog no registra el resultado del CI de ningún PR."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (confirmar el commit local; después publicar el PR)
commit: null
pr: null
rama: feat/action-check-gate0
sha: null
resumen_acumulado: "ad hoc — ARQ-6.1 Gate 0 semiautomático: #61 y #62 fusionados; action y guía en rama local; sin PR/tag"
---

# INIT-arquitectura / Iteration-026

## Línea de decisión

- Decisión del humano («APlicalo», 2026-10-24; la hora exacta no se registró): diseño B. El comprobador es **bloqueante** (código de salida 1 con algún `FAIL`), coherente con el STOP de Gate 0 en [H05](../../handbook/05-development-workflow.md). Solo hace comprobaciones **mecánicas**: no decide, no aprueba, no cambia estados ni escribe ficheros, y su redacción nunca afirma que Gate 0 esté cumplido.
- El PBI en curso se elige por el diff del PR (como `check-worklog-presence.py`, con el mismo módulo de diff) y `--pbi` lo anula. Si el diff toca código de producto y no identifica ningún PBI, es un `FAIL` (STOP) en vez de un OK por omisión.
- G0.3 es juicio humano: sale siempre como `AVISO`, y el comprobador solo verifica que los ADRs citados existan y estén Aceptados. La caracterización Approved cuenta para G0.1, con `AVISO` si todas las specs del PBI son de caracterización; un acceptance dado por ID debe estar Approved y tener criterios.
- La excepción de adopción (H05, H13 §3) no se puede detectar mecánicamente: el comprobador nunca relaja un `FAIL` por ella y, si la línea base declara unidades «heredada», solo añade un `AVISO`. Un PR correctivo legítimo en el perímetro heredado fallará el paso; quien tenga activo el input debe desactivarlo en ese PR (queda escrito en la guía).
- La action añade `check-gate0` (desactivado por defecto) y `gate0-pbi`; las entradas se pasan por `env`, nunca interpoladas en el script, y con los valores por defecto la action no cambia.
- Entrega en tres PRs: #61 (refactor y módulo de lectura, +492/-68, con `size:exception` declarada en la descripción), #62 (`check-gate0.py`, su prueba y el fixture, +978, con `size:exception` declarada) y el de cierre (action, guía, worklog y plan). El humano confirmó cada commit, los pushes y los PRs, y fusionó #61 y #62.
- Decisiones menores del escritor, aceptadas por defecto: la salida usa líneas `OK`, `FAIL` y `AVISO` con el código de la comprobación y el PBI; un ADR con estado heredado «Accepted» cuenta como Aceptado (misma tabla que el modo consumidor); un enlace externo en `Acceptance` es `AVISO`; `backlog/README.md` no se trata como PBI.
- Fuera de alcance, sin tocar: H05, `skills/sdaf-gate0`, `templates/*`, `stack.units` (v0.6.0), vocabulario de cierre de PBI y vigencia de `Caducidad`. Con ARQ-6.1 hecho son 25 de 34 PBIs; quedan ARQ-4.1 a 4.8 y ARQ-6.2. Siguen abiertas las decisiones J y K.
- Límites conocidos, no corregidos: G0.2 y G0.4 duplican el `FAIL` cuando `Acceptance` está vacío; el `AVISO` de la excepción de adopción sale con cualquier `FAIL`, también si el diff no se pudo calcular; no se calcula la vigencia de `Caducidad` de los ADRs.

## Pruebas

- TDD: en #62, RED observado con `check-gate0.py` ausente (55 casos fallando) y GREEN con 58 casos en `test-gate0.py`; en #61, `test-docs.py` con RED por módulo ausente y GREEN con 47 casos.
- Refactor sin cambio de comportamiento (#61): comparación diferencial de 101 casos entre el commit base y el nuevo (`--changed` con configuración por defecto, personalizada y ausente, `--base`, evento de PR con JSON y con `GITHUB_BASE_SHA`, 48 árboles de ADRs y modo `--consumer`), 0 diferencias en salida y código de salida; repetida por el orquestador con el mismo resultado. `test-worklog.py`, `test-adrs.py` y `test-dates.py` pasan sin modificarse.
- Mutaciones sobre una copia de `check-gate0.py`, con el resultado de `test-gate0.py`: G0.1 sin comprobar el estado (2 casos fallan), G0.6 que acepta Draft (3), G0.3 que ignora el estado del ADR (1), salida siempre 0 (87), FAIL sin contar (87) y línea anterior a 0.5.0 que no corta (2).
- Pruebas propias del orquestador sobre #62: raíz sin git ni flags, `AVISO` y salida 0; `--pbi` inexistente, `FAIL` y salida 1; evento de PR ilegible, `FAIL` sin traceback; diff sin producto, OK; diff con producto y sin PBI, `FAIL` STOP; línea 0.4.2, `AVISO` y salida 0; spec que no es UTF-8, `FAIL` sin traceback.
- Simulación local del paso de la action sobre el fixture `gate0-valido`: `gate0-pbi` con `PBI-PRD-001`, salida 0; vacío y sin diff, `AVISO` y salida 0; con un PBI inexistente, salida 1; con un valor hostil (`x; echo PWNED`, una sustitución de comandos y un comodín) cada palabra llega al script como un PBI desconocido, no se ejecuta nada y el comodín no se expande; un valor que empieza por `-` se rechaza con salida 2.
- Checks del repo sobre la rama de cierre: `test-gate0.py` (58), `test-docs.py` (47), `test-adrs.py` (40), `test-dates.py`, `test-worklog.py` y `test-validate-config.py` en verde. markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| scripts/sdaf_diff.py, scripts/check-worklog-presence.py, scripts/check-adrs.py, scripts/sdaf_adrs.py | IA, redacción revisada | Subagente escritor; refactor sin cambio de comportamiento (#61) |
| scripts/sdaf_docs.py, scripts/test-docs.py | IA, redacción revisada | Subagente escritor; lectura de documentos compartida (#61) |
| scripts/check-gate0.py, scripts/test-gate0.py, scripts/testdata/gate0-valido/ | IA, redacción revisada | Subagente escritor; comprobaciones mecánicas, 58 casos y fixture (#62) |
| .github/workflows/validate.yml | IA, redacción revisada | Pasos `test-docs.py` y `test-gate0.py` |
| .github/actions/validate-sdaf/action.yml y README.md | IA, redacción revisada | Inputs `check-gate0` y `gate0-pbi` |
| docs/adopcion-y-upgrade.md | IA, redacción revisada | Sección «Comprobar Gate 0 en el PR» y limitaciones |
| docs/iniciativas/INIT-arquitectura.md, docs/iniciativas/README.md | IA | Plan 0.1.25 e índice; estado verificado |
