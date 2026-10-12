---
pbi: INIT-arquitectura
iteracion: Iteration-009
fecha: 2026-10-07
inicio: 2026-10-07T18:20:00+02:00
fin: 2026-10-07T18:29:00+02:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano: «Continúa con la siguiente funcionalidad completa, sin hacerlo todo a la vez para que pueda revisarlo. Antes de hacer commit local, pide confirmación.»"
contexto: "ARQ-3.3 de INIT-arquitectura (slice S1 de v0.5.0): implementar ADR-006 en la plantilla de ADR y en check-adrs.py."
especificaciones_utilizadas: "architecture/decisions/ADR-006; handbook/13-enmienda-excepciones-ciclo-de-vida.md §3; docs/iniciativas/INIT-arquitectura.md (ARQ-3.3)"
archivos_leidos: "architecture/decisions/ADR-006; scripts/check-adrs.py; scripts/test-dates.py; scripts/sdaf_meta.py; templates/adr.md; architecture/decisions/README.md; .github/workflows/validate.yml; skills/adr-propose/SKILL.md"
archivos_modificados: "scripts/check-adrs.py; templates/adr.md; architecture/decisions/README.md (columna «Sustituido por»); .github/workflows/validate.yml (paso nuevo); scripts/test-adrs.py (nuevo); scripts/testdata/adrs-ciclo-valido/ (fixture nuevo); este worklog."
origen_cambios: "scripts/check-adrs.py, scripts/test-adrs.py y el fixture: redacción de un subagente escritor delegado, revisada por el orquestador."
resultado: "check-adrs.py valida los cinco estados de ADR-006, la reciprocidad Sustituye / Sustituido por, Caducidad en excepciones y la columna del índice. ADR-001 a 008 siguen en verde. test-adrs.py: 19 casos OK."
tiempo: PT9M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "Interpretaciones de ADR-006 que el humano debe confirmar al revisar: (1) la marca de excepción es el campo Tipo = Excepción, con Caducidad obligatoria y prohibida sin él; (2) Rechazado exige una fila Rechazo (fecha con hora y zona y motivo); (3) Sustituido conserva su fila Aceptación; (4) Drivers es opcional porque ADR-001 a 008 no lo tienen. La skill adr-propose no cambia aquí: es ARQ-3.9. La estrategia de entrega de v0.5.0 (decisión A) sigue abierta: nada se publica."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (revisión y confirmación del commit local; decisión A)
commit: null
pr: null
rama: feat/ciclo-de-vida-adrs
sha: null
resumen_acumulado: "ad hoc — S1 / ARQ-3.3 ciclo de vida de ADRs en rama local; sin commit/PR/tag"
---

# INIT-arquitectura / Iteration-009

## Línea de decisión

- ADR-006 define estados, campos y vigencia, pero no fija cómo se reconoce un ADR de excepción ni qué lleva un rechazo. Se implementan las cuatro interpretaciones de `observaciones`, a confirmar por el humano.
- `Drivers` no se exige: ADR-001 a 008 no lo tienen y deben seguir en verde.
- El checker conserva su interfaz (`--root`) y su salida `OK ADRs (N)`; los tests de ADRs de `test-dates.py` no cambian y siguen pasando.
- La columna «Sustituido por» del índice es opcional para el checker, de modo que un consumidor con el índice anterior no falla.
- La plantilla escribe «ADR-006» y «H13 §3» como texto, sin enlaces relativos al core, porque el consumidor la copia.
- Trazabilidad ODD: ruta de implementación delegada (disparador de escritura, 2 o más ficheros no triviales); la verificación la repite el orquestador.

## Pruebas

`check-adrs.py` (8 ADRs), `test-adrs.py` (19 casos), `test-dates.py` (16), `check-version-metadata.py`, `check-history-append-only.py`, `validate-worklog.py` y `check-local-links.py --strict-anchors --strict-orphans` (copia limpia). markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| scripts/check-adrs.py | IA | Subagente escritor; revisado |
| scripts/test-adrs.py | IA | Subagente escritor; 19 casos |
| scripts/testdata/adrs-ciclo-valido/ | IA | Fixture válido de los cinco estados |
| templates/adr.md, architecture/decisions/README.md, .github/workflows/validate.yml | IA | Redacción |
