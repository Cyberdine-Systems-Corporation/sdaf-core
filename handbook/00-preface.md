# 00 — Preface

| Campo | Valor |
|--------|--------|
| **Versión** | 0.3.0 |
| **Estado** | Approved |
| **Fecha** | 2026-09-18 |
| **Parte** | Front matter |
| **Norma superior** | Ninguna (inaugura la constitución del método) |
| **Deriva hacia** | Todo este handbook |

---

**En esta página:** [Por qué existe](#1-por-qué-existe-este-handbook) · [Qué es y qué no es](#2-qué-es-y-qué-no-es) · [Autoridad](#3-autoridad) · [Doble entregable](#4-doble-entregable) · [Cómo leer](#5-cómo-leer-este-handbook) · [Idioma](#6-idioma-y-estilo) · [Audiencia](#7-audiencia)

## 1. Por qué existe este handbook

SDAF (Spec-Driven AI Development Framework) es un **sistema de ingeniería** reutilizable. Este handbook es su constitución.

Existe para que:

- Las decisiones importantes sean explícitas y auditables.
- Humanos y agentes IA compartan las mismas reglas.
- El código derive de especificaciones, no al revés.
- Un nuevo colaborador (o un nuevo agente) pueda retomar el proyecto sin depender de conversaciones perdidas.

Sin constitución, la velocidad con IA produce deuda opaca. Con constitución, la velocidad es gobernada.

El **producto** concreto (charter, MVP, dominio) lo define el repo consumidor, no este core.

---

## 2. Qué es y qué no es

### Es

- La **constitución del método**.
- El contrato que deben respetar specs, ADRs, prompts, agentes e implementación del consumidor.
- La norma de que `specs/` del consumidor es la **verdad operativa** para implementar.

### No es

- Un documento de requisitos detallados (eso vive en `specs/` del consumidor).
- Un registro de decisiones tácticas (eso vive en ADRs del consumidor).
- Un log de trabajo de agentes (eso vive en `worklogs/` del consumidor).
- Un manual de usuario final.
- Un sustituto del knowledge de expertos (`knowledge/` del consumidor permanece inmutable).
- Una imposición de stack tecnológico.

---

## 3. Autoridad

1. Mientras un capítulo esté en **Draft**, orienta el trabajo pero puede corregirse sin ceremonia.
2. Cuando un capítulo pase a **Approved**, solo puede cambiarse mediante propuesta de enmienda, revisión humana, versión y entrada en `handbook/CHANGELOG.md`.
3. Ningún agente IA puede autodeclarar un capítulo como Approved.
4. Ninguna implementación puede contradecir un capítulo Approved. Si el código lo exige, primero se enmienda la norma o se registra un ADR de excepción temporal con fecha de caducidad.

---

## 4. Doble entregable

Cada proyecto bajo SDAF persigue, en paralelo:

| Entregable | Descripción |
|------------|-------------|
| **Producto** | Capacidad demostrable acorde al MVP / roadmap del consumidor |
| **Metodología** | SDAF: knowledge → specs → arquitectura → implementación trazable con agentes |

Ninguno justifica sacrificar al otro sin decisión explícita.

---

## 5. Cómo leer este handbook

1. Este preface y el [índice](README.md).
2. Parte I **antes** de escribir código o prompts de implementación.
3. Parte II según rol de agente.
4. Parte III para testing, review/QG, devops y seguridad.
5. Apéndices A (plantillas) y B (glosario de método).

Regla práctica: si vas a implementar y no puedes citar spec + ADR (si aplica) + criterio de aceptación, vuelve a la Parte I.

> [!CAUTION]
> Sin spec + ADR (si aplica) + criterio de aceptación: no implementar.

---

## 6. Idioma y estilo

- Idioma oficial: **español**.
- Estilo: normativo, corto, verificable (“debe”, “no debe”, “puede”).
- Evitar ensayos, marketing vacío y reglas imposibles de auditar.

---

## 7. Audiencia

Arquitecto / director técnico, Product Owner, desarrolladores, agentes IA del repositorio, revisores. Todos sujetos a la misma constitución. La IA no tiene privilegios para saltarse gates.

---

## Relacionado

| Destino | Por qué |
|---------|---------|
| [README del handbook](README.md) | Índice y estados de capítulo |
| [01-sdaf-framework.md](01-sdaf-framework.md) | Definición del marco |
| [09-testing-framework.md](09-testing-framework.md) | Parte III: tests desde specs |
| [docs/adopcion-y-upgrade.md](../docs/adopcion-y-upgrade.md) | HOWTO de pin y bootstrap |

## 8. Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.3.0 | 2026-09-19 | Enlaces a Parte III: se retira el calificador Draft (sin cambio de norma) |
| 0.3.0 | 2026-09-18 | Orden de lectura: Parte III y apéndice B (sin cambio de norma de 00–08) |
| 0.2.2 | 2026-09-17 | TOC, Relacionado y alerta de lectura (sin cambio de norma) |
| 0.2.0 | 2026-08-25 | Renumeración correlativa; orden de lectura Parte I / II / Apéndice A |
| 0.1.1 | 2026-08-24 | Approved (aprobación humana del director técnico) |
| 0.1.0 | 2026-08-24 | Extracción genérica desde laboratorio SDAF (ADR-008) |
