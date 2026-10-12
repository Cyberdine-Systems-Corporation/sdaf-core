---
pbi: INIT-arquitectura
iteracion: Iteration-010
fecha: 2026-10-07
inicio: 2026-10-07T18:35:00+02:00
fin: 2026-10-07T18:41:00+02:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: chained-pr
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano: «Proponme la elección de estrategias de entrega» y después «La apruebo» (cadena sobre rama de feature, auto-chain, size:exception en S1)."
contexto: "Estrategia de entrega de v0.5.0 (decisión A del plan): cómo se publica el bloque 3 sin superar el presupuesto de 400 líneas por PR."
especificaciones_utilizadas: "docs/iniciativas/INIT-arquitectura.md §4 y §5; skill chained-pr y su referencia chaining-details"
archivos_leidos: "docs/iniciativas/INIT-arquitectura.md; skill chained-pr; git diff de la rama feat/ciclo-de-vida-adrs (tamaño de S1)"
archivos_modificados: "docs/iniciativas/INIT-arquitectura.md (plan 0.1.7, §4 y §11); docs/iniciativas/README.md; este worklog."
origen_cambios: N/A
resultado: "Decisión A cerrada: auto-chain con feature-branch-chain, tracker feat/linea-0.5.0, slices S1 a S6 (S4 en dos PRs) y size:exception aceptada para S1 (574 líneas). Registrada en el plan."
tiempo: PT6M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "Las estimaciones de líneas de S2 a S6 son de planificación, no medidas; S1 sí está medida (533 añadidas y 41 borradas). GitHub no admite un PR sin diferencias respecto a main, por eso el primer commit del tracker es este registro de la decisión; la rama de S1 se rebasa sobre el tracker (solo local, sin publicar). La decisión autoriza la estrategia; el push y los PRs siguen requiriendo confirmación expresa en cada paso."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (confirmar el commit local del tracker; después publicar tracker y S1)
commit: null
pr: null
rama: feat/linea-0.5.0
sha: null
resumen_acumulado: "ad hoc — decisión A (estrategia de entrega de v0.5.0) registrada en el plan; rama tracker local"
---

# INIT-arquitectura / Iteration-010

## Línea de decisión

- Decisor: Manuel Ortiz de Villajos Quirós (CODEOWNERS), 2026-10-07T18:41+02:00, tras la propuesta del asistente. Transcrita; no autodeclarada.
- Estrategia: `auto-chain` con `feature-branch-chain`. Razón: los slices normativos se citan entre sí (H14 y G0.6) y no pueden aterrizar solos en `main`.
- S1 con `size:exception`: 574 líneas cambiadas, 393 sin fixtures, worklog ni plan; no hay un corte coherente bajo 400 sin separar tests y código.
- S4 se divide en S4a (ARQ-3.7 y 3.8) y S4b (ARQ-3.6 y 3.9) por quedar al límite del presupuesto.

## Pruebas

`check-version-metadata.py`, `check-history-append-only.py`, `check-adrs.py`, `validate-worklog.py` (Iteration-001 a 008 y 010) y `check-local-links.py --strict-anchors --strict-orphans` (copia limpia). markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | Redacción IA; decisión del humano. |
