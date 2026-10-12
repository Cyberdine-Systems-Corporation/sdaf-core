---
name: adr-propose
description: Propone o enmienda ADRs en Draft con plantilla, ciclo de vida y consecuencias. Usar cuando el cambio toca límites, stack, motores o estándares.
---

# adr-propose

| Campo | Valor |
|--------|--------|
| ID | adr-propose |
| Versión | 0.3.0 |
| Estado | Approved |
| Prioridad | media |
| Fecha | 2026-10-11T23:12+02:00 |
| Norma | [handbook/05](../../handbook/05-development-workflow.md) G0.3, [handbook/14](../../handbook/14-architecture-description.md) §6, `architecture/decisions/`, ADR-006 |

## Disparadores

- Nuevo ADR; enmendar ADR existente; G0.3 requiere decisión arquitectónica o de stack.

## Pasos

1. Revisar los ADRs **vigentes** en `architecture/decisions/` del consumidor: Aceptados y sin «Sustituido por» (ADR-006 §4). Leer también `architecture/description.md`.
2. Usar [templates/adr.md](../../templates/adr.md): contexto, decisión, alternativas, consecuencias. Rellenar `Drivers` (specs, atributos de calidad o capítulos que lo motivan; `N/A` si no hay). Solo en excepciones, `Tipo = Excepción` con `Caducidad`.
3. Estado **Propuesto**. Los estados son Propuesto, Aceptado, Rechazado, Sustituido y Deprecado; ningún agente marca Aceptado, Rechazado ni Sustituido (ADR-006 §1): es un acto humano.
4. Si el ADR sustituye a otro, rellenar `Sustituye` con el ADR anterior y proponer el `Sustituido por` recíproco en este; ambos extremos deben coincidir. No editar un ADR Aceptado para cambiar la decisión: se crea un ADR nuevo que lo sustituya (ADR-006 §3).
5. Actualizar índice `architecture/decisions/README.md` si aplica.
6. Si el ADR cambia unidades, reglas de dependencia, integraciones o la prioridad de un atributo de calidad ([H14 §6](../../handbook/14-architecture-description.md)), proponer una **versión nueva en Draft** de la línea base y actualizar su sección 6 (decisiones vigentes). La aprueba un humano.
7. Si impacta handbook, proponer enmienda Draft del capítulo (no auto-aprobar).
8. Worklog Architecture + `adr-propose@0.3.0`.

## Definition of Done

- [ ] ADR Propuesto con alternativas y consecuencias.
- [ ] `Drivers` rellenado; `Sustituye` / `Sustituido por` recíprocos si hay sustitución.
- [ ] Enlaces a PBI/specs si existen.
- [ ] Índice actualizado.
- [ ] Línea base nueva en Draft propuesta si el cambio es de H14 §6.

## Restricciones

- No código de producto salvo spike con excepción documentada.
- No contradecir handbook Approved sin enmienda explícita.
- No imponer un stack en el método; registrarlo como ADR del consumidor.
- No marcar Aceptado, Rechazado ni Sustituido; no aprobar la línea base.

## Relacionado

| Destino | Por qué |
|---------|---------|
| [architecture-agent](../../prompts/agents/architecture-agent.md) | Prompt del rol |
| [templates/adr.md](../../templates/adr.md) | Plantilla ADR |
| [H14](../../handbook/14-architecture-description.md) | Línea base y cuándo cambia |

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.3.0 | 2026-10-11T23:12+02:00 | Estados y campos de ADR-006 (sustitución recíproca, Drivers, excepciones); vigentes = Aceptados sin «Sustituido por»; propone línea base nueva en Draft cuando el ADR es de H14 §6 |
| 0.2.0 | 2026-08-25 | Fila inicial de historial (cabecera ya publicada) |
