---
name: sdaf-worklog-handoff
description: Cierra o inicia iteraciones ATF y handoffs entre agentes con plantilla de worklog. Usar al cerrar iteración, cambiar de agente o registrar evidencia.
---

# sdaf-worklog-handoff

| Campo | Valor |
|--------|--------|
| ID | sdaf-worklog-handoff |
| Versión | 0.2.1 |
| Estado | Approved |
| Prioridad | alta |
| Fecha | 2026-09-13 |
| Norma | [handbook/08](../../handbook/08-agent-traceability.md) |

## Disparadores

- Cerrar iteración; “siguiente agente”; handoff canónico.
- Inicio de iteración (junto a `sdaf-gate0`).

## Pasos

1. Ruta: `worklogs/<contexto>/Iteration-NNN.md` en el **repo consumidor**.
2. Completar campos mínimos (H08): fecha, agente, modelo, contexto, specs, archivos leídos/modificados, resultado, pruebas, estado, siguiente agente.
3. Recibo de iteración (recomendado en worklogs nuevos): `prompt_id@version` base, prompts adicionales (`ninguno` o ids), `skill-id@version`, reglas IDE, ad hoc (`ninguno` o párrafo en el worklog).
4. Si hubo elección normativa, apartado **Línea de decisión** citando spec/ADR/capítulo § (índice; no volcar el prompt). Si no hubo, `N/A`.
5. El saliente fija **siguiente agente** (o humano).
6. El entrante **lee worklog + specs**; no asume chat no registrado.
7. Estado: `en_curso` | `hecho` | `bloqueado` | `abortado`.
8. No reescribir worklogs históricos para añadir el recibo.

## Definition of Done

- [ ] Worklog existe y es auditable sin el chat.
- [ ] Prompt(s) y skill(s) citados (`id@version`).
- [ ] Recibo / línea de decisión en worklogs nuevos (H08 §4.1–4.2).
- [ ] “Siguiente agente” explícito.

## Restricciones

- Chat no sustituye worklog.
- No purgar worklogs históricos.
- El resumen no sustituye al prompt versionado.

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.2.1 | 2026-09-13 | Recibo ATF y línea de decisión en worklogs nuevos |

## Referencias

- [handbook/08-agent-traceability.md](../../handbook/08-agent-traceability.md)
- [handbook/07-prompt-engineering-standard.md](../../handbook/07-prompt-engineering-standard.md)
- [handbook/A-templates.md](../../handbook/A-templates.md)
- [templates/worklog.md](../../templates/worklog.md)
