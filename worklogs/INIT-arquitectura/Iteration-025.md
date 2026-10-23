---
pbi: INIT-arquitectura
iteracion: Iteration-025
fecha: 2026-10-21
inicio: 2026-10-21T23:30:00+02:00
fin: 2026-10-24T00:25:00+02:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano en la sesión: ejecutar ARQ-6.3 (modo consumidor de check-adrs.py), fase 1, paso 1 de la secuencia, con el diseño aceptado («Empezamos con el paso 1 de la fase 1», 2026-10-21; «Acepto las proposiciones, adelante», 2026-10-23)."
contexto: "ARQ-6.3 de INIT-arquitectura: modo consumidor de check-adrs.py (formato anterior, corte de heredados por número) y su input opt-in en la action validate-sdaf, con guía para el consumidor."
especificaciones_utilizadas: "ADR-006; handbook/13-enmienda-excepciones-ciclo-de-vida.md §3 y §9; docs/iniciativas/INIT-arquitectura.md (ARQ-6.3 y hallazgo del piloto de 0.5.0)"
archivos_leidos: "scripts/check-adrs.py, scripts/test-adrs.py y scripts/test-dates.py; templates/adr.md; architecture/decisions/ y su índice; .github/actions/validate-sdaf/ (action.yml y README.md); docs/adopcion-y-upgrade.md; skills/sdaf-adopt-existing/SKILL.md; plan de la iniciativa; worklogs Iteration-023 y 024; plantilla de worklog"
archivos_modificados: "scripts/sdaf_adrs.py (nuevo); scripts/check-adrs.py; scripts/test-adrs.py; scripts/testdata/adrs-consumidor-heredado/ (fixture nuevo); .github/actions/validate-sdaf/action.yml y README.md; docs/adopcion-y-upgrade.md; docs/iniciativas/INIT-arquitectura.md (plan 0.1.24); docs/iniciativas/README.md; este worklog."
origen_cambios: "Scripts, pruebas, action y docs: redacción de subagentes escritores delegados, revisada y verificada por el orquestador; ver cuerpo."
resultado: "check-adrs.py gana --consumer y --legacy-up-to N (#58 y #59, fusionados) y la action validate-sdaf gana los inputs check-adrs y adrs-legacy-up-to, desactivados por defecto, con guía en adopcion-y-upgrade.md (PR de cierre, en rama local). Pendiente de publicar como parche junto a ARQ-6.1."
tiempo: PT3H
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "El inicio (23:30 del 2026-10-21) es aproximado. El tiempo es una estimación de trabajo activo repartido en varios días y es menor o igual que la diferencia entre fin e inicio. Sin tag ni Release todavía: se publicará como parche junto a ARQ-6.1, con confirmación aparte. Hallazgos abiertos, no tocados: la skill sdaf-adopt-existing (0.1.1, Approved) sigue citando el índice obligatorio de check-adrs.py en modo core, cierto para el core; mencionar el modo consumidor exigiría 0.1.2 con aprobación humana. validate.yml no usa la action del propio repo: el CI cubre el modo con test-adrs sobre el fixture."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (confirmar el commit local; después publicar el PR)
commit: null
pr: null
rama: feat/action-check-adrs
sha: null
resumen_acumulado: "ad hoc — ARQ-6.3 modo consumidor de check-adrs.py: #58 y #59 fusionados; action y guía en rama local; sin PR/tag"
---

# INIT-arquitectura / Iteration-025

## Línea de decisión

