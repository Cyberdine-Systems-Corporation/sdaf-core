---
pbi: INIT-arquitectura
iteracion: Iteration-029
fecha: 2026-11-01
inicio: 2026-11-01T11:57:27+01:00
fin: 2026-11-02T18:27:53+01:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano en la sesión: ejecutar ARQ-4.1 (manifiesto de pack), primer PBI del camino a v0.6.0, tras recomendárselo como siguiente paso («Si, empieza», 2026-11-01)."
contexto: "ARQ-4.1 de INIT-arquitectura: manifiesto sdaf-pack.yaml con su schema, plantilla y validador (PR A, #71) y sección «Manifiesto» del contrato de pack (PR B)."
especificaciones_utilizadas: "architecture/decisions/ADR-007-modelo-de-capas-y-precedencia.md (§3, §5, §6 y Consecuencias); docs/iniciativas/INIT-arquitectura.md (D-7, ARQ-4.1, ARQ-4.2, §11); docs/contrato-pack-stack.md; Iteration-026 y 028 como modelo de cierre"
archivos_leidos: "architecture/decisions/ADR-007-modelo-de-capas-y-precedencia.md; docs/contrato-pack-stack.md; docs/iniciativas/INIT-arquitectura.md; docs/iniciativas/README.md; sdaf.config.schema.json; scripts/validate-config.py y test-validate-config.py (como referencia); worklog.schema.json; worklogs Iteration-025, 026 y 028; sdaf-pack.schema.json, templates/sdaf-pack.yaml y scripts/validate-pack.py (PR A)"
archivos_modificados: "PR A (#71): sdaf-pack.schema.json, templates/sdaf-pack.yaml, scripts/validate-pack.py, scripts/test-validate-pack.py, scripts/testdata/pack-*.yaml (13 fixtures) y .github/workflows/validate.yml. PR B: docs/contrato-pack-stack.md; docs/iniciativas/INIT-arquitectura.md (plan 0.1.28); docs/iniciativas/README.md; este worklog."
origen_cambios: "Schema, plantilla, validador, test, fixtures y paso de CI (PR A): redacción de un subagente escritor delegado, revisada por el orquestador. Contrato, plan, índice y worklog (PR B): redacción de un subagente escritor delegado, revisada por el orquestador; ver cuerpo."
resultado: "ARQ-4.1 hecho: sdaf-pack.yaml se valida con sdaf-pack.schema.json y scripts/validate-pack.py (#71, fusionado), con plantilla y test con fixtures; el contrato de pack documenta el manifiesto y deja claro que su cruce con la config es de ARQ-4.2 (PR B, en rama local). Sin tag ni release: v0.6.0 es ARQ-4.8."
tiempo: PT30M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "El inicio (2026-11-01T11:57:27+01:00) es aproximado: es la hora del commit del PR A (80be014), el único instante registrado de la serie; el mapeo, el diseño y la escritura previos no se cronometraron. El tiempo es una estimación de trabajo activo de la redacción del PR B y es menor o igual que la diferencia entre fin e inicio. Sin CHANGELOG ni entrada de handbook hasta ARQ-4.8; sdaf.version y los capítulos no cambian. Este worklog no registra el resultado del CI de ningún PR."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (confirmar el commit local; después publicar el PR)
commit: null
pr: null
rama: docs/contrato-manifiesto-pack
sha: null
resumen_acumulado: "ad hoc — ARQ-4.1 manifiesto de pack: #71 fusionado; contrato y plan 0.1.28 en rama local; sin PR de cierre"
---

# INIT-arquitectura / Iteration-029

## Línea de decisión

