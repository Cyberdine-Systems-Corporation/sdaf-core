---
name: sdaf-worklog-handoff
description: Cierra o inicia iteraciones ATF y handoffs entre agentes con plantilla de worklog. Usar al cerrar iteración, cambiar de agente o registrar evidencia.
---

# sdaf-worklog-handoff

| Campo | Valor |
|--------|--------|
| ID | sdaf-worklog-handoff |
| Versión | 0.4.0 |
| Estado | Approved |
| Prioridad | alta |
| Fecha | 2026-09-24T18:54+02:00 |
| Norma | [handbook/08](../../handbook/08-agent-traceability.md) |

## Disparadores

- Cerrar iteración; “siguiente agente”; handoff canónico.
- Inicio de iteración (junto a `sdaf-gate0`).

## Pasos

1. Ruta: `worklogs/<contexto>/Iteration-NNN.md` en el **repo consumidor**.
2. Completar campos mínimos (H08): en worklogs **nuevos**, frontmatter de [`templates/worklog.md`](../../templates/worklog.md) (incl. `inicio`/`fin` con hora y zona, `tiempo` y `coste` medidos o `N/D: <motivo>`, `commit`/`pr`/`rama`/`sha` o `null`, y `resumen_acumulado`). La tabla markdown vigente sigue válida.
3. Recibo de iteración (recomendado en worklogs nuevos): `prompt_id@version` base, prompts adicionales (`ninguno` o ids), `skill-id@version`, reglas IDE, ad hoc (`ninguno` o párrafo en el worklog).
4. Si hubo elección normativa, apartado **Línea de decisión** citando spec/ADR/capítulo § (índice; no volcar el prompt). Si no hubo, `N/A`.
5. Si la iteración toca código de producto: **Origen de cambios** por archivo (`humano` / `ia` / `mixto` / `dependencia`) o tabla resumen (H08 §4.3). Si no toca código: `N/A`. No backfill de worklogs anteriores.
6. El saliente fija **siguiente agente** (o humano).
7. El entrante **lee worklog + specs**; no asume chat no registrado.
8. Estado: `en_curso` | `hecho` | `bloqueado` | `abortado`.
9. No reescribir worklogs históricos para añadir el recibo ni el origen.

## Definition of Done

- [ ] Worklog existe y es auditable sin el chat.
- [ ] Prompt(s) y skill(s) citados (`id@version`).
- [ ] Recibo / línea de decisión en worklogs nuevos (H08 §4.1–4.2).
- [ ] Origen de cambios si hay código de producto (H08 §4.3).
- [ ] “Siguiente agente” explícito.

## Restricciones

- Chat no sustituye worklog.
- No purgar worklogs históricos.
- El resumen no sustituye al prompt versionado.

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.4.0 | 2026-09-24T18:54+02:00 | Frontmatter y cadena commit/PR/rama/SHA; tabla vigente sin backfill |
| 0.3.2 | 2026-09-19 | Origen de cambios (H08 §4.3) en worklogs nuevos de código de producto |
| 0.2.1 | 2026-09-13 | Recibo ATF y línea de decisión en worklogs nuevos |

## Relacionado

| Destino | Por qué |
|---------|---------|
| [H08](../../handbook/08-agent-traceability.md) | ATF: campos y retención |
| [templates/worklog.md](../../templates/worklog.md) | Plantilla |
