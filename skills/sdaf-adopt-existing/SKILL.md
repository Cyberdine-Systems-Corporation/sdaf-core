---
name: sdaf-adopt-existing
description: Adopta SDAF sobre un repo con código existente (inventario de unidades, línea base descriptiva, ADRs de reconocimiento, excepción de adopción y primer PBI gobernado). Usar al incorporar el método a un repo que ya tiene código previo.
---

# sdaf-adopt-existing

| Campo | Valor |
|--------|--------|
| ID | sdaf-adopt-existing |
| Versión | 0.1.1 |
| Estado | Approved |
| Prioridad | media |
| Fecha | 2026-10-18T20:14+02:00 |
| Norma | [ADR-008](../../architecture/decisions/ADR-008-adopcion-sobre-codigo-existente.md), [H05 §3](../../handbook/05-development-workflow.md), [H13 §3](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md#3-excepciones-temporales), [H04 §4](../../handbook/04-specification-standard.md#4-cabecera-obligatoria), [H14](../../handbook/14-architecture-description.md) |

## Disparadores

- “Adoptar SDAF sobre código existente”, “repo con código previo”, “excepción de adopción”.
- Precondiciones: `sdaf-bootstrap` ejecutado (existen `sdaf.config.yaml` y el árbol); el repo adopta la línea `0.5.0` (opt-in; la línea base y G0.6 son de esa línea); hay un humano que aceptará los ADRs y aprobará la línea base. Si falta alguna, parar y pedirla.

## Pasos

Citar `sdaf-adopt-existing@0.1.1` una sola vez, en el campo `skills` del worklog de adopción.

1. Inventariar las unidades del código existente con nombres estables (el tipo de unidad es libre), proponer cuáles quedan en el perímetro heredado y registrar el inventario en la sección «Inventario» del worklog.
2. Rellenar `architecture/description.md` (la crea bootstrap; si no existe, crearla desde [`templates/architecture-description.md`](../../templates/architecture-description.md)) como línea base descriptiva en Draft: documenta lo existente tal como es, marca «heredada» las unidades heredadas y recoge las dependencias observadas o `N/A`, sin inventar reglas normativas de «permitida/prohibida». Se aprueba como descripción, no como diseño deseado.
3. Proponer un ADR de reconocimiento por decisión previa a la adopción, en Propuesto, desde [`templates/adr.md`](../../templates/adr.md): «Decisión heredada» al empezar Contexto y `N/A: decisión previa a la adopción` en Alternativas. Crear o actualizar `architecture/decisions/README.md` (índice) con cada ADR en Propuesto: `check-adrs.py` falla si falta.
4. Proponer el ADR de excepción de adopción, en Propuesto: `Tipo | Excepción`; alcance = Gate 0 y spec retroactiva, solo en el perímetro heredado; `Caducidad | <fecha con hora y zona> (PROPUESTA; la fija el humano al aceptar)`; plan de retorno que lista las unidades heredadas. Nombres `ADR-NNN-slug.md` contiguos: reconocimiento primero y la excepción al final.
5. Abrir el primer PBI gobernado con [`templates/pbi.md`](../../templates/pbi.md), en Draft, con `Specs` y `Acceptance` pendientes (p. ej. «pendiente: spec de la feature en Draft»), y redactar la spec de la feature en Draft; los enlaces a specs Approved llegan cuando un humano las apruebe. Si procede, describir el comportamiento existente en `specs/` con specs de caracterización en Draft y `Origen: caracterización` ([H04 §4](../../handbook/04-specification-standard.md#4-cabecera-obligatoria)); sus tests de caracterización quedan pendientes o van en `tests/` con worklog.
6. Ejecutar el checklist Gate 0 → **STOP** esperado en G0.1, G0.2, G0.4 y G0.6 (línea base en Draft, sin specs Approved ni acceptance); G0.3 solo si el PBI toca límites ([H05 §3](../../handbook/05-development-workflow.md), [H14 §6](../../handbook/14-architecture-description.md)). Registrar cada motivo en el worklog.

## Definition of Done

- [ ] Inventario, línea base descriptiva, ADRs de reconocimiento y ADR de excepción creados, todos en Draft o Propuesto, con el índice de ADRs al día.
- [ ] El recorrido termina en el STOP esperado de Gate 0 (G0.1, G0.2, G0.4, G0.6; G0.3 si el PBI toca límites). Orden humano: aceptar los ADRs, luego aprobar la línea base completando su sección de decisiones vigentes.
- [ ] Aceptar el ADR de excepción legitima solo los cambios correctivos en el perímetro heredado: no desbloquea Gate 0 en el perímetro gobernado (lo hacen specs Approved con acceptance y la línea base Approved).
- [ ] Nada del perímetro heredado tocado salvo cambios correctivos con worklog.
- [ ] Worklog con los motivos del STOP y `sdaf-adopt-existing@0.1.1` en `skills`.

## Restricciones

- No aceptar ADRs ni aprobar la línea base, las specs ni el PBI.
- No fijar la caducidad de la excepción: solo proponerla.
- No crear un tipo nuevo de ADR: la excepción es `Tipo | Excepción`.
- No tratar el código existente como spike: no es acotado ni desechable.
- No escribir spec retroactiva de código nuevo ([H05 §8](../../handbook/05-development-workflow.md#8-violaciones)).
- No commit ni escritura al remoto sin petición **en este turno** (H06 §7).

## Relacionado

| Destino | Por qué |
|---------|---------|
| [docs/adopcion-y-upgrade.md](../../docs/adopcion-y-upgrade.md) | Guía de adopción sobre un repo con código |
| [sdaf-bootstrap](../sdaf-bootstrap/SKILL.md) | Árbol y config previos |
| [sdaf-gate0](../sdaf-gate0/SKILL.md) | STOP esperado al final |

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.1.1 | 2026-10-18T20:14+02:00 | Approved (aprobación humana de Manuel Ortiz de Villajos Quirós, CODEOWNERS; el agente transcribe la aprobación dada en el encargo, H00 §3.3) |
| 0.1.0 | 2026-10-13T15:59+02:00 | Primera versión (ADR-008); Draft, pendiente de aprobación humana |
