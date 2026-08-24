---
name: spec-draft-pbi
description: Redacta o actualiza specs Draft (DOM/APP/ACC), índices y backlog sin auto-aprobar. Usar al derivar knowledge a specs o abrir un PBI en Specification.
---

# spec-draft-pbi

| Campo | Valor |
|--------|--------|
| ID | spec-draft-pbi |
| Versión | 0.1.1 |
| Estado | Approved |
| Prioridad | media |
| Fecha | 2026-08-24 |
| Norma | [handbook/08](../../handbook/08-specification-standard.md) |

## Disparadores

- Draft SPEC-DOM / SPEC-APP / SPEC-ACC; actualizar índices; PBI Ready pendiente de aprobación humana.

## Pasos

1. Leer knowledge citado y specs relacionadas Approved (no contradecir sin enmienda explícita).
2. Usar [templates/spec.md](../../templates/spec.md) / H08: contexto, alcance, acceptance, Out.
3. Estado **Draft**; versionar según H08.
4. Actualizar índices en `specs/**` y enlace en `backlog/` (no fingir Approved).
5. Worklog Specification + `spec-draft-pbi@0.1.1`.
6. Siguiente agente: **humano** (aprobación) o Architecture si falta ADR.

## Definition of Done

- [ ] Specs Draft coherentes y enlazadas.
- [ ] Acceptance testeable (Dado/Cuando/Entonces o equivalente).
- [ ] Sin auto-Approved.

## Restricciones

- No implementar código de producto desde esta skill.
- No inventar alcance Out del MVP del consumidor.

## Referencias

- [prompts/agents/specification-agent.md](../../prompts/agents/specification-agent.md)
- [templates/spec.md](../../templates/spec.md)
