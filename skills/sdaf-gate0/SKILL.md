---
name: sdaf-gate0
description: Verifica Gate 0 (G0.1–G0.6: specs Approved, acceptance, ADR Aceptado si aplica, backlog, worklog y línea base Approved) antes de implementar producto. Usar al empezar un PBI o al pedir código de feature.
---

# sdaf-gate0

| Campo | Valor |
|--------|--------|
| ID | sdaf-gate0 |
| Versión | 0.4.0 |
| Estado | Approved |
| Prioridad | alta |
| Fecha | 2026-10-18T19:44+02:00 |
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
8. Excepción de adopción ([ADR-008](../../architecture/decisions/ADR-008-adopcion-sobre-codigo-existente.md)): un cambio **correctivo** en una unidad del perímetro heredado, con el ADR de excepción de adopción **Aceptado** y vigente (no caducado), no hace STOP por Gate 0 y exige worklog. Una feature o un cambio de comportamiento en esa unidad pasa antes al perímetro gobernado (Gate 0 completo). Sin ADR Aceptado, o con la excepción caducada, no aplica.
9. Si falta algún ítem y no aplica el paso 8 → **STOP**. Listar gaps; no implementar producto. Ofrecer solo docs/specs/ADR/línea base en Draft.
10. Si todo OK → registrar `sdaf-gate0@0.4.0` en worklog y continuar con el agente de implementación.

> [!CAUTION]
> ⛔ Si falta G0.1–G0.6 (salvo la excepción de adopción del paso 8): **STOP**. No implementar producto.

## Definition of Done

- [ ] Checklist G0.1–G0.6 marcado con evidencias (rutas).
- [ ] STOP documentado si falla; o proceed explícito si pasa.
- [ ] Worklog actualizado.

## Restricciones

- No saltar Gate 0 “por demo”.
- No marcar specs/handbook ni la línea base como Approved.
- Spike técnico solo con ADR de excepción (H05).
- La excepción de adopción cubre solo cambios correctivos en el perímetro heredado ([H05 §3](../../handbook/05-development-workflow.md#3-gate-0-pre-implementación-stop), [H13 §3](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md#3-excepciones-temporales)); en el perímetro gobernado Gate 0 no cambia.

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| ⛔ | [H05 §3](../../handbook/05-development-workflow.md#3-gate-0-pre-implementación-stop) | Checklist G0.1–G0.6 |
| 📖 | [H14](../../handbook/14-architecture-description.md) | Línea base (G0.6) y cuándo un cambio «toca límites» |
| 📖 | [H13 §3](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md#3-excepciones-temporales) | Excepción de adopción: alcance, caducidad y perímetro heredado |
| 🧭 | [AGENTS.md.template](../../AGENTS.md.template) | Router tras el gate |

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.4.0 | 2026-10-18T19:44+02:00 | Perímetro heredado: la excepción de adopción (ADR-008) no hace STOP en cambios correctivos; sin cambio de gates en el perímetro gobernado |
| 0.3.0 | 2026-10-11T23:12+02:00 | G0.6 nuevo (línea base Approved); G0.3 contra H14 §6 con ADR Aceptado; G0.4 con unidades de la línea base; STOP en G0.1–G0.6 |
| 0.2.0 | 2026-08-25 | Fila inicial de historial (cabecera ya publicada) |
