# 08 — Specification Standard

| Campo | Valor |
|--------|--------|
| **Versión** | 0.1.1 |
| **Estado** | Approved |
| **Fecha** | 2026-08-24 |
| **Parte** | II — SDAF |
| **Norma superior** | [05-sdaf-framework.md](05-sdaf-framework.md), [07-repository-organization.md](07-repository-organization.md) |
| **Deriva hacia** | `specs/` del consumidor, [09-development-workflow.md](09-development-workflow.md), tests, backlog |

---

## 1. Propósito

Definir qué es una especificación válida: formato mínimo, tipos, estados, trazabilidad y relación con knowledge, ADRs y código.

**Norma canónica:** en todo proyecto bajo SDAF, la verdad operativa para implementar está en `specs/` del repo consumidor. Este capítulo estandariza esa carpeta; no la rellena.

Sin este estándar, “tener una spec” es ambiguo y el Gate 0 no es auditable.

---

## 2. Definición

Una **especificación** es un artefacto versionado en `specs/` que describe de forma **testeable** qué debe cumplirse, con criterios de aceptación explícitos y referencias a knowledge/handbook/ADRs cuando aplique.

No es un ensayo sin criterios, ni un ticket de backlog (el backlog **apunta** a specs), ni un PR description como única fuente.

---

## 3. Tipos y ubicación

| Tipo | Carpeta | Contenido típico |
|------|---------|------------------|
| Producto | `specs/product/` | Capabilities, journeys, NFRs de producto |
| Dominio | `specs/domain/` | Glossary, modelo, reglas hard/soft, invariantes |
| Aplicación | `specs/application/` | Casos de uso, comandos/consultas, contratos a nivel app |
| Aceptación | `specs/acceptance/` | Escenarios Given/When/Then mapeables a tests |

Una capacidad puede tener varios archivos enlazados; **una fuente canónica** y referencias.

---

## 4. Cabecera obligatoria

| Campo | Descripción |
|--------|-------------|
| Título | Nombre estable |
| ID | Identificador único (p. ej. `SPEC-DOM-001`) |
| Versión | Semver o `MAJOR.MINOR` |
| Estado | `Draft` / `Approved` / `Deprecated` |
| Fecha | Última actualización |
| Fuentes | Rutas en `knowledge/` y capítulos de handbook |
| ADRs relacionados | Si aplica |
| PBIs / backlog | IDs vinculados |
| Derivados | Tests, slices, worklogs esperados |

Solo specs **Approved** autorizan implementación de producto (salvo spike explícito con ADR de excepción y fecha de caducidad).

---

## 5. Contenido mínimo por tipo

### 5.1 Dominio — Glossary / Ubiquitous Language

Término, definición, sinónimos prohibidos, contexto.

### 5.2 Dominio — Model / Rules

Aggregates/entities/VOs a nivel conceptual; invariantes; reglas **Hard** vs **Soft** etiquetadas; ejemplos y contraejemplos.

### 5.3 Application — Use cases

Actor, precondiciones, flujo, postcondiciones; comandos/queries por nombre, no código.

### 5.4 Acceptance

Observables, independientes en lo razonable, trazables. Formato preferido:

```text
Dado [contexto]
Cuando [acción]
Entonces [resultado observable]
```

---

## 6. Pipeline de elaboración

```text
knowledge/raw|curated
    → specs/domain (glossary → model → rules)
    → specs/application (use cases)
    → specs/acceptance
    → tests (derivados)
    → implementación
```

1. No saltar de knowledge a código.
2. Si una acceptance contradice una regla de dominio, se corrige antes de codear.
3. Alcance diferido se marca explícitamente en la spec (`Implementación: diferida`).

---

## 7. Versionado y cambios

- Cambio incompatible de comportamiento → versión mayor de la spec y tests.
- Specs Approved solo cambian con revisión humana explícita.
- Deprecated: dejar archivo con puntero al sucesor.

---

## 8. Relación con ADRs

| Pregunta | Artefacto |
|----------|-----------|
| ¿Qué debe hacer el negocio/sistema? | Spec |
| ¿Qué opción técnica (incl. stack) elegimos y por qué? | ADR |
| ¿Está permitido por la constitución? | Handbook |

Una spec no sustituye un ADR de stack o de límites.

---

## 9. Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.1.1 | 2026-08-24 | Approved (aprobación humana del director técnico) |
| 0.1.0 | 2026-08-24 | Extracción genérica; `specs/` = verdad operativa del consumidor (ADR-008) |
