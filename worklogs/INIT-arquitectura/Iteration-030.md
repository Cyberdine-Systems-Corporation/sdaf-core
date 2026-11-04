---
pbi: INIT-arquitectura
iteracion: Iteration-030
fecha: 2026-11-03
inicio: 2026-11-03T14:42:22+01:00
fin: 2026-11-04T08:47:02+01:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano en la sesión: ejecutar ARQ-4.2 (varios packs en la config), segundo PBI del camino a v0.6.0, tras preguntar «Cual es siguiente paso?» y responder «Si, empieza con mapeo de ARQ-4.2» (2026-11-03)."
contexto: "ARQ-4.2 de INIT-arquitectura: stack.packs con stack.pack como alias obsoleto (PR #74), módulo hermano sdaf_packs.py con el hueco de provides de ARQ-4.1 cerrado (PR #73), y --pack-manifest con rango core, colisiones, I4 con manifiestos y aviso de ausencia (PR #75); contrato de pack, plan y worklog en el PR de cierre."
especificaciones_utilizadas: "architecture/decisions/ADR-007-modelo-de-capas-y-precedencia.md (§3, §5 y Consecuencias); docs/iniciativas/INIT-arquitectura.md (D-6, D-7, ARQ-4.1, ARQ-4.2); docs/contrato-pack-stack.md; sdaf.config.schema.json y .yaml; Iteration-029 como modelo de cierre"
archivos_leidos: "architecture/decisions/ADR-007-modelo-de-capas-y-precedencia.md; docs/contrato-pack-stack.md; docs/iniciativas/INIT-arquitectura.md; docs/iniciativas/README.md; sdaf.config.schema.json y .yaml; scripts/validate-config.py, test-validate-config.py, validate-pack.py y test-validate-pack.py; sdaf-pack.schema.json; examples/*.yaml; worklog.schema.json; worklogs Iteration-029 y 028 como modelo"
archivos_modificados: "PR #73: scripts/sdaf_packs.py (nuevo), scripts/validate-pack.py y scripts/test-validate-pack.py. PR #74: sdaf.config.schema.json y .yaml, scripts/validate-config.py, scripts/test-validate-config.py y 14 fixtures scripts/testdata/config-*.yaml. PR #75: scripts/sdaf_packs.py, scripts/validate-pack.py, scripts/validate-config.py, scripts/test-validate-config.py, scripts/test-validate-pack.py y los fixtures scripts/testdata/pack-otro.yaml y config-packs-060.yaml. PR de cierre: docs/contrato-pack-stack.md; docs/iniciativas/INIT-arquitectura.md (plan 0.1.29); docs/iniciativas/README.md; este worklog."
origen_cambios: "Scripts, schema, fixtures y pruebas (#73, #74 y #75): redacción de subagentes escritores delegados, revisada y verificada por el orquestador. Contrato, plan, índice y worklog (PR de cierre): redacción de un subagente escritor delegado, revisada por el orquestador; ver cuerpo."
resultado: "ARQ-4.2 hecho en tres PRs fusionados en main (#73, #74 y #75): stack.packs con stack.pack como alias obsoleto, rango core contra sdaf.version, colisiones de ids de extensión, skill y prompt entre manifiestos, I4 con manifiestos y aviso por manifiesto ausente desde la línea 0.6.0; el contrato de pack lo documenta (PR de cierre, en rama local). Sin tag ni release: v0.6.0 es ARQ-4.8. Sigue pendiente el visto bueno explícito del humano sobre el rango >=X.Y.Z <=X.Y.Z como versión única."
tiempo: PT3H
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "El inicio (2026-11-03T14:42:22+01:00) es aproximado: es la hora del commit del PR #73 (6ca0b63), el primer instante registrado de la serie; el mapeo y el diseño previos no se cronometraron. El tiempo es una estimación honesta de trabajo activo de las tres entregas y del cierre, sin cronometrar, y es menor o igual que la diferencia entre fin e inicio. Las decisiones del humano se tomaron el 2026-11-03 y la hora exacta no se registró. Sin CHANGELOG ni entrada de handbook hasta ARQ-4.8; sdaf.version y los capítulos no cambian. Este worklog no registra el resultado del CI de ningún PR."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (confirmar el commit local; después publicar el PR)
commit: null
pr: null
rama: docs/contrato-packs-arq-4-2
sha: null
resumen_acumulado: "ad hoc — ARQ-4.2 varios packs en la config: #73, #74 y #75 fusionados; contrato y plan 0.1.29 en rama local; sin PR de cierre"
---

