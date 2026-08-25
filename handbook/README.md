# SDAF — Handbook del método

| Campo | Valor |
|--------|--------|
| Versión | 0.2.0 |
| Estado | Approved |
| Idioma | Español |
| Clasificación | Constitución del método (no del producto) |
| Última actualización | 2026-08-25 |

---

## Propósito

Este handbook es la **constitución del Spec-Driven AI Development Framework (SDAF)**.

- Define cómo se decide y qué es obligatorio en cualquier proyecto que adopte SDAF.
- Toda spec, ADR, backlog, prompt, worklog e implementación del **consumidor** debe poder justificarse remontándose a este handbook (método) más el handbook de producto del consumidor.
- Si un artefacto del consumidor lo contradice, prevalece este handbook hasta enmienda Approved aquí.

No es un tutorial ni un dump de requisitos de un producto.

El **handbook de producto** (charter, vision, MVP, arquitectura de solución) vive en el repo consumidor y **no** forma parte de este core.

Los HOWTO de adopción, upgrade y contrato de pack viven en [`docs/`](../docs/) de este core (no sustituyen este handbook).

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

### Parte I — Método SDAF

| Cap. | Archivo | Título | Estado |
|------|---------|--------|--------|
| 01 | [01-sdaf-framework.md](01-sdaf-framework.md) | SDAF Framework | Approved |
| 02 | [02-engineering-principles.md](02-engineering-principles.md) | Engineering Principles | Approved |
| 03 | [03-repository-organization.md](03-repository-organization.md) | Repository Organization | Approved |
| 04 | [04-specification-standard.md](04-specification-standard.md) | Specification Standard | Approved |
| 05 | [05-development-workflow.md](05-development-workflow.md) | Development Workflow | Approved |

### Parte II — Ingeniería IA

| Cap. | Archivo | Título | Estado |
|------|---------|--------|--------|
| 06 | [06-ai-agent-framework.md](06-ai-agent-framework.md) | AI Agent Framework | Approved |
| 07 | [07-prompt-engineering-standard.md](07-prompt-engineering-standard.md) | Prompt Engineering Standard | Approved |
| 08 | [08-agent-traceability.md](08-agent-traceability.md) | Agent Traceability Framework | Approved |

### Apéndices

| Cap. | Archivo | Título | Estado |
|------|---------|--------|--------|
| A | [A-templates.md](A-templates.md) | Templates | Approved |
| — | [CHANGELOG.md](CHANGELOG.md) | Historial de versiones | Approved |

**Alcance 0.2:** constitución correlativa del método; adopción/upgrade y contrato de pack en `docs/`; skills `sdaf-bootstrap` y `sdaf-upgrade`.

**Fuera de 0.2 (consumidor, packs o releases posteriores):** charter/MVP/arquitectura de solución (consumidor); testing/devops/security y métricas de sprint detallados; glosario de dominio; idiomas distintos de `es`.

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