- Decisiones del humano (2026-11-01, respuestas una a una; la hora exacta no se registró): el `id` del manifiesto es el nombre completo, «Nombre completo: sdaf-stack-<id>», el mismo que se escribe en `stack.pack`; `requires` es una «Lista de objetos {id, version}»; el comprobador es «validate-pack.py + su test + paso en CI». La compatibilidad pack ↔ core la declara el pack en su manifiesto (D-7, cerrada A el 2026-10-02).
- Diseño: el schema (`sdaf-pack.schema.json`, JSON Schema 2020-12, `additionalProperties: false` en cada objeto) valida la **sintaxis** de `id`, `version` (semver estricto), `core` (rango de uno o dos comparadores), `provides` (al menos una lista de ids kebab-case, sin catálogo cerrado de ids de extensión) y `requires` (opcional, objetos `{id, version}` con la versión como rango). `validate-pack.py` añade lo que el schema no expresa: en un rango de dos comparadores el límite inferior es menor que el superior, y un pack no se requiere a sí mismo. La plantilla `templates/sdaf-pack.yaml` usa el pack ficticio `sdaf-stack-example` y no se versiona.
- Entrega en dos PRs: #71 (schema, plantilla, validador, test, fixtures y paso de CI, +642, con `size:exception` declarada; fusionado el 2026-11-01, merge `37bda39`) y el de cierre (contrato, worklog y plan). El humano confirmó el commit y la apertura de #71, y lo fusionó.
- Decisión menor del escritor del PR A, **pendiente de visto bueno del humano**: el rango `>=X.Y.Z <=X.Y.Z` se acepta como versión única (documentado en el docstring de `validate-pack.py`); la lectura estricta (inferior menor que superior) la rechazaría.
- Contrato de pack: nueva sección «Manifiesto» con los campos, un ejemplo mínimo que remite a la plantilla, la relación con `stack.pack` y cómo ejecutar el validador. La identidad y las obligaciones del contrato remiten al manifiesto. Su ausencia es un aviso durante `0.6.x` (ADR-007, Consecuencias), no un error.
- Límite conocido, dicho en el contrato: hoy el validador solo comprueba el manifiesto aislado. No cruza el manifiesto con la config: la coincidencia de `id` y `version` con la referencia de `stack.pack`, la comparación de `core` con `sdaf.version`, las colisiones de ids, el contraste de `extension_ids` con el catálogo del core y el aviso por manifiesto ausente son de ARQ-4.2 y no existen todavía.
- Aviso para ARQ-4.2: `sdaf.config.schema.json` usa patrones con `$` (p. ej. `sdaf.version`) y `validate-config.py` acepta hoy `sdaf.version` con un salto de línea final (observado en este PR con un bloque literal `|` en un directorio temporal, salida `OK`). Es el mismo agujero que se cerró en `validate-pack.py`; no se corrige aquí.
- Fuera de alcance, sin tocar: `stack.packs` y alias, `sdaf.config.schema.*` y `validate-config.py` (ARQ-4.2); overlay (4.3); materialización (4.4); `stack.units` (4.5); examples 09 y 10 (4.6); repo del pack de referencia (4.7); release `v0.6.0` (4.8). Con ARQ-4.1 hecho son 26 de 34 PBIs; H-5 sigue abierto hasta `v0.6.0`. Siguen abiertas las decisiones J y K.

## Pruebas

- TDD en #71: RED por ausencia del validador observado antes de implementar; GREEN con 56 casos. 8 mutaciones detectadas por `test-validate-pack.py`.
- Hallazgo del orquestador en la revisión de #71: un bloque literal YAML (`version: |`) producía `0.1.0` con salto final y el schema lo aceptaba, porque `$` de Python admite un salto de línea final. RED con 4 casos (`id`, `version`, `core` y `requires[].version`) observado; arreglo en `validate-pack.py` (`edge_issue`, que rechaza espacios y saltos en los extremos); GREEN con 60 casos. El arreglo está en el validador: evaluado con un motor que interprete `$` como Python, el schema por sí solo sigue admitiendo el salto final.
- Checks del repo sobre la rama de cierre: `check-version-metadata.py`, `check-history-append-only.py`, `check-adrs.py`, `test-adrs.py`, `test-dates.py`, `test-docs.py`, `test-gate0.py`, `test-worklog.py`, `test-validate-config.py`, `test-validate-pack.py`, `validate-pack.py` (plantilla), `validate-config.py`, `validate-examples.py`, `measure-handbook-scaffolding.py`, `validate-worklog.py` (Iteration-029) y `check-local-links.py --strict-anchors --strict-orphans` sobre copia limpia. markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| sdaf-pack.schema.json, templates/sdaf-pack.yaml | IA, redacción revisada | Subagente escritor (#71) |
| scripts/validate-pack.py, scripts/test-validate-pack.py, scripts/testdata/pack-*.yaml | IA, redacción revisada | Subagente escritor (#71); arreglo de los saltos finales por el orquestador |
| docs/contrato-pack-stack.md | IA, redacción revisada | Subagente escritor; sección «Manifiesto» |
| docs/iniciativas/INIT-arquitectura.md, docs/iniciativas/README.md | IA, redacción revisada | Subagente escritor; plan 0.1.28 e índice |
