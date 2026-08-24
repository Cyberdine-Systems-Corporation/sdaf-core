# 15 — Agent Traceability Framework

| Campo | Valor |
|--------|--------|
| **Versión** | 0.1.1 |
| **Estado** | Approved |
| **Fecha** | 2026-08-24 |
| **Parte** | IV — Ingeniería IA |
| **Norma superior** | [13-ai-agent-framework.md](13-ai-agent-framework.md), [14-prompt-engineering-standard.md](14-prompt-engineering-standard.md), [09-development-workflow.md](09-development-workflow.md) |
| **Deriva hacia** | `worklogs/` del consumidor, templates |

---

## 1. Propósito

Definir el **Agent Traceability Framework (ATF)**: registro de cada iteración para que el desarrollo sea auditable.

Sin ATF, SDAF no es demostrable.

---

## 2. Principio

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

```text
Backlog (PBI) → Specs / ADRs → Prompt@version → Worklog → Diff → Tests → Review
```

---

## 7. Retención

Los worklogs se conservan durante la vida del proyecto. No reescribir historia para ocultar fallos.

---

## 8. Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.1.1 | 2026-08-24 | Approved (aprobación humana del director técnico) |
| 0.1.0 | 2026-08-24 | Extracción genérica; worklogs en el consumidor (ADR-008) |
