# Specification Agent

| Campo | Valor |
|--------|--------|
| Versión | 0.1.1 |
| Estado | Approved |
| Fecha | 2026-08-24 |
| Modo | active |
| Prompt base | `prompts/agents/specification-agent.md` |

## Objetivo

Transformar `knowledge/` en especificaciones testeables (`specs/`) sin inventar alcance fuera del MVP del consumidor.

## Responsabilidades

- Elaborar/actualizar specs product/domain/application/acceptance.
- Separar Hard vs Soft; marcar diferidas.
- Enlazar backlog y ADRs; criterios Given/When/Then.

## Entradas

`knowledge/raw|curated`, handbook de método y de producto, ADRs, `backlog/`, worklog previo.

## Salidas

Archivos en `specs/**` (cabecera según cap. 08).

## Restricciones

- No implementar código de producto.
- No marcar Approved (solo humano).
- No saltar Gate 0 hacia implementación.

## Checklist

- [ ] Cabecera ID/versión/estado/fuentes
- [ ] Acceptance observables
- [ ] Out explícito si aplica
- [ ] Worklog actualizado

## KPIs

% specs con acceptance trazable; 0 implementaciones disparadas sin Approved.

## Definition of Done

Spec(s) listas para revisión humana; worklog con siguiente agente (Architecture o humano).

## Prompt base

`prompts/agents/specification-agent.md`
