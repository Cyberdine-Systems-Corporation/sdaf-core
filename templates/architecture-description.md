# Descripción de arquitectura (plantilla)

| Campo | Valor |
|--------|--------|
| Versión | 0.1.0 |
| Estado | Draft |
| Fecha | YYYY-MM-DDThh:mm±hh:mm |
| Norma | H14 (handbook del método) |

> Copia esta plantilla a `architecture/description.md`. Rellena cada sección o escribe `N/A: <motivo>`, y borra los ejemplos. Una línea base de una página es conforme. Solo un humano pasa el estado a Approved.

---

## 1. Contexto del sistema

Declara el sistema y los actores o sistemas externos con los que se relaciona.

| Elemento | Tipo | Relación con el sistema |
|----------|------|-------------------------|
| Sistema | Sistema descrito | Nombre y propósito en una frase |
| Actor externo 1 | Persona | Qué hace con el sistema |
| Actor externo 2 | Sistema de terceros | Qué intercambia con el sistema |

`N/A: <motivo>`

---

## 2. Unidades

Declara cada unidad arquitectónica con un nombre estable. El tipo es libre.

| Unidad | Tipo | Responsabilidad |
|--------|------|-----------------|
| Unidad A | Tipo libre | Qué hace y qué no hace |
| Unidad B | Tipo libre | Qué hace y qué no hace |

`N/A: <motivo>`

---

## 3. Reglas de dependencia

Declara qué unidad puede depender de cuál. Cada regla es permitida o prohibida y dice cómo se verifica.

| Desde | Hacia | Regla | Cómo se verifica |
|-------|-------|-------|------------------|
| Unidad A | Unidad B | Permitida | Manual |
| Unidad B | Unidad A | Prohibida | Test |

`N/A: <motivo>` (si no hay reglas, QG-Arch es `N/A` con motivo en el worklog).

---

## 4. Integraciones y contratos

Declara las interfaces entre unidades o con terceros y enlaza la spec que define cada contrato.

| Origen | Destino | Contrato | Spec |
|--------|---------|----------|------|
| Unidad A | Unidad B | Qué se intercambia | SPEC-XXX-000 |
| Unidad B | Actor externo 2 | Qué se intercambia | SPEC-XXX-000 |

`N/A: <motivo>`

---

## 5. Atributos de calidad

Declara los atributos priorizados. Cada uno lleva al menos un escenario medible y la spec de producto que lo recoge.

| Atributo | Prioridad | Escenario (fuente, estímulo, entorno, respuesta, medida) | Spec |
|----------|-----------|----------------------------------------------------------|------|
| Atributo 1 | 1 | Fuente: Actor externo 1. Estímulo: acción. Entorno: condición. Respuesta: resultado. Medida: umbral | SPEC-XXX-000 |
| Atributo 2 | 2 | Fuente, estímulo, entorno, respuesta y medida | SPEC-XXX-000 |

`N/A: <motivo>`

---

## 6. Decisiones vigentes

Indexa los ADRs Aceptados y no sustituidos que configuran la arquitectura. No copies su razonamiento: enlázalo.

| ADR | Decisión | Unidades afectadas |
|-----|----------|--------------------|
| ADR-NNN | Una frase | Unidad A |
| ADR-NNN | Una frase | Unidad A, Unidad B |

`N/A: <motivo>`

---

## 7. Riesgos y deuda

Declara los riesgos y la deuda arquitectónica conocidos.

| Riesgo o deuda | Unidades afectadas | Mitigación o plan |
|----------------|--------------------|-------------------|
| Descripción breve | Unidad A | Qué se hará y cuándo se revisa |

`N/A: <motivo>`

---

## 8. Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.1.0 | 2026-10-08T08:19+02:00 | Borrador inicial |
