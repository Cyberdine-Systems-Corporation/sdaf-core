---
pbi: INIT-arquitectura
iteracion: Iteration-005
fecha: 2026-10-02
inicio: 2026-10-02T18:01:00+02:00
fin: 2026-10-02T18:03:00+02:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano: «Acepto las recomendaciones propuestas» (D-1 a D-4 y D-6 a D-9), tras ver el resumen de decisiones."
contexto: "ARQ-0.1 de INIT-arquitectura: cerrar las decisiones humanas D-1 a D-9 y registrarlas en el plan."
especificaciones_utilizadas: "docs/iniciativas/INIT-arquitectura.md §3, §5 (ARQ-0.1) y §10; architecture/decisions/ADR-005 a ADR-008"
archivos_leidos: "docs/iniciativas/INIT-arquitectura.md; docs/iniciativas/README.md; worklogs/INIT-arquitectura/Iteration-004.md"
archivos_modificados: "docs/iniciativas/INIT-arquitectura.md (plan 0.1.3); docs/iniciativas/README.md (enlaces a Iteration-004 y 005); este worklog."
origen_cambios: N/A
resultado: "D-1 a D-9 cerradas con la opción recomendada del plan y registradas con fecha, hora, zona y decisor. ADR-005 a 008 siguen Propuestos: ningún agente los acepta (H00 §3.3)."
tiempo: PT2M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "Decisiones transcritas del chat, no autodeclaradas por el agente. Sin push, rama remota, PR ni tag: el encargo no los nombra (H06 §7). El texto de ADR-005 y ADR-007 sigue diciendo «pendiente de la decisión D-n»: se actualiza al aceptarlos (ARQ-2.1), porque tocar un ADR Propuesto aquí sería otro cambio."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (revisión de ADR-005 a 008 y aceptación o rechazo, ARQ-2.1)
commit: null
pr: null
rama: docs/cerrar-decisiones-d1-d9
sha: null
resumen_acumulado: "ad hoc — D-1 a D-9 cerradas (ARQ-0.1) en rama local; sin PR/tag"
---

# INIT-arquitectura / Iteration-005

## Línea de decisión

Todas las decisiones eligen la opción recomendada del plan. Decisor: Manuel Ortiz de Villajos Quirós (CODEOWNERS), 2026-10-02T18:02+02:00, transcrita del chat.

| ID | Opción elegida | Desbloquea |
|----|----------------|------------|
| D-1 | A) G0.6 en línea nueva opt-in `0.5.0` | Bloque 3 |
| D-2 | A) `architecture/description.md` (B permitido si crece) | ARQ-3.1, 3.2, 3.4 |
| D-3 | C) Mismo nivel por materia; conflicto = STOP y enmienda (ADR-007 §2) | ARQ-3.7 |
| D-4 | A) Reutilizar 008 con nota en el índice | ARQ-2.1 |
| D-6 | A) `stack.packs` con `stack.pack` como alias obsoleto | ARQ-4.2 |
| D-7 | A) El pack declara la compatibilidad en su manifiesto | ARQ-4.1 |
| D-8 | A) Mantener `es` y registrarlo como decisión explícita | ARQ-3.12 |
| D-9 | A) Capítulo nuevo H14 «Descripción de arquitectura» | ARQ-3.1 |

- Cerrar una decisión no acepta ningún ADR: ADR-005 a 008 siguen Propuestos hasta que un humano los acepte o rechace ([plan §5, ARQ-2.1](../../docs/iniciativas/INIT-arquitectura.md)).
- Con D-1, D-2, D-3 y D-9 cerradas, lo único que bloquea `v0.5.0` es la aceptación de ADR-005, ADR-006 y ADR-007 §2.
- El plan sube a `0.1.3`; el DoD marca D-1 a D-9 como cerradas y el siguiente paso apunta a ARQ-2.1.

## Pruebas

`check-adrs.py`, `check-version-metadata.py`, `check-history-append-only.py`, `validate-worklog.py` (Iteration-001 a 005) y `check-local-links.py --strict-anchors --strict-orphans` (copia limpia). `mkdocs build --strict` y markdownlint los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | Redacción IA; decisiones del humano. |
