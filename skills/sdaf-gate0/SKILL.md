---
name: sdaf-gate0
description: Verifica Gate 0 (specs Approved, acceptance, ADR si aplica, backlog, worklog) antes de implementar producto. Usar al empezar un PBI o al pedir código de feature.
---

# sdaf-gate0

| Campo | Valor |
|--------|--------|
| ID | sdaf-gate0 |
| Versión | 0.2.0 |
| Estado | Approved |
| Prioridad | alta |
| Fecha | 2026-08-25 |
| Norma | [handbook/05](../../handbook/05-development-workflow.md) §3 |

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
8. Si todo OK → registrar `sdaf-gate0@0.2.0` en worklog y continuar con el agente de implementación.

> [!CAUTION]
> ⛔ Si falta G0.1–G0.5: **STOP**. No implementar producto.

## Definition of Done

- [ ] Checklist G0.1–G0.5 marcado con evidencias (rutas).
- [ ] STOP documentado si falla; o proceed explícito si pasa.
- [ ] Worklog actualizado.

## Restricciones

- No saltar Gate 0 “por demo”.
- No marcar specs/handbook como Approved.
- Spike técnico solo con ADR de excepción (H05).

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| ⛔ | [H05 §3](../../handbook/05-development-workflow.md#3-gate-0-pre-implementación-stop) | Checklist G0.1–G0.5 |
| 🧭 | [AGENTS.md.template](../../AGENTS.md.template) | Router tras el gate |

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.2.0 | 2026-08-25 | Fila inicial de historial (cabecera ya publicada) |
