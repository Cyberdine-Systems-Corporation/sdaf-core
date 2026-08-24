---
name: adr-propose
description: Propone o enmienda ADRs en Draft con plantilla y consecuencias. Usar cuando el cambio toca límites, stack, motores o estándares.
---

# adr-propose

| Campo | Valor |
|--------|--------|
| ID | adr-propose |
| Versión | 0.1.1 |
| Estado | Approved |
| Prioridad | media |
| Fecha | 2026-08-24 |
| Norma | [handbook/09](../../handbook/09-development-workflow.md) G0.3, `architecture/decisions/` |

## Disparadores

- Nuevo ADR; enmendar ADR existente; G0.3 requiere decisión arquitectónica o de stack.

## Pasos

1. Revisar ADRs vigentes en `architecture/decisions/` del consumidor.
2. Usar [templates/adr.md](../../templates/adr.md): contexto, decisión, alternativas, consecuencias.
3. Estado **Propuesto**; no “Aceptado” sin humano.
4. Actualizar índice `architecture/decisions/README.md` si aplica.
5. Si impacta handbook, proponer enmienda Draft del capítulo (no auto-aprobar).
6. Worklog Architecture + `adr-propose@0.1.1`.

## Definition of Done

- [ ] ADR Propuesto con alternativas y consecuencias.
- [ ] Enlaces a PBI/specs si existen.
- [ ] Índice actualizado.

## Restricciones

- No código de producto salvo spike con excepción documentada.
- No contradecir handbook Approved sin enmienda explícita.
- No imponer un stack en el método; registrarlo como ADR del consumidor.

## Referencias

- [prompts/agents/architecture-agent.md](../../prompts/agents/architecture-agent.md)
- [templates/adr.md](../../templates/adr.md)
