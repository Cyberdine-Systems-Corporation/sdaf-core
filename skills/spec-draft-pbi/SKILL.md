---
name: spec-draft-pbi
description: Redacta o actualiza specs Draft (DOM/APP/ACC), índices y backlog sin auto-aprobar. Usar al derivar knowledge a specs o abrir un PBI en Specification.
---

# spec-draft-pbi

| Campo | Valor |
|--------|--------|
| ID | spec-draft-pbi |
| Versión | 0.3.0 |
| Estado | Approved |
| Prioridad | media |
| Fecha | 2026-10-08T23:07+02:00 |
| Norma | [handbook/04](../../handbook/04-specification-standard.md) |

## Disparadores

- Draft SPEC-DOM / SPEC-APP / SPEC-ACC; actualizar índices; PBI Ready pendiente de aprobación humana.

## Pasos

1. Leer knowledge citado y specs relacionadas Approved (no contradecir sin enmienda explícita).
2. Usar [templates/spec.md](../../templates/spec.md) / H04: contexto, alcance, acceptance, Out.
3. Estado **Draft**; versionar según H04.
4. Actualizar índices en `specs/**` y crear o actualizar el PBI en `backlog/` con [templates/pbi.md](../../templates/pbi.md): enlaza las specs (no fingir Approved) y su acceptance, y rellena **Unidades** con los nombres de la línea base ([H14](../../handbook/14-architecture-description.md)).
5. Worklog Specification + `spec-draft-pbi@0.3.0`.
6. Siguiente agente: **humano** (aprobación) o Architecture si falta ADR.

## Definition of Done

- [ ] Specs Draft coherentes y enlazadas.
- [ ] Acceptance testeable (Dado/Cuando/Entonces o equivalente).
- [ ] Sin auto-Approved.

## Restricciones

- No implementar código de producto desde esta skill.
- No inventar alcance Out del MVP del consumidor.

## Relacionado

| Destino | Por qué |
|---------|---------|
| [specification-agent](../../prompts/agents/specification-agent.md) | Prompt del rol |
| [templates/spec.md](../../templates/spec.md) | Cabecera de spec |
| [templates/pbi.md](../../templates/pbi.md) | Plantilla de PBI (G0.4) |

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.3.0 | 2026-10-08T23:07+02:00 | G0.4 comprobable: el PBI usa `templates/pbi.md` y declara las unidades de la línea base |
| 0.2.0 | 2026-08-25 | Fila inicial de historial (cabecera ya publicada) |
