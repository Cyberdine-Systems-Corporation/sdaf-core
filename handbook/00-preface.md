# 00 — Preface

> Andamiaje (cabecera, TOC, Relacionado, Historial): `_meta/00-preface.yaml`.

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

El ciclo de vida ampliado (derogación, breaking, quién acepta, excepción con caducidad) está en [13-enmienda-excepciones-ciclo-de-vida.md](13-enmienda-excepciones-ciclo-de-vida.md) (Approved) y [ADR-002](../architecture/decisions/ADR-002-gobernanza-del-metodo.md) (Aceptado). Las cuatro viñetas de esta sección siguen vigentes; H13 las desarrolla. «Director técnico» no está definido; ver H13 §2.

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