# INIT-arquitectura / Iteration-030

## Línea de decisión

- Decisiones del humano (2026-11-03, respuestas una a una; la hora exacta no se registró):
    - Coexistencia de `stack.pack` (no nulo) y `stack.packs`: «Error (Recomendado)».
    - Localización de manifiestos: «--pack-manifest RUTA, repetible (Recomendado)».
    - Aviso por manifiesto ausente: «Solo con sdaf.version >= 0.6.0 (Recomendado)».
    - Rango frente a una línea: «Tupla X.Y.Z literal (Recomendada)».
- El resto se aplicó por defecto, como propuesta del asistente no objetada por el humano y reabrible: `stack.packs` es una lista de cadenas `id@version` con `uniqueItems` y el patrón estricto del manifiesto; el aviso de alias solo salta con `stack.pack` no nulo; el hueco del `$` se corrige en el validador con `edge_issue` y no en el schema; un YAML roto es un `FAIL` limpio sin traceback; I4 sin manifiestos conserva la conducta anterior (cualquier pack declarado cuenta) y con manifiestos exige que cada id de extensión usado figure en `provides.extension_ids` de algún pack.
- Diseño: `validate-config.py` no comparaba `sdaf.version` con nada antes de ARQ-4.2. El validador de manifiestos (`validate-pack.py`, con guion en el nombre y por tanto no importable) se partió en un módulo hermano `scripts/sdaf_packs.py`, que reutilizan los dos scripts (patrón de `sdaf_adrs.py` y `sdaf_docs.py`). Los manifiestos solo se leen con `--pack-manifest RUTA` (repetible): el core no tiene todavía una ruta normada de manifiestos (ADR-007 §7, ARQ-4.4). El `id@version` de cada manifiesto se cruza con las referencias de `stack.packs` o del alias; el rango `core` se compara con `sdaf.version` como tupla de enteros `X.Y.Z` literal, así que los rangos usan límites `X.Y.0`.
- Entrega en tres PRs a `main`, más el de cierre:
    - #73 (módulo `sdaf_packs.py` extraído sin cambio de comportamiento y hueco de `provides` cerrado; +96/−58; merge `36b40a1`).
    - #74 (`stack.packs`, alias obsoleto, coexistencia = error, duplicados por id = error, `WARN` de alias solo con `stack.pack` no nulo, agujero del `$` y YAML roto sin traceback, schema JSON y catálogo; +455/−19; `size:exception` declarada; merge `8c47ef0`).
    - #75 (`--pack-manifest` repetible, rango `core` frente a `sdaf.version`, colisiones de ids de extensión, skill y prompt entre manifiestos, I4 con manifiestos, aviso de ausencia; +503/−151, unas 275 líneas movidas de `validate-pack.py` a `sdaf_packs.py`; `size:exception` declarada; merge `5423b51`).
    - Ramas de #73, #74 y #75 borradas en local y en remoto. El humano confirmó cada commit y la apertura de cada PR; los tres están fusionados en `main`.
- Contrato de pack: la sección «Relación con `stack.packs`» sustituye al aviso «no existe todavía» y documenta lo implementado; una sección «Qué no existe todavía» deja el aviso breve de lo que sigue pendiente. Las menciones sueltas a `stack.pack` (Identidad, tabla de `id`, Cumplimiento, Relacionado) remiten a `stack.packs`.
- Duda abierta, **pendiente de visto bueno explícito del humano**: `core: ">=X.Y.Z <=X.Y.Z"` se acepta como versión única (decisión del escritor de ARQ-4.1, mantenida en ARQ-4.2); la lectura estricta (inferior menor que superior) lo rechazaría.
- Fuera de alcance, sin tocar: contraste de los `extension_ids` de un manifiesto con el catálogo de ids del core; overlay y sustitución explícita (4.3); materialización y ruta normada de los packs (4.4); `stack.units` (4.5); `examples/09` y `10` (4.6); manifiesto real del pack de referencia (4.7); input de la action `validate-sdaf` para pasar manifiestos (no pedido); release y bumps (4.8). Los ejemplos 04, 05, 07 y 08 siguen usando `stack.pack` y emiten el `WARN` de alias. Con ARQ-4.2 hecho son 27 de 34 PBIs; H-5 sigue abierto hasta `v0.6.0`. La decisión J (autorización sobre el repo del pack de referencia) «se da cuando ARQ-4.2 esté fusionado»: ya procede decidirla y sigue abierta. La decisión K también.

