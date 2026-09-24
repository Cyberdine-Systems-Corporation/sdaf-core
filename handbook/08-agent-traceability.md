# 08 — Agent Traceability Framework

> Andamiaje (cabecera, TOC, Relacionado, Historial): `_meta/08-agent-traceability.yaml`.

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

Plantilla nueva (`templates/worklog.md`): esos campos van en **frontmatter** YAML, más `inicio` y `fin` (fecha y hora ISO 8601 con zona horaria; `fecha` es el día de `inicio`), `commit`, `pr`, `rama`, `sha` (cada uno `null` = ausencia explícita) y `resumen_acumulado` (índice de una línea, H07 §7). En el formato nuevo, `tiempo` es una duración ISO 8601 que no supera `fin − inicio`, y `coste` indica modalidad, importe, moneda, tokens y fuente del dato; lo que no se conozca se escribe `N/D: <motivo>`, nunca `N/D` a secas. Schema: [`worklog.schema.json`](../worklog.schema.json). Los worklogs en tabla markdown vigente siguen válidos; no se reescriben.

### 4.1 Recibo de iteración (opcional en 0.2.1)

Campos adicionales recomendados en worklogs **nuevos** (plantilla `templates/worklog.md`). Los worklogs anteriores siguen válidos con solo `Versión prompt`; no se reescriben.

| Campo | Uso |
|-------|-----|
| Prompt base | `prompt_id@version` del rol |
| Prompts adicionales | `ninguno` o ids versionados |
| Skills | `skill-id@version` |
| Reglas IDE | p. ej. `idioma-castellano`, `git-remoto-encargo` |
| Ad hoc | `ninguno` o párrafo en el mismo worklog (H07 §6) |

### 4.2 Línea de decisión (opcional en 0.2.1)

Apartado breve que cita spec/ADR/capítulo **§** que justificó cada elección normativa. No volcar el cuerpo del prompt. Si no hubo elección, omitir o escribir `N/A`.

### 4.3 Origen de cambios

Obligatorio en worklogs **nuevos** cuya iteración toca código de producto (H08 §5). Los worklogs anteriores siguen válidos sin este campo; no se reescriben.

Por archivo de producto modificado (o tabla resumen):

| Valor | Significado |
|-------|-------------|
| `humano` | Escrito o dictado sin generación de modelo |
| `ia` | Generado por el modelo citado en `Modelo` |
| `mixto` | Humano y modelo en el mismo archivo |
| `dependencia` | Vendored, lockfile o código de paquete |

Si la iteración **no** toca código de producto: `N/A`. Si el origen es `ia` o `mixto`, `Modelo` y `prompt_id@version` ya son campos obligatorios o de recibo.

Gate 2 / QG-Review comprueba este campo cuando el diff toca código de producto ([H10](10-code-review-and-quality-gates.md) §3.1).

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

Campos del worklog **nuevo** que cierran la cadena hacia el diff: `commit`, `pr`, `rama`, `sha`. Si no hay aún, el valor es `null` (ausencia explícita). El CI de presencia (`scripts/check-worklog-presence.py`) solo comprueba que exista un fichero bajo `worklogs/` cuando el diff toca código de producto; no parsea estos campos.

---

## 7. Retención

Los worklogs se conservan durante la vida del proyecto. No reescribir historia para ocultar fallos.

---
