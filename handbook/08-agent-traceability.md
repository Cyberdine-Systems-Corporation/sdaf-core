# 08 — Agent Traceability Framework

| Campo | Valor |
|--------|--------|
| **Versión** | 0.2.2 |
| **Estado** | Approved |
| **Fecha** | 2026-09-17 |
| **Parte** | II — Ingeniería IA |
| **Norma superior** | [06-ai-agent-framework.md](06-ai-agent-framework.md), [07-prompt-engineering-standard.md](07-prompt-engineering-standard.md), [05-development-workflow.md](05-development-workflow.md) |
| **Deriva hacia** | `worklogs/` del consumidor, templates |

---

**En esta página:** [Propósito](#1-propósito) · [Principio](#2-principio) · [Organización](#3-organización) · [Campos](#4-campos-obligatorios) · [Cuándo](#5-cuándo-crear-worklog) · [Cadena](#6-cadena-de-trazabilidad) · [Retención](#7-retención)

## 1. Propósito

Definir el **Agent Traceability Framework (ATF)**: registro de cada iteración para que el desarrollo sea auditable.

Sin ATF, SDAF no es demostrable.

---

## 2. Principio

> [!IMPORTANT]
> Si no está en el worklog (o en un artefacto enlazado desde él), **no forma parte del contexto oficial** del handoff.

El chat es efímero. El worklog es evidencia. Los worklogs viven en el **repo consumidor**, no en este core.

---

## 3. Organización

```text
worklogs/
  PBI-001/
    Iteration-001.md
    Iteration-002.md
```

Un directorio por PBI (o iniciativa: `INIT-.../`). Plantilla: `templates/worklog.md`.

---

## 4. Campos obligatorios

Fecha, agente, modelo, versión prompt, contexto, especificaciones utilizadas, archivos leídos, archivos modificados, resultado, tiempo, coste (`N/D` si no se conoce), observaciones, pruebas ejecutadas, estado (`en_curso` / `hecho` / `bloqueado` / `abortado`), siguiente agente.

### 4.1 Recibo de iteración (opcional en 0.2.1)

Campos adicionales recomendados en worklogs **nuevos** (plantilla `templates/worklog.md`). Los worklogs anteriores siguen válidos con solo `Versión prompt`; no se reescriben.

| Campo | Uso |
|-------|-----|
| Prompt base | `prompt_id@version` del rol |
| Prompts adicionales | `ninguno` o ids versionados |
| Skills | `skill-id@version` |
| Reglas IDE | p. ej. `idioma-castellano` |
| Ad hoc | `ninguno` o párrafo en el mismo worklog (H07 §6) |

### 4.2 Línea de decisión (opcional en 0.2.1)

Apartado breve que cita spec/ADR/capítulo **§** que justificó cada elección normativa. No volcar el cuerpo del prompt. Si no hubo elección, omitir o escribir `N/A`.

---

## 5. Cuándo crear worklog

| Situación | ¿Worklog? |
|-----------|-----------|
| Feature/PBI con Gate 0 | Sí (G0.5) |
| Cambio de handbook/ADR/spec material | Sí |
| Typo trivial sin decisión | No obligatorio |
| Spike con ADR de excepción | Sí |
| Ejecución que toca código de producto | Sí |

---

## 6. Cadena de trazabilidad

```mermaid
flowchart LR
  PBI[Backlog PBI] --> Spec[Specs / ADRs]
  Spec --> Prompt[Prompt@version]
  Prompt --> WL[Worklog]
  WL --> Diff[Diff]
  Diff --> Tests[Tests]
  Tests --> Rev[Review]
  classDef norm fill:#d0e3f8,stroke:#1e4d8b,color:#1a1a1a;
  classDef ok fill:#d4edda,stroke:#2d6a4f,color:#1a1a1a;
  classDef stub fill:#e9ecef,stroke:#6c757d,color:#1a1a1a;
  class PBI,Spec,Prompt norm
  class WL,Tests,Rev ok
  class Diff stub
```

---

## 7. Retención

Los worklogs se conservan durante la vida del proyecto. No reescribir historia para ocultar fallos.

---

## Relacionado

| Destino | Por qué |
|---------|---------|
| [templates/worklog.md](../templates/worklog.md) | Plantilla ATF |
| [skills/sdaf-worklog-handoff](../skills/sdaf-worklog-handoff/SKILL.md) | Cerrar y pasar el testigo |
| [05-development-workflow.md](05-development-workflow.md) | G0.5 exige worklog abierto |

## 8. Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.2.2 | 2026-09-17 | TOC, Relacionado, diagrama y alerta ATF (sin cambio de norma) |
| 0.2.1 | 2026-09-13 | Recibo de iteración y línea de decisión (opcionales; sin backfill) |
| 0.2.0 | 2026-08-25 | Renumerado (ex-15); Parte II |
| 0.1.1 | 2026-08-24 | Approved (aprobación humana del director técnico) |
| 0.1.0 | 2026-08-24 | Extracción genérica; worklogs en el consumidor (ADR-008) |
