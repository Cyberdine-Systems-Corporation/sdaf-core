---
pbi: INIT-arquitectura
iteracion: Iteration-001
fecha: 2026-09-28
inicio: 2026-09-28T18:08:15+02:00
fin: 2026-09-28T18:11:53+02:00
agente: humano + asistente IA (Claude, chat de claude.ai)
modelo: claude-opus-5-5
version_prompt: "N/D: encargo ad hoc en chat, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc en chat; se siguió el rol de prompts/agents/architecture-agent.md sin cargarlo como prompt base)
prompts_adicionales: ninguno
skills: adr-propose@0.2.0
reglas_ide: idioma-castellano, git-remoto-encargo
ad_hoc: "Encargos del humano en chat: examinar sdaf-core buscando vacíos de arquitectura; después, «haz la planificación completa y déjamelo en artefactos». El plan (PLAN-INIT-arquitectura.md) se entrega fuera del repo hasta la decisión D-5."
contexto: "Auditoría de arquitectura de sdaf-core v0.4.2 (9c90c79) y planificación de la iniciativa que cierra sus diez hallazgos."
especificaciones_utilizadas: "handbook/01-sdaf-framework.md §3, §4 y §6; handbook/03-repository-organization.md §2; handbook/04-specification-standard.md §3–§5; handbook/05-development-workflow.md §3 y §8; handbook/06-ai-agent-framework.md §3 y §7; handbook/08-agent-traceability.md §5 y §6; handbook/10-code-review-and-quality-gates.md §3.2 y §4; handbook/13-enmienda-excepciones-ciclo-de-vida.md §3, §5, §6 y §8; docs/contrato-pack-stack.md; sdaf.config.schema.yaml"
archivos_leidos: "README.md; handbook/00, 01, 02, 03, 04, 05, 06, 08, 10, 13; agents/architecture-agent.md; prompts/agents/architecture-agent.md; prompts/review/architecture-review.md; prompts/system/master-architect.md; skills/adr-propose, sdaf-gate0, sdaf-bootstrap; templates/adr.md, handbook-product.md, worklog.md; architecture/decisions/*.md; docs/contrato-pack-stack.md, adopcion-y-upgrade.md; sdaf.config.schema.yaml y .json; examples/07 y 08; .github/actions/validate-sdaf/action.yml; .github/workflows/validate.yml; scripts/check-adrs.py, check-worklog-presence.py, check-local-links.py; worklog.schema.json; worklogs/INIT-auditoria-v0.3.3/Iteration-001.md"
archivos_modificados: "architecture/decisions/ADR-005-linea-base-arquitectonica.md, ADR-006-ciclo-de-vida-de-adrs.md, ADR-007-modelo-de-capas-y-precedencia.md, ADR-008-adopcion-sobre-codigo-existente.md (nuevos, Propuesto); architecture/decisions/README.md (índice y nota de numeración); este worklog. Fuera del repo: PLAN-INIT-arquitectura.md."
origen_cambios: N/A
resultado: "Diez hallazgos de arquitectura (H-1 a H-10). Cuatro ADRs en estado Propuesto. Plan con nueve decisiones humanas (D-1 a D-9), cuatro releases (v0.4.3, v0.5.0, v0.5.1, v0.6.0) y 34 PBIs en bloques 0–6, con matriz de cobertura, dependencias, validación y riesgos."
tiempo: PT3M38S
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: el chat de claude.ai no expone tokens ni consumo de la conversación; plan de suscripción sin importe por uso"
observaciones: "inicio es la primera lectura de reloj de esta iteración (inicio de la redacción de ADRs y plan); la auditoría del turno anterior no tiene hora medida y no se incluye en tiempo. Las fechas de los ADRs son la misma lectura de reloj. Ningún ADR se marca Aceptado: aceptar es un acto humano (H00 §3.3). Sin commit, rama, PR ni tag: el encargo no los nombra (H06 §7). El número ADR-008 coincide con la cita histórica que equivale a ADR-001; queda como decisión D-4."
pruebas_ejecutadas: "Locales sobre un clon de 9c90c79 con los cambios sin commit: check-adrs.py, check-local-links.py --strict-anchors --strict-orphans, validate-worklog.py sobre este worklog."
estado: hecho
siguiente_agente: humano (revisión del plan y de ADR-005 a 008; decisiones D-1 a D-9)
commit: null
pr: null
rama: null
sha: null
resumen_acumulado: "ad hoc (chat) + adr-propose@0.2.0 — auditoría de arquitectura v0.4.2 → ADR-005 a 008 Propuestos y plan INIT-arquitectura; sin commit/PR/rama/SHA"
---

# INIT-arquitectura / Iteration-001

## Línea de decisión

- ADRs en estado **Propuesto** y sin fila Aceptación: aceptar es un acto humano ([H00 §3.3](../../handbook/00-preface.md), [adr-propose](../../skills/adr-propose/SKILL.md) paso 3).
- Numeración contigua ADR-005 a 008 porque `check-adrs.py` no admite huecos; la coincidencia con la cita histórica «ADR-008» se deja como decisión D-4 y se aclara en el índice ([H13 §8](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md)).
- La línea base exigida por Gate 0 se propone en una línea opt-in `0.5.0` porque cambia un gate de forma incompatible ([H13 §5](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md)).
- La adopción sobre código existente se propone como excepción con caducidad, reutilizando el mecanismo de [H13 §3](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md) en lugar de crear uno nuevo.
- Ninguna norma propuesta nombra estilo, notación, stack ni producto: el core no se estatiza a una adopción.
- El plan queda fuera del repo hasta D-5, con el precedente de la auditoría v0.3.3.
- Este worklog existe porque el cambio es material de ADR ([H08 §5](../../handbook/08-agent-traceability.md)).

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | Redacción IA; decisiones pendientes del humano. |

`commit`, `pr`, `rama` y `sha` quedan en `null`: no hay commit ni rama en esta iteración.
