---
name: sdaf-worklog-handoff
description: Cierra o inicia iteraciones ATF y handoffs entre agentes con plantilla de worklog. Usar al cerrar iteración, cambiar de agente o registrar evidencia.
---

# sdaf-worklog-handoff

| Campo | Valor |
|--------|--------|
| ID | sdaf-worklog-handoff |
| Versión | 0.1.1 |
| Estado | Approved |
| Prioridad | alta |
| Fecha | 2026-08-24 |
| Norma | [handbook/15](../../handbook/15-agent-traceability.md) |

## Disparadores

- Cerrar iteración; “siguiente agente”; handoff canónico.
- Inicio de iteración (junto a `sdaf-gate0`).

## Pasos

1. Ruta: `worklogs/<contexto>/Iteration-NNN.md` en el **repo consumidor**.
2. Completar campos mínimos (H15): fecha, agente, modelo, contexto, specs, archivos leídos/modificados, resultado, pruebas, estado, siguiente agente.
3. Citar `prompt_id@version` del agente y `skill-id@version` de skills usadas.
4. El saliente fija **siguiente agente** (o humano).
5. El entrante **lee worklog + specs**; no asume chat no registrado.
6. Estado: `en_curso` | `hecho` | `bloqueado` | `abortado`.

## Definition of Done

- [ ] Worklog existe y es auditable sin el chat.
- [ ] Prompt(s) y skill(s) citados.
- [ ] “Siguiente agente” explícito.

## Restricciones

- Chat no sustituye worklog.
- No purgar worklogs históricos.

## Referencias

- [handbook/15-agent-traceability.md](../../handbook/15-agent-traceability.md)
- [handbook/B-templates.md](../../handbook/B-templates.md)
- [templates/worklog.md](../../templates/worklog.md)