## Hallazgos

- Hueco de ARQ-4.1 en `provides`: un id con salto de línea final (bloque literal `|` de YAML) pasaba con `OK` en `validate-pack.py` porque `edge_issue` solo se aplicaba a `id`, `version`, `core` y `requires`. Cerrado en #73 aplicándolo a cada elemento de `provides.extension_ids`, `skills` y `prompts`.
- Agujero del `$` en `validate-config.py` (anunciado en Iteration-029): `sdaf.version`, `stack.pack`, cada elemento de `stack.packs` y `tooling.gentle_ai` aceptaban un salto de línea final. Cerrado en el validador en #74 (no en el schema, que por sí solo sigue admitiéndolo).
- Un YAML roto o no UTF-8 en `validate-config.py` terminaba en traceback; ahora es `FAIL` con motivo (#74).

## Pruebas

- #73: RED con 3 casos (uno por lista de `provides`); GREEN con 63 casos, 3 nuevos. Comprobación diferencial del commit base frente al nuevo sobre 14 casos: 0 diferencias. Mutación (quitar el bucle de `provides`): fallan exactamente los 3 casos nuevos.
- #74: RED con 26 fallos, 2 de ellos tracebacks; GREEN con 39 casos. Diferencial sobre 13 casos: solo las diferencias esperadas (el `WARN` de alias en los ejemplos 04, 05, 07 y 08 y en `invalid-invariants.yaml`, y el texto de I4 «sin packs»), con el mismo código de salida. 4 mutaciones detectadas.
- #75: RED con 44 casos en `FAIL`; GREEN con 117 casos. Diferencial de `validate-pack.py` sobre 15 casos (única diferencia: el fixture nuevo `pack-otro.yaml`) y de `validate-config.py` sin el flag sobre 28 casos (única diferencia: el fixture nuevo `config-packs-060.yaml`). Sondas reales con la salida esperada: `sdaf.version` 0.6.0 con rango coincidente `OK`; 0.7.0 fuera de rango `FAIL`; 0.6.0 sin el flag, `WARN` de ausencia; 0.5.0, sin aviso; manifiesto inexistente, `FAIL`. 5 mutaciones detectadas (8, 3, 4, 8 y 5 casos).
- Checks del repo sobre la rama de cierre: `check-version-metadata.py`, `check-history-append-only.py`, `check-adrs.py`, `test-adrs.py`, `test-dates.py`, `test-docs.py`, `test-gate0.py`, `test-worklog.py`, `test-validate-config.py`, `test-validate-pack.py`, `validate-pack.py` (plantilla), `validate-config.py`, `validate-examples.py`, `measure-handbook-scaffolding.py`, `validate-worklog.py` (Iteration-030) y `check-local-links.py --strict-anchors --strict-orphans` sobre copia limpia. Los mensajes que cita el contrato se contrastaron ejecutando `validate-config.py` y `validate-pack.py` con los fixtures reales. markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| scripts/sdaf_packs.py, scripts/validate-pack.py, scripts/test-validate-pack.py | IA, redacción revisada | Subagentes escritores (#73 y #75) |
| scripts/validate-config.py, scripts/test-validate-config.py, scripts/testdata/ | IA, redacción revisada | Subagentes escritores (#74 y #75) |
| sdaf.config.schema.json, sdaf.config.schema.yaml | IA, redacción revisada | Subagente escritor (#74) |
| docs/contrato-pack-stack.md | IA, redacción revisada | Subagente escritor; sección «Relación con `stack.packs`» |
| docs/iniciativas/INIT-arquitectura.md, docs/iniciativas/README.md | IA, redacción revisada | Subagente escritor; plan 0.1.29 e índice |
