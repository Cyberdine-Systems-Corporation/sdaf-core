# 07 — Prompt Engineering Standard

> Andamiaje (cabecera, TOC, Relacionado, Historial): `_meta/07-prompt-engineering-standard.yaml`.

## 1. Propósito

Los prompts son **artefactos versionados**, no texto libre improvisado como norma de trabajo.

---

## 2. Principios

1. **Una responsabilidad** por prompt.
2. **Contexto mínimo** — enlazar rutas; no pegar el handbook entero.
3. **Reutilizar** artefactos Approved por referencia.
4. **Sin duplicar** la constitución.
5. **Castellano** en instrucciones y criterios.
6. Toda ejecución relevante **cita la versión** del prompt en el worklog (recibo ATF: ver cap. 08).

---

## 3. Árbol de la biblioteca

```text
prompts/
  system/           # p. ej. master-architect.md
  agents/           # un prompt base por agente
  documentation/    # handbook-author, spec-author, adr-author
```

El consumidor puede añadir `planning/`, `review/`, `quality/`. El prompt maestro de gobierno vive en `prompts/system/master-architect.md`.

---

## 4. Estructura obligatoria

Metadatos (ID, versión, estado, rol, fecha), objetivo, contexto (enlaces), entradas, restricciones, artefactos, resultado esperado, formato de salida, criterios de aceptación, historial **en el cuerpo del prompt**.

El andamiaje de los **capítulos** del handbook (cabecera, TOC, Relacionado, Historial) vive en `handbook/_meta/` e `handbook/index.yaml` ([ADR-003](../architecture/decisions/ADR-003-formato-de-artefactos.md), Aceptado). No forma parte de la estructura obligatoria de un prompt.

---

## 5. Versionado

- `MAJOR.MINOR` en cabecera.
- Cambio incompatible → MAJOR.
- Worklog registra `prompt_id@version`.
- No editar en silencio un prompt Approved usado en iteraciones abiertas.

---

## 6. Prompts ad hoc

Solo experimentos locales o incrustados en el worklog de esa iteración. Si se reutiliza → promover a `prompts/`.

---

## 7. Economía de tokens

| Práctica | Norma |
|----------|--------|
| Adjuntar handbook completo | Prohibido por defecto |
| Adjuntar `handbook/_meta/` o `index.yaml` | Prohibido por defecto; el cuerpo del capítulo basta |
| Citar capítulo/sección | Obligatorio cuando basen la decisión |
| Pegar specs enteras irrelevantes | Evitar |
| Multi-agente en un mega-prompt | Prohibido; usar handoff |
| Resumen como sustituto del prompt versionado | Prohibido; el resumen es índice (`id@version` + 1 línea) |
| Mega-resumen de todos los agentes activos en un system prompt | Prohibido (sigue siendo mega-prompt) |

Un resumen compatible **apunta** a `prompts/<id>@versión`, skills y secciones de spec/ADR. No duplica la constitución. Si resumen y prompt discrepan, **gana el prompt**.

---

## 8. Relación con skills

Prompts = rol; skills = playbooks de flujo. Enlazar `skills/<id>/SKILL.md`; no pegar. Citar ambos en worklog.

---

## 9. Relación con IDEs

`.cursor/rules/` contiene reglas **finas** que apuntan al handbook. No duplicar Partes I–II. El trabajo debe poder reproducirse desde `prompts/` + `skills/` + repo.

---
