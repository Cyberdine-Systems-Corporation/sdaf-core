# 13 — AI Agent Framework

| Campo | Valor |
|--------|--------|
| **Versión** | 0.1.1 |
| **Estado** | Approved |
| **Fecha** | 2026-08-24 |
| **Parte** | IV — Ingeniería IA |
| **Norma superior** | [05-sdaf-framework.md](05-sdaf-framework.md), [09-development-workflow.md](09-development-workflow.md) |
| **Deriva hacia** | `agents/`, `prompts/agents/`, `skills/`, [14-prompt-engineering-standard.md](14-prompt-engineering-standard.md), [15-agent-traceability.md](15-agent-traceability.md) |

---

## 1. Propósito

Definir el equipo de agentes de **ingeniería** (desarrollo). No confundir con una eventual IA de producto del consumidor.

Los agentes ejecutan el pipeline SDAF. No son un nivel normativo. No aprueban capítulos Approved ni saltan Gate 0.

---

## 2. Distinción crítica

| Tipo | Dónde | Rol |
|------|-------|-----|
| Agentes de ingeniería (este capítulo) | `agents/`, `prompts/` | Specs, ADRs, código, tests, docs |
| IA de producto | Infraestructura del consumidor (si existe) | Fuera del alcance de este core |

---

## 3. Modelo operativo

**Problema:** demasiados agentes activos con un solo supervisor generan thrash.

**Decisión del core:** pocos **activos** + **stubs** (contrato + prompt listos). La lista concreta la fija `sdaf.config.yaml`.

Por defecto en v0.1:

### 3.1 Activos

| Agente | Objetivo | Salidas típicas |
|--------|----------|-----------------|
| Specification | Knowledge → specs/acceptance | `specs/**` |
| Architecture | Boundaries, ADRs | `architecture/decisions/**` |
| Testing+Review | Tests derivados, gates, review | `tests/**`, dictámenes |

### 3.2 Stubs

Product, Domain, Application, DevOps, Review (puro), Testing (puro).

Un stub **debe** tener contrato, prompt base y estado `stub` visible.

Agentes de implementación de UI/infra/stack (p. ej. Frontend) los aporta el **pack de stack** o el consumidor; no son norma de este core.

---

## 4. Contrato de agente (obligatorio)

Cada agente en `agents/` documenta: objetivo, responsabilidades, entradas, salidas, restricciones, checklist, KPIs, Definition of Done, prompt base.

`AGENTS.md` en el consumidor actúa como **router** (materializado desde `AGENTS.md.template`).

---

## 5. Orquestación y handoffs

```text
Specification → Architecture → (implementación del consumidor)
                                      ↘ Testing+Review ↗
```

1. El saliente cierra worklog con “siguiente agente”.
2. El entrante lee worklog + specs; **no** depende de chat no registrado.
3. El humano puede reordenar o fusionar pasos; no puede omitir Gate 0.

---

## 6. Skills

Las **skills** viven en `skills/` (índice: [`skills/README.md`](../skills/README.md)). Tool-agnostic: no dependen de `.cursor/skills/`.

| Capa | Contiene |
|------|----------|
| Contrato + prompt | *Quién* / rol |
| Skill (`SKILL.md`) | *Cómo* (flujo) |
| Rules IDE | Restricciones locales finas |

Citar `skill-id@version` en el worklog. Gate 0 manda sobre cualquier skill de implementación.

Catálogo core (prioridad alta/media): `sdaf-gate0`, `sdaf-worklog-handoff`, `sdaf-agent-router`, `spec-draft-pbi`, `adr-propose`.

---

## 7. Restricciones globales

- Castellano en artefactos de ingeniería.
- Respetar handbook y specs Approved.
- No inventar alcance Out del MVP del consumidor.
- No marcar Approved.
- No force-push ni destruir history sin orden humana.
- No introducir secretos.
- Economía de tokens (cap. 14).

---

## 8. Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.1.1 | 2026-08-24 | Approved (aprobación humana del director técnico) |
| 0.1.0 | 2026-08-24 | Agentes genéricos; implementación de stack fuera del core (ADR-008) |