- Decisión del humano («Acepto las proposiciones, adelante», 2026-10-23; la hora exacta no se registró): diseño B. El corte entre ADRs heredados y nuevos es `--legacy-up-to N`, por **número** y no por fecha: una fecha se puede retrodatar y así disfrazar de heredado un ADR nuevo; el número no.
- El modo es opt-in y no cambia el core: sin `--consumer` la salida y el código de salida de `check-adrs.py` son idénticos. La tabla de estados cerrada y fija se aplica solo a heredados; los ADRs nuevos conservan las reglas del core y solo se relajan en formato (ancho de número del consumidor, huecos, índice por nombre de columna). Sin ADR nuevo ni cambio de H13.
- La action fuerza `--consumer` con el input `check-adrs` y lo deja desactivado por defecto (`adrs-legacy-up-to` a 0): con los valores por defecto la action no cambia.
- Entrega en tres PRs: #58 (refactor, 167 líneas, merge `5d7d1d3`), #59 (modo consumidor, 579 líneas con `size:exception` declarada en la descripción porque el repo no tiene etiqueta `size:*`; 197 son pruebas y fixture y unas 45, docstring; merge `65a0900`) y el de cierre (action, guía, worklog y plan). El humano confirmó cada commit y la estructura de PRs («Confirmo», «Abre A1», «Confirmo ambas cosas»).
- Decisiones menores del escritor, aceptadas por defecto: una cabecera de índice es reconocible si tiene «Estado» o «Sustituido por»; «sin sucesor» en el índice acepta —, –, -, vacío y N/A solo en modo consumidor; un fichero no UTF-8 se registra como existente con datos vacíos.
- La skill `sdaf-adopt-existing` no se toca (ver `observaciones`). Publicación como parche junto a ARQ-6.1. Con ARQ-6.3 hecho son 24 de 34 PBIs; H-5 y H-6 siguen abiertos y la DoD, en 2 de 6 casillas. Siguen abiertas las decisiones J (autorización sobre el repo externo del pack de referencia, antes de ARQ-4.7) y K.

## Pruebas

- TDD en #59: RED con 16 casos fallando antes de implementar; GREEN con 40 casos en `test-adrs.py` (21 nuevos) y `test-dates.py` en verde. Fixture `adrs-consumidor-heredado`: pasa con `--consumer --legacy-up-to 3` y falla sin `--consumer`.
- Diferencial: en #58, 48 árboles de ADRs comparados antes y después, 0 diferencias en salida y código de salida; en #59, la misma comparación sobre el core, 0 diferencias.
- Protecciones, con pruebas propias del orquestador: con `--legacy-up-to 12`, un ADR-0013 Aceptado con fecha sin hora y sin Aceptación falla y el 0001 heredado pasa; sin `--legacy-up-to` nada es heredado; Propuesto con Aceptación falla siempre, también en heredados.
- Simulación local del paso de la action: corte 3 OK (5 ADRs), código 0; valor vacío = 0 y falla; valor no numérico, código 2.
- Checks del repo: `test-adrs.py`, `test-dates.py`, `check-adrs.py`, `check-version-metadata.py`, `check-history-append-only.py`, `measure-handbook-scaffolding.py`, `validate-config.py`, `validate-examples.py`, `test-validate-config.py`, `validate-worklog.py` (Iteration-001 a 025, ejecutado sobre todos) y `check-local-links.py --strict-anchors --strict-orphans` sobre copia limpia. markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| scripts/sdaf_adrs.py | IA, redacción revisada | Subagente escritor; parseo compartido (#58) |
| scripts/check-adrs.py | IA, redacción revisada | Subagente escritor; modo consumidor (#59) |
| scripts/test-adrs.py | IA, redacción revisada | Subagente escritor; 21 casos nuevos |
| scripts/testdata/adrs-consumidor-heredado/ | IA, redacción revisada | Fixture de heredados y un ADR nuevo estricto |
| .github/actions/validate-sdaf/action.yml y README.md | IA, redacción revisada | Inputs `check-adrs` y `adrs-legacy-up-to` |
| docs/adopcion-y-upgrade.md | IA, redacción revisada | Sección «Validar los ADRs del consumidor» y avisos reescritos |
| docs/iniciativas/INIT-arquitectura.md, docs/iniciativas/README.md | IA | Plan 0.1.24 e índice; estado verificado |
