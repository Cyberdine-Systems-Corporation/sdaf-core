# SDAF — Handbook del método

| Campo | Valor |
|--------|--------|
| Versión | 0.1.1 |
| Estado | Approved |
| Idioma | Español |
| Clasificación | Constitución del método (no del producto) |
| Última actualización | 2026-08-24 |

---

## Propósito

Este handbook es la **constitución del Spec-Driven AI Development Framework (SDAF)**.

- Define cómo se decide y qué es obligatorio en cualquier proyecto que adopte SDAF.
- Toda spec, ADR, backlog, prompt, worklog e implementación del **consumidor** debe poder justificarse remontándose a este handbook (método) más el handbook de producto del consumidor.
- Si un artefacto del consumidor lo contradice, prevalece este handbook hasta enmienda Approved aquí.

No es un tutorial ni un dump de requisitos de un producto.

El **handbook de producto** (charter, vision, MVP, arquitectura de solución) vive en el repo consumidor y **no** forma parte de este core.

---

## Mapa normativo (consumidor)

```text
Knowledge (inmutable, en el consumidor)
    → Handbook SDAF (este core) + handbook de producto (consumidor)
    → Specs en specs/ del consumidor  ← verdad operativa para implementar
    → Architecture + ADRs
    → Backlog
    → Implementation ∥ Spec-derived Tests
    → Review / Quality Gates
    → Release
```

Los **agentes IA** no son un nivel normativo: ejecutan el pipeline bajo estas reglas.
Los **prompts**, **skills** y **worklogs** son infraestructura de ingeniería, no sustituyen al handbook.

---

## Índice

### Front matter

| Cap. | Archivo | Título | Estado |
|------|---------|--------|--------|
| 00 | [00-preface.md](00-preface.md) | Preface | Approved |

### Parte II — SDAF

| Cap. | Archivo | Título | Estado |
|------|---------|--------|--------|
| 05 | [05-sdaf-framework.md](05-sdaf-framework.md) | SDAF Framework | Approved |
| 06 | [06-engineering-principles.md](06-engineering-principles.md) | Engineering Principles | Approved |
| 07 | [07-repository-organization.md](07-repository-organization.md) | Repository Organization | Approved |
| 08 | [08-specification-standard.md](08-specification-standard.md) | Specification Standard | Approved |
| 09 | [09-development-workflow.md](09-development-workflow.md) | Development Workflow | Approved |

### Parte IV — Ingeniería IA

| Cap. | Archivo | Título | Estado |
|------|---------|--------|--------|
| 13 | [13-ai-agent-framework.md](13-ai-agent-framework.md) | AI Agent Framework | Approved |
| 14 | [14-prompt-engineering-standard.md](14-prompt-engineering-standard.md) | Prompt Engineering Standard | Approved |
| 15 | [15-agent-traceability.md](15-agent-traceability.md) | Agent Traceability Framework | Approved |

### Apéndices

| Cap. | Archivo | Título | Estado |
|------|---------|--------|--------|
| B | [B-templates.md](B-templates.md) | Templates | Approved |
| — | [CHANGELOG.md](CHANGELOG.md) | Historial de versiones | Approved |

**Fuera de v0.1 (consumidor o v0.2+):** Parte I (producto), Parte III (arquitectura de solución), Parte V (testing/devops/security detallados), Parte VI (métricas de sprint), glosario de dominio.

---

## Estados de capítulo

| Estado | Significado |
|--------|-------------|
| **Draft** | Borrador; usable como guía, no cerrado |
| **Approved** | Norma vigente; cambios requieren revisión formal y CHANGELOG |

Ningún agente puede autodeclarar Approved.

---

## Prioridad ante conflicto (en un repo consumidor)

1. Capítulos **Approved** de este handbook (método)
2. Handbook de producto Approved del consumidor
3. ADRs vigentes en `architecture/decisions/`
4. Specs en `specs/`
5. Backlog
6. Implementación / prompts / worklogs
