---
name: sdaf-gate0
description: Verifica Gate 0 (specs Approved, acceptance, ADR si aplica, backlog, worklog) antes de implementar producto. Usar al empezar un PBI o al pedir código de feature.
---

# sdaf-gate0

| Campo | Valor |
|--------|--------|
| ID | sdaf-gate0 |
| Versión | 0.1.1 |
| Estado | Approved |
| Prioridad | alta |
| Fecha | 2026-08-24 |
| Norma | [handbook/09](../../handbook/09-development-workflow.md) §3 |

## Disparadores

- “Implementar PBI-…”, “empezar feature”, “abrir slice de producto”.
- Cualquier cambio en código de producto (`src/` o ruta de `sdaf.config`) sin Gate 0 cerrado.

## Pasos

1. Identificar PBI en `backlog/` y specs enlazadas.
2. Comprobar **G0.1**: specs aplicables con estado **Approved**.
3. Comprobar **G0.2**: acceptance en `specs/acceptance/` (o sección en spec).
4. Comprobar **G0.3**: ADR si toca límites/stack; si N/A, justificar en worklog.
5. Comprobar **G0.4**: PBI enlazado a specs.
6. Comprobar **G0.5**: worklog de iteración iniciado (`worklogs/...`).
7. Si falta algún ítem → **STOP**. Listar gaps; no implementar producto. Ofrecer solo docs/specs/ADR Draft.
8. Si todo OK → registrar `sdaf-gate0@0.1.1` en worklog y continuar con el agente de implementación.

## Definition of Done

- [ ] Checklist G0.1–G0.5 marcado con evidencias (rutas).
- [ ] STOP documentado si falla; o proceed explícito si pasa.
- [ ] Worklog actualizado.

## Restricciones

- No saltar Gate 0 “por demo”.
- No marcar specs/handbook como Approved.
- Spike técnico solo con ADR de excepción (H9).

## Referencias

- [handbook/09-development-workflow.md](../../handbook/09-development-workflow.md)
- [AGENTS.md.template](../../AGENTS.md.template)
