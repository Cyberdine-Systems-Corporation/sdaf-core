# 07 — Repository Organization

| Campo | Valor |
|--------|--------|
| **Versión** | 0.1.1 |
| **Estado** | Approved |
| **Fecha** | 2026-08-24 |
| **Parte** | II — SDAF |
| **Norma superior** | [05-sdaf-framework.md](05-sdaf-framework.md) |
| **Deriva hacia** | Specs, ADRs, agentes, prompts, skills, worklogs, código del consumidor |

---

## 1. Propósito

Definir la organización del **repo consumidor** como almacén de conocimiento, decisiones, especificaciones, trazabilidad y código.

El repo no es solo `src/`.

---

## 2. Árbol normativo (consumidor)

Carpetas obligatorias del método; las de código y contrato HTTP son del consumidor (rutas configurables):

```text
/
├── README.md
├── AGENTS.md                 # materializado desde AGENTS.md.template
├── sdaf.config.yaml
├── handbook/                 # constitución de producto del consumidor
│                             # (el método puede referenciarse vía sdaf-core)
├── knowledge/
│   ├── raw/
│   └── curated/
├── specs/
│   ├── product/
│   ├── domain/
│   ├── application/
│   └── acceptance/
├── architecture/
│   └── decisions/            # ADRs (incluidas decisiones de stack)
├── backlog/
├── agents/
├── prompts/
├── skills/
├── worklogs/
├── templates/
├── docs/                     # HOWTO / runbooks (no sustituye handbook ni specs)
├── src/                      # código de producto (ruta vía sdaf.config)
├── tests/
├── .cursor/rules/
└── .github/
```

`postman/` u otros contratos de API son opcionales y no sustituyen specs.

---

## 3. Responsabilidad por carpeta

| Carpeta | Contiene | No contiene |
|---------|----------|-------------|
| `knowledge/` | Evidencia de expertos; inmutable | Specs “mejoradas”, código |
| `handbook/` (método + producto) | Norma constitucional | Detalle táctico de un PBI |
| `specs/` | **Verdad operativa para implementar** | Ensayos de diseño sin aceptación |
| `architecture/decisions/` | ADRs (incl. stack/límites) | Tutoriales largos |
| `backlog/` | PBIs / historias trazables a specs | Implementación |
| `agents/` | Contratos de agente | Prompts completos |
| `prompts/` | Prompts versionados | Instrucciones ad hoc no registradas |
| `skills/` | Playbooks (`SKILL.md`) | Prompts de rol, constitución, código |
| `worklogs/` | Iteraciones ATF | Sustituto de commits o specs |
| `docs/` | Runbooks, HOWTO | Constitución ni specs canónicas |
| `src/`, `tests/` | Código y pruebas | Knowledge crudo |

---

## 4. Reglas de `knowledge/`

1. `raw/` conserva originales sin reescritura silenciosa.
2. `curated/` solo añade extracciones; las interpretaciones van a `specs/`.
3. Nunca se borra knowledge para encajar el código.

---

## 5. Separación Knowledge / Specs / Código

```text
knowledge  →  qué dijo el experto
specs      →  qué acordamos construir (interpretado, testeable)
src/tests  →  cómo quedó construido
```

Si el código descubre un error de spec: se enmienda la spec (y el test), no se deja el hallazgo solo en un comentario.

---

## 6. Idioma y nombres

- Artefactos de ingeniería en **castellano** (contenido).
- Nombres de carpetas del árbol SDAF en inglés corto estable.
- Código: convención que fije el ADR de coding standards del consumidor (o pack de stack).

---

## 7. Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.1.1 | 2026-08-24 | Approved (aprobación humana del director técnico) |
| 0.1.0 | 2026-08-24 | Árbol genérico; sin asumir runtime concreto (ADR-008) |
