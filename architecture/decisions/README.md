# ADRs del método (sdaf-core)

Esta carpeta guarda las decisiones de **gobernanza del núcleo**, no las de un producto.

El árbol normativo del **consumidor** sigue exigiendo `architecture/decisions/` para sus ADRs de stack y límites ([H03 §2](../../handbook/03-repository-organization.md)). Este core numera sus ADRs desde 001. Los historiales hasta `v0.3.3` citan «ADR-008», un número heredado del laboratorio de origen: equivale a [ADR-001](ADR-001-nucleo-reutilizable.md). Esas filas no se reescriben. El [ADR-008](ADR-008-adopcion-sobre-codigo-existente.md) propuesto en 2026-09-28 es otra decisión; la cita histórica sigue apuntando a ADR-001.

| ADR | Estado | Título | Sustituido por |
|-----|--------|--------|----------------|
| [ADR-001](ADR-001-nucleo-reutilizable.md) | Aceptado | Extracción del núcleo reutilizable | — |
| [ADR-002](ADR-002-gobernanza-del-metodo.md) | Aceptado | Enmienda, excepciones y ciclo de vida | — |
| [ADR-003](ADR-003-formato-de-artefactos.md) | Aceptado | Formato de andamiaje y worklog | — |
| [ADR-004](ADR-004-tooling-externo-de-agentes.md) | Aceptado | Tooling externo de agentes | — |
| [ADR-005](ADR-005-linea-base-arquitectonica.md) | Aceptado | Línea base arquitectónica del consumidor | — |
| [ADR-006](ADR-006-ciclo-de-vida-de-adrs.md) | Aceptado | Ciclo de vida y sustitución de ADRs | — |
| [ADR-007](ADR-007-modelo-de-capas-y-precedencia.md) | Aceptado | Modelo de capas del método y precedencia | — |
| [ADR-008](ADR-008-adopcion-sobre-codigo-existente.md) | Propuesto | Adopción del método sobre código existente | — |

Estados válidos: Propuesto, Aceptado, Rechazado, Sustituido y Deprecado. Su ciclo de vida y la sustitución están en [ADR-006](ADR-006-ciclo-de-vida-de-adrs.md).

Ningún agente marca un ADR como Aceptado ([H00 §3.3](../../handbook/00-preface.md)). ADR-001, 002 y 003 los aceptó un humano el 2026-09-24, y ADR-004 el 2026-09-26; cada ADR registra quién. ADR-005 lo aceptó un humano el 2026-10-03, y ADR-006 y ADR-007 el 2026-10-07. ADR-008 está Propuesto y pendiente de decisión humana.
