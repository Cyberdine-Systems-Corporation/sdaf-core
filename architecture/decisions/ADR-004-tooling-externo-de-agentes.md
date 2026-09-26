# ADR-004 — Tooling externo de agentes

| Campo | Valor |
|--------|--------|
| Estado | Aceptado |
| Fecha | 2026-09-26T08:41+02:00 |
| Decisores | Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS) |
| Aceptación | 2026-09-26T11:41+02:00, por Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS). El agente transcribe la aceptación dada en el encargo; no la autodeclara ([H00 §3.3](../../handbook/00-preface.md)). |
| Relacionado | [H06 §6 y §7](../../handbook/06-ai-agent-framework.md#7-restricciones-globales), [H05 §3](../../handbook/05-development-workflow.md#3-gate-0-pre-implementación-stop), [H08](../../handbook/08-agent-traceability.md), [H10 §2](../../handbook/10-code-review-and-quality-gates.md), [H12](../../handbook/12-security-standards.md), [contrato de pack](../../docs/contrato-pack-stack.md), [integración gentle-ai](../../docs/integracion-gentle-ai.md) |

## Contexto

Hay instaladores que configuran el entorno de los agentes de un repo: memoria persistente, servidores MCP, bibliotecas de skills, listas de rutas bloqueadas, personas y flujos de trabajo propios. El caso de referencia es [gentle-ai](https://github.com/Gentleman-Programming/gentle-ai) (MIT), que configura Claude Code, Cursor, Codex, OpenCode y otros.

Ese tooling no es un pack de stack: no aporta contratos, prompts ni ids de extensión. Sin embargo, trae flujos que se solapan con el método o lo contradicen: un ciclo de specs paralelo que implementa sin Gate 0 (`sdd-*`, presente hasta v3.7.0 y retirado en `main` el 2026-09-25), un commit por tarea sin encargo humano y una memoria que puede tomarse por evidencia. El core no dice hoy qué lugar ocupa. Cada consumidor lo resolvería a su manera.

## Decisión

1. **El core sigue tool-agnostic.** No empaqueta, versiona ni exige tooling de entorno (instaladores, memoria, MCP, personas). Las skills del core siguen en `skills/` sin depender de ninguna herramienta ([H06 §6](../../handbook/06-ai-agent-framework.md#6-skills)).
2. **El tooling externo vive en el consumidor** como capa de entorno subordinada al método. No es un pack: no aporta contratos, prompts ni ids de extensión, y no se declara en `stack.pack`.
3. **Specs Approved y worklogs son la única verdad y la única evidencia.** La memoria persistente del tooling es una caché de contexto. No sustituye al worklog (ATF) ni a las specs ([H08](../../handbook/08-agent-traceability.md)).
4. **Ningún flujo externo sustituye a Gate 0 ni aprueba nada.** Los ciclos de specs paralelos (p. ej. `sdd-*` de gentle-ai) no se usan para producto. Las specs viven en `specs/` y las aprueba un humano ([H05 §3](../../handbook/05-development-workflow.md#3-gate-0-pre-implementación-stop), [H00 §3](../../handbook/00-preface.md)).
5. **H06 §7 prevalece** sobre cualquier protocolo de commit, rama o PR del tooling. Solo lo relaja una excepción que el `AGENTS.md` o un ADR del consumidor enumeren ([H06 §7](../../handbook/06-ai-agent-framework.md#7-restricciones-globales)).
6. **La review automatizada no es QG-Review.** Su dictamen puede alimentar `testing-review-pr`, pero el merge sigue exigiendo revisión humana nominada ([H10 §2](../../handbook/10-code-review-and-quality-gates.md)).
7. **Adopción opcional.** Ninguna skill ni gate del core presupone el tooling. El consumidor lo declara en `tooling.<id>` de `sdaf.config.yaml` (hoy solo `tooling.gentle_ai`, con una release o un SHA de commit, no una rama). Bloque ausente o `null` significa no adoptado. Una release que aún incluya un flujo incompatible (p. ej. `sdd` hasta v3.7.0) se admite con aviso, porque ese componente no se instala ([`sdaf.config.schema.yaml`](../../sdaf.config.schema.yaml)).

La guía operativa para gentle-ai (qué componentes usar, cómo instalarlo y qué cláusula añadir al `AGENTS.md`) vive en [`docs/integracion-gentle-ai.md`](../../docs/integracion-gentle-ai.md).

## Alternativas consideradas

- **Tratarlo como pack** (`sdaf-tooling-*`). Obliga a ampliar el contrato de pack con un tipo que no aporta playbooks del método y ata el core al ritmo de releases de una herramienta ajena.
- **Prohibirlo.** Pierde piezas compatibles (listas de rutas bloqueadas, índice de skills, documentación viva) y no impide que el consumidor lo instale igualmente.
- **No decir nada.** Deja que cada consumidor descubra solo los choques con Gate 0 y H06 §7.

## Consecuencias

- No cambia la constitución: el ADR aplica H05, H06, H08 y H10 tal como están.
- El schema de config gana el bloque opcional `tooling`. Es aditivo: ninguna config existente deja de validar, así que no es breaking ([H13 §5](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md)). Entra en el parche `0.4.1` ([`handbook/CHANGELOG.md`](../../handbook/CHANGELOG.md)); `sdaf.version` sigue en `"0.4.0"`.
- El core publica una guía HOWTO por herramienta de referencia. Esa guía fecha la versión revisada y no sigue cada release de la herramienta.
- Un cambio posterior puede añadir a `AGENTS.md.template` una cláusula opcional de precedencia frente al tooling externo.
- Worklogs de la propuesta: [Iteration-001](../../worklogs/ADR-004-tooling-externo/Iteration-001.md) (ADR y guía), [Iteration-002](../../worklogs/ADR-004-tooling-externo/Iteration-002.md) (SDD frente a Gate 0), [Iteration-003](../../worklogs/ADR-004-tooling-externo/Iteration-003.md) (adopción opcional y clave `tooling`) , [Iteration-004](../../worklogs/ADR-004-tooling-externo/Iteration-004.md) (SHA de commit y aviso T1) e [Iteration-005](../../worklogs/ADR-004-tooling-externo/Iteration-005.md) (aceptación y parche 0.4.1) ([H08 §5](../../handbook/08-agent-traceability.md)).
