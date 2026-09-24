# 03 — Repository Organization

> Andamiaje (cabecera, TOC, Relacionado, Historial): `_meta/03-repository-organization.yaml`.

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

El método SDAF puede referenciarse en el consumidor vía pin (submodule u otra ruta) a un **tag** de sdaf-core. El procedimiento de adopción y upgrade está en [`docs/adopcion-y-upgrade.md`](../docs/adopcion-y-upgrade.md); este capítulo no fija una única ruta de carpeta como norma.

Este **core** también publica ADRs de gobernanza del método en [`architecture/decisions/`](../architecture/decisions/README.md) y los worklogs de sus cambios materiales en `worklogs/` ([H08 §5](08-agent-traceability.md)). El árbol de arriba es el del consumidor: no obliga al core a copiar `knowledge/` ni `specs/`.

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
