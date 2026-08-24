# 05 — SDAF Framework

| Campo | Valor |
|--------|--------|
| **Versión** | 0.1.1 |
| **Estado** | Approved |
| **Fecha** | 2026-08-24 |
| **Parte** | II — SDAF |
| **Norma superior** | [00-preface.md](00-preface.md) |
| **Deriva hacia** | [06-engineering-principles.md](06-engineering-principles.md), [07-repository-organization.md](07-repository-organization.md), [08-specification-standard.md](08-specification-standard.md), [09-development-workflow.md](09-development-workflow.md) |

---

## 1. Propósito

Definir el **Spec-Driven AI Development Framework (SDAF)**: jerarquía normativa, pipeline de artefactos y reglas de gobierno para humanos y agentes.

SDAF no es un conjunto de prompts sueltos.

---

## 2. Definición

**SDAF** es un marco Spec-Driven donde:

1. El **conocimiento** de expertos es la fuente primaria del dominio (`knowledge/`, inmutable, en el consumidor).
2. El **handbook** de este core es la constitución del método; el consumidor añade constitución de producto.
3. Las **especificaciones** en `specs/` del **repo consumidor** son la única fuente de verdad operativa para implementar.
4. El **código** y los **tests** se derivan de las specs (nunca al revés como norma).
5. Los **agentes IA** ejecutan el pipeline bajo supervisión humana y trazabilidad.

El core **exige** la carpeta `specs/` y su estándar (cap. 08). **No** incluye el contenido de specs de ningún producto.

---

## 3. Jerarquía normativa

```text
Knowledge (inmutable)
    → Handbook SDAF (método) + handbook de producto (consumidor)
    → Specs (Glossary → Model → Rules → Use Cases → Acceptance)
    → Architecture + ADRs
    → Backlog
    → Implementation ∥ Spec-derived Tests
    → Review / Quality Gates
    → Release
```

### 3.1 Qué no es un nivel normativo

| Artefacto | Rol |
|-----------|-----|
| Agentes IA | Actores que operan el pipeline |
| Prompts | Contratos operativos versionados |
| Worklogs | Trazabilidad de iteraciones |
| Código | Resultado derivado |

### 3.2 Prioridad ante conflicto

1. Capítulos **Approved** de este handbook  
2. Handbook de producto Approved del consumidor  
3. ADRs vigentes  
4. Specs en `specs/`  
5. Backlog  
6. Implementación / prompts / worklogs  

---

## 4. Pipeline de dominio

```text
Knowledge
    → Glossary + Ubiquitous Language
    → Domain Model
    → Business Rules (Hard Constraints vs Soft Preferences)
    → Calculation Rules
    → Use Cases
    → Acceptance Tests
    → Implementation
```

No se implementa el documento de experto “tal cual”. Se transforma.

---

## 5. Doble entregable

| Entregable | Significado |
|------------|-------------|
| Producto | Capacidad demostrable acorde al MVP / roadmap del consumidor |
| Metodología | Artefactos SDAF actualizados (specs, ADRs, worklogs, prompts) |

Acelerar el producto destruyendo la metodología es una violación de SDAF.

---

## 6. Gobierno antes de implementar

Antes de generar implementación de una feature de producto, **debe** existir:

1. Especificación aplicable (o enmienda Approved del alcance).
2. Decisión de arquitectura relevante (ADR) cuando el cambio cruza límites o stack.
3. Criterios de aceptación / tests derivados de la spec.
4. Entrada de trazabilidad (worklog) de la iteración.

Si falta alguno → **STOP**. Proponer su creación; no improvisar código.

El core **no** fija el stack: exige que las decisiones de stack/límites queden en ADRs (gobernanza). El pack de stack es opcional.

Detalle operativo en el capítulo 09.

---

## 7. Agentes en SDAF (resumen)

- Equipo especializado, no un único agente omnisciente.
- Activos y stubs se declaran en `sdaf.config.yaml` del consumidor (detalle en Parte IV).
- El humano aprueba handoffs relevantes y todo capítulo Approved.
- Ningún agente puede autodeclarar Approved ni saltarse el gate del §6.

---

## 8. Portabilidad

Este capítulo **debe** poder aplicarse a otro producto y otro stack con un handbook de producto y, si aplica, un pack de stack. No menciona un producto concreto ni un runtime concreto como norma.

---

## 9. Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.1.1 | 2026-08-24 | Approved (aprobación humana del director técnico) |
| 0.1.0 | 2026-08-24 | Extracción genérica (ADR-008): norma de `specs/` y gobernanza de stack explícitas |
