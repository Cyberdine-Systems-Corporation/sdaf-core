---
pbi: INIT-arquitectura
iteracion: Iteration-004
fecha: 2026-10-02
inicio: 2026-10-02T17:26:00+02:00
fin: 2026-10-02T17:30:00+02:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano: «Planifica el desarrollo de la iniciativa de arquitectura»; después «Siguiente paso», que ejecuta la Fase A del plan (bloque 1, v0.4.3)."
contexto: "Bloque 1 de INIT-arquitectura (ARQ-1.1 a 1.4): coherencia de versiones en la documentación publicada, sin cambio de norma."
especificaciones_utilizadas: "docs/iniciativas/INIT-arquitectura.md §2 (H-10) y §5 (bloque 1); handbook/13-enmienda-excepciones-ciclo-de-vida.md §6; handbook/08-agent-traceability.md §5"
archivos_leidos: "docs/iniciativas/INIT-arquitectura.md; architecture/decisions/ADR-005 y ADR-007; .github/workflows/validate.yml; handbook/_meta/05 y 06; handbook/index.yaml; scripts/check-version-metadata.py; commits 581d4ee y 1548074 (proceso de release de v0.4.2)"
archivos_modificados: "README.md; CHANGELOG.md; handbook/CHANGELOG.md; handbook/05-development-workflow.md; handbook/06-ai-agent-framework.md; handbook/_meta/05-development-workflow.yaml; handbook/_meta/06-ai-agent-framework.yaml; handbook/index.yaml; sdaf.config.schema.yaml; sdaf.config.schema.json; sdaf.config.example.yaml; examples/README.md; examples/01-default-core.yaml; examples/08-completo.yaml; skills/README.md; prompts/README.md; docs/adopcion-y-upgrade.md; .gitignore (ignora odd/); este worklog."
origen_cambios: N/A
resultado: "H-10 cerrado en el árbol: README 00–13 y línea 0.4.0; H05 y H06 sin condiciones de versión obsoletas (0.3.4); etiquetas «v0.3» neutralizadas en config, ejemplos y catálogos; entrada 0.4.3 en los CHANGELOG y sección 0.4.3 en adopción y upgrade. Sin cambio de norma."
tiempo: PT4M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "Sin push, rama remota, PR ni tag: el encargo no los nombra (H06 §7). El tag v0.4.3 y el PR de publicación quedan para orden humana. Los scripts de validación necesitan PYTHONUTF8=1 en este equipo (Windows, cp1252); sin eso test-validate-config.py falla por decodificación, no por el cambio."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (revisión; tag v0.4.3 y PR de publicación; decisiones D-1 a D-4 y D-6 a D-9)
commit: null
pr: null
rama: docs/coherencia-versiones-0.4.3
sha: null
resumen_acumulado: "ad hoc — bloque 1 de INIT-arquitectura (v0.4.3) en rama local; sin PR/tag"
---

# INIT-arquitectura / Iteration-004

## Línea de decisión

- Solo el bloque 1 está desbloqueado: no depende de D-1 a D-9 ni de ADR-005 a 008 ([plan §4 y §11](../../docs/iniciativas/INIT-arquitectura.md)).
- Clase **redacción** ([H13 §6](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md)): H05 y H06 suben a `0.3.4` con fila «sin cambio de norma»; `skills/README.md` sube a `0.3.4` por tener cabecera versionada.
- «Solo `es`» en `sdaf.config.schema.yaml` y `examples/README.md` conserva su significado; solo cambia la etiqueta de versión. Registrar el idioma fijo es D-8 / ARQ-3.12.
- El plan omitía `CHANGELOG.md` raíz, el badge y la tabla «Estado» del README, y `.github/actions/validate-sdaf/README.md` en ARQ-1.4; este último se actualiza en el PR de publicación, como en `1548074`.
- `odd/` se ignora en `.gitignore` (seguimiento local de tareas del orquestador): un `.md` no enlazado rompería `check-local-links.py --strict-orphans`.

## Pruebas

`validate-config.py`, `test-validate-config.py`, `test-worklog.py`, `test-dates.py`, `validate-examples.py`, `check-version-metadata.py`, `check-history-append-only.py`, `check-adrs.py`, `measure-handbook-scaffolding.py`, `validate-worklog.py` (Iteration-001 a 004) y `check-local-links.py --strict-anchors --strict-orphans`. `mkdocs build --strict` no se ejecuta: mkdocs no está instalado en este equipo; lo cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | Redacción IA; plan aprobado por el humano. |
