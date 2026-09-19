---
name: testing-review-pr
description: Ejecuta Gate 2 / review de PR con checklist H10, acceptance del PBI, tests y dictamen de merge. Usar en Testing+Review o al pedir merge recomendado.
---

# testing-review-pr

| Campo | Valor |
|--------|--------|
| ID | testing-review-pr |
| Versión | 0.3.2 |
| Estado | Approved |
| Prioridad | alta |
| Fecha | 2026-09-19 |
| Norma | [handbook/10](../../handbook/10-code-review-and-quality-gates.md), [handbook/05](../../handbook/05-development-workflow.md) §Gate 2, [handbook/09](../../handbook/09-testing-framework.md), [handbook/08](../../handbook/08-agent-traceability.md) §4.3 |

## Disparadores

- “Gate 2”, “review del PR”, “¿merge?”, cierre Testing+Review.

## Pasos

1. Confirmar Gate 0 del PBI (o regularización documentada). Skill `sdaf-gate0` si hace falta.
2. Checklist H10: gobierno (incl. origen H08 §4.3 si hay código de producto), dominio/arquitectura, calidad, coding standards del consumidor si hay ADR, tests vs acceptance, H12 §5.1 si toca superficie de seguridad.
3. Ejecutar el comando de test del **consumidor** (runbook / pack); anotar conteos. No inventar un runner.
4. Contrastar acceptance del PBI con tests presentes (H09).
5. Dictamen: **merge sí / no / condicionado** con hallazgos priorizados (H10 §5). El dictamen **no** satisface QG-Review.
6. Worklog de review (`testing-review-pr@0.3.2` + prompt Testing+Review citados).
7. QG-Review exige aprobación humana **nominada** del merge (H10 §2). No auto-merge.

> [!CAUTION]
> ⛔ No recomendar merge si Gate 0 está roto, el acceptance del flujo tocado falla, QG-Sec falla o falta origen de cambios en código de producto.

## Definition of Done

- [ ] Checklist H10 recorrido.
- [ ] Resultado de tests registrado (comando del consumidor).
- [ ] Dictamen de merge explícito; siguiente agente = humano.
- [ ] Worklog cerrado (origen H08 §4.3 si aplica).

## Restricciones

- No aprobar handbook/specs/ADR.
- No ampliar alcance Out del MVP del consumidor en el review “de paso”.
- No exigir el checklist de coding standards si el consumidor no tiene ADR/pack que lo fije.
- Completar este playbook no autoriza merge.

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.3.2 | 2026-09-19 | QG-Review = humano nominado; origen ATF; QG-Sec H12 §5.2 |
| 0.3.0 | 2026-09-19 | Approved (aprobación humana del director técnico) |

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| 📖 | [H10](../../handbook/10-code-review-and-quality-gates.md) | Checklist y QG |
| 📖 | [H09](../../handbook/09-testing-framework.md) | Tests desde specs |
| 📝 | [testing-review-agent](../../prompts/agents/testing-review-agent.md) | Prompt de rol |
