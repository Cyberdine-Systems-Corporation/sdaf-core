---
name: sdaf-gate0
description: Verifica Gate 0 (G0.1–G0.6: specs Approved, acceptance, ADR Aceptado si aplica, backlog, worklog y línea base Approved) antes de implementar producto. Usar al empezar un PBI o al pedir código de feature.
---

# sdaf-gate0

| Campo | Valor |
|--------|--------|
| ID | sdaf-gate0 |
| Versión | 0.3.0 |
| Estado | Approved |
| Prioridad | alta |
| Fecha | 2026-10-11T23:12+02:00 |
| Norma | [handbook/05](../../handbook/05-development-workflow.md) §3, [handbook/14](../../handbook/14-architecture-description.md) §7 |

## Disparadores

- “Implementar PBI-…”, “empezar feature”, “abrir slice de producto”.
- Cualquier cambio en código de producto (`src/` o ruta de `sdaf.config`) sin Gate 0 cerrado.

## Pasos

1. Identificar PBI en `backlog/` y specs enlazadas.
2. Comprobar **G0.1**: specs aplicables con estado **Approved**.
3. Comprobar **G0.2**: acceptance en `specs/acceptance/` (o sección en spec).
4. Comprobar **G0.3**: si el cambio produce alguno de los cambios de [H14 §6](../../handbook/14-architecture-description.md) (añadir, retirar o renombrar una unidad; cambiar una regla de dependencia, una integración o la prioridad de un atributo de calidad), o toca stack o motores, exige ADR **Aceptado**; si N/A, justificar en worklog.
5. Comprobar **G0.4**: PBI en `backlog/` enlazado a specs Approved, con su acceptance y unidades que existan en la línea base.
6. Comprobar **G0.5**: worklog de iteración iniciado (`worklogs/...`).
7. Comprobar **G0.6**: leer `architecture/description.md`; debe existir y tener estado **Approved**. Si falta o es Draft → no se satisface.
8. Si falta algún ítem → **STOP**. Listar gaps; no implementar producto. Ofrecer solo docs/specs/ADR/línea base en Draft.
9. Si todo OK → registrar `sdaf-gate0@0.3.0` en worklog y continuar con el agente de implementación.

> [!CAUTION]
> ⛔ Si falta G0.1–G0.6: **STOP**. No implementar producto.

## Definition of Done

- [ ] Checklist G0.1–G0.6 marcado con evidencias (rutas).
- [ ] STOP documentado si falla; o proceed explícito si pasa.
- [ ] Worklog actualizado.

## Restricciones

- No saltar Gate 0 “por demo”.
- No marcar specs/handbook ni la línea base como Approved.
- Spike técnico solo con ADR de excepción (H05).

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| ⛔ | [H05 §3](../../handbook/05-development-workflow.md#3-gate-0-pre-implementación-stop) | Checklist G0.1–G0.6 |
| 📖 | [H14](../../handbook/14-architecture-description.md) | Línea base (G0.6) y cuándo un cambio «toca límites» |
| 🧭 | [AGENTS.md.template](../../AGENTS.md.template) | Router tras el gate |

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.3.0 | 2026-10-11T23:12+02:00 | G0.6 nuevo (línea base Approved); G0.3 contra H14 §6 con ADR Aceptado; G0.4 con unidades de la línea base; STOP en G0.1–G0.6 |
| 0.2.0 | 2026-08-25 | Fila inicial de historial (cabecera ya publicada) |
