# ADR-008 — Adopción del método sobre código existente

| Campo | Valor |
|--------|--------|
| Estado | Propuesto |
| Fecha | 2026-09-28T18:08+02:00 |
| Decisores | Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS) |
| Relacionado | [H05](../../handbook/05-development-workflow.md), [H13](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md), [H04](../../handbook/04-specification-standard.md), [ADR-001](ADR-001-nucleo-reutilizable.md), [ADR-005](ADR-005-linea-base-arquitectonica.md), [ADR-006](ADR-006-ciclo-de-vida-de-adrs.md), [worklog](../../worklogs/INIT-arquitectura/Iteration-001.md) |

> [!NOTE]
> Numeración: los historiales publicados hasta `v0.3.3` citan «ADR-008» como origen de la extracción del core; esa cita equivale a [ADR-001](ADR-001-nucleo-reutilizable.md) y no se refiere a este ADR. Reutilizar el número o reservarlo es la decisión D-4 del [plan de la iniciativa](../../docs/iniciativas/INIT-arquitectura.md). `check-adrs.py` exige hoy numeración sin huecos, así que reservarlo implica cambiar el checker.

## Contexto

Todo el flujo del core asume un repo nuevo. Gate 0 prohíbe código de producto sin spec Approved ([H05 §3](../../handbook/05-development-workflow.md)) y H05 §8 prohíbe la spec retroactiva «como hábito». Un equipo con código en producción que quiera adoptar SDAF no tiene un camino conforme:

- no puede escribir specs del comportamiento existente sin que parezcan retroactivas;
- no puede tocar el código existente sin un Gate 0 que ese código nunca tuvo;
- no tiene dónde describir la arquitectura tal como está, ni cómo registrar decisiones tomadas antes de adoptar el método.

## Decisión

1. **Excepción de adopción.** Adoptar SDAF sobre código existente es una excepción temporal ([H13 §3](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md)) registrada como ADR del consumidor, con alcance, caducidad y plan de retorno.
2. **Dos perímetros.**
   - **Gobernado**: Gate 0 completo.
   - **Heredado**: el código existente al adoptar. Admite solo cambios correctivos con worklog. Una feature nueva o un cambio de comportamiento en una unidad heredada la mueve al perímetro gobernado antes de implementar.

   El plan de retorno lista las unidades heredadas; la caducidad obliga a revisarlo.
3. **Línea base descriptiva.** La línea base ([ADR-005](ADR-005-linea-base-arquitectonica.md)) documenta la arquitectura existente tal como es y marca las unidades heredadas. Se aprueba como descripción, no como diseño deseado.
4. **ADRs de reconocimiento.** Las decisiones anteriores a la adopción se registran como ADRs Aceptados con la marca «decisión heredada» en Contexto y `N/A: decisión previa a la adopción` en Alternativas.
5. **Specs de caracterización.** Describen el comportamiento observado, con `Origen: caracterización` en la cabecera ([H04 §4](../../handbook/04-specification-standard.md)) y tests de caracterización. Solo pasan a Approved tras revisión humana que decide si ese comportamiento es el deseado. No son la spec retroactiva que prohíbe H05 §8: aquella justifica código nuevo escrito sin gate; estas describen código anterior a la adopción.
6. **Skill.** Nueva skill `sdaf-adopt-existing` con los pasos: inventario de unidades, línea base descriptiva, ADRs de reconocimiento, excepción de adopción y primer PBI gobernado.

## Alternativas consideradas

- **No admitir adopción sobre código existente.** Limita el método a proyectos nuevos, en contra de la vocación de núcleo reutilizable ([ADR-001](ADR-001-nucleo-reutilizable.md)).
- **Especificar todo el sistema antes de adoptar.** Bloquea la adopción durante meses y produce specs sin revisión real.
- **Tratar el código existente como spike.** El spike es acotado y desechable; el código heredado no lo es.

## Consecuencias

- Cambian H05 (nota de la excepción de adopción), H04 (campo `Origen`), `templates/spec.md`, `templates/adr.md` y `docs/adopcion-y-upgrade.md`; se añade `skills/sdaf-adopt-existing/`.
- Añade un procedimiento opcional sin cambiar gates existentes: no es breaking ([H13 §5](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md)) y puede publicarse como parche de una línea ya adoptada.
- Depende de [ADR-005](ADR-005-linea-base-arquitectonica.md) (unidades) y de [ADR-006](ADR-006-ciclo-de-vida-de-adrs.md) (campo Caducidad).
