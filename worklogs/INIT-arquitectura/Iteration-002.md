---
pbi: INIT-arquitectura
iteracion: Iteration-002
fecha: 2026-09-29
inicio: 2026-09-29T07:28:43+02:00
fin: 2026-09-29T07:30:02+02:00
agente: humano + asistente IA (Claude, chat de claude.ai)
modelo: claude-opus-5-5
version_prompt: "N/D: encargo ad hoc en chat, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc en chat)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano, git-remoto-encargo
ad_hoc: "Encargo del humano en chat: «Incluye el plan en el repo, en docs/iniciativas». Cierra la decisión D-5 del plan con la opción B."
contexto: "ARQ-0.2: versionar en el repo el plan de INIT-arquitectura, entregado fuera del repo en Iteration-001."
especificaciones_utilizadas: "docs/checklist-pagina-docs.md; docs/mapa-navegacion.md (vocabulario visual); handbook/08-agent-traceability.md §5; handbook/13-enmienda-excepciones-ciclo-de-vida.md §9"
archivos_leidos: "docs/README.md; docs/checklist-pagina-docs.md; docs/mapa-navegacion.md; mkdocs/mkdocs.yml; scripts/check-version-metadata.py"
archivos_modificados: "docs/iniciativas/INIT-arquitectura.md (nuevo, plan 0.1.1); docs/iniciativas/README.md (nuevo, índice); docs/README.md (fila de iniciativas); mkdocs/mkdocs.yml (navegación: ADR-005 a 008 e iniciativas); architecture/decisions/ADR-005, ADR-007 y ADR-008 (enlace al plan en lugar de la cita en texto); este worklog."
origen_cambios: N/A
resultado: "Plan versionado en docs/iniciativas/ con D-5 cerrada (B), ARQ-0.2 hecho, TOC, Relacionado e Historial. Índice de iniciativas enlazado desde el HOWTO y la navegación de MkDocs. ADR-005 a 008 añadidos a la navegación, que no los incluía."
tiempo: PT1M19S
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: el chat de claude.ai no expone tokens ni consumo de la conversación; plan de suscripción sin importe por uso"
observaciones: "Hora medida con el reloj del contenedor en zona Europe/Madrid. La decisión D-5 la dio el humano en el encargo; el asistente la transcribe (H00 §3.3). Iteration-001 no se modifica: su ad_hoc describe correctamente la situación de entonces. Sin commit, rama, PR ni tag: el encargo no los nombra (H06 §7)."
pruebas_ejecutadas: "Locales sobre un clon de 9c90c79 con los cambios sin commit: ver cuerpo."
estado: hecho
siguiente_agente: humano (revisión; decisiones D-1 a D-4 y D-6 a D-9)
commit: null
pr: null
rama: null
sha: null
resumen_acumulado: "ad hoc (chat) — plan INIT-arquitectura 0.1.1 en docs/iniciativas/ (D-5 = B); sin commit/PR/rama/SHA"
---

# INIT-arquitectura / Iteration-002

## Línea de decisión

- D-5 cerrada con la opción B por el humano en el encargo de este turno; el plan registra fecha y quién decide.
- Carpeta `docs/iniciativas/` con índice propio para que cada plan llegue en ≤3 clics desde el README ([checklist de página](../../docs/checklist-pagina-docs.md), punto 3).
- El plan declara su rol (plan de iniciativa, no constitución) con alerta GFM, como pide el checklist (puntos 2 y 16).
- ADR-005 a 008 entran en la navegación de MkDocs, que listaba solo ADR-001 a 004.
- Este worklog existe porque el cambio sigue siendo parte de la iniciativa con ADRs materiales ([H08 §5](../../handbook/08-agent-traceability.md)).

## Pruebas

`check-adrs.py`, `check-local-links.py --strict-anchors --strict-orphans`, `validate-worklog.py` (Iteration-001 y 002), `check-version-metadata.py`, `check-history-append-only.py`, `validate-examples.py` y `mkdocs build --strict`.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | Redacción IA; decisión D-5 humana. |
