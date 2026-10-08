# 14 — Descripción de arquitectura

> Andamiaje (cabecera, TOC, Relacionado, Historial): `_meta/14-architecture-description.yaml`.

## 1. Propósito

Definir la **línea base arquitectónica** del consumidor: una descripción versionada de la arquitectura vigente del sistema.

Cierra el vacío que presuponen G0.3 ([H05](05-development-workflow.md)) y QG-Arch ([H10 §4](10-code-review-and-quality-gates.md)): ambos remiten a «límites» y «dependencias» sin un artefacto que diga cuáles son. Con ADRs acumulados, la arquitectura vigente solo se reconstruiría leyendo todos en orden; la línea base la declara en un único sitio.

Este capítulo **no** impone estilo, notación ni stack. Decisión de origen: [ADR-005](../architecture/decisions/ADR-005-linea-base-arquitectonica.md).

## 2. Dónde vive

- Ruta: `architecture/description.md` en el repo del consumidor.
- Si crece, se permite la carpeta `architecture/description/` con un índice en `architecture/description.md`. El índice conserva la versión, el estado y el historial de la línea base completa.
- Plantilla: [`templates/architecture-description.md`](../templates/architecture-description.md). El consumidor la copia y la rellena.

## 3. Contenido mínimo

La línea base declara, con nombres estables:

| N.º | Sección | Qué declara |
|-----|---------|-------------|
| 1 | Contexto del sistema | El sistema y los actores o sistemas externos con los que se relaciona |
| 2 | Unidades | Cada unidad arquitectónica: nombre, responsabilidad y tipo libre (módulo, capa, servicio, bounded context…) |
| 3 | Reglas de dependencia | Qué unidad puede depender de cuál, como permitido o prohibido, y cómo se verifica (manual o test) |
| 4 | Integraciones y contratos | Las interfaces entre unidades o con terceros, enlazando las specs que las definen |
| 5 | Atributos de calidad | Los atributos priorizados, cada uno con al menos un escenario medible, enlazando las specs de producto |
| 6 | Decisiones vigentes | Índice de los ADRs Aceptados y no sustituidos que configuran la arquitectura ([ADR-006](../architecture/decisions/ADR-006-ciclo-de-vida-de-adrs.md)) |
| 7 | Riesgos y deuda | Riesgos y deuda arquitectónica conocidos |

Una sección puede escribirse `N/A: <motivo>`. Una línea base de una página es conforme.

## 4. Relación con ADRs, specs y handbook de producto

- El **ADR** registra una decisión y su porqué. La línea base describe el **estado vigente** que resulta de esas decisiones y no duplica el razonamiento: enlaza al ADR.
- La **spec** ([H04](04-specification-standard.md)) define qué debe cumplirse. La línea base enlaza las specs de integración y de calidad; no las reemplaza.
- El **estilo arquitectónico** es un ADR del consumidor. La línea base lo refleja en sus unidades y reglas de dependencia, pero el core no lo fija.
- **Trazabilidad:** las specs y los PBIs declaran las unidades afectadas con los nombres de la línea base ([ADR-005](../architecture/decisions/ADR-005-linea-base-arquitectonica.md) §7, [H08 §7](08-agent-traceability.md)).

## 5. Estados y aprobación

La línea base tiene versión, estado y historial.

| Estado | Significado |
|--------|-------------|
| Draft | Borrador; orienta, pero no satisface el requisito de Gate 0 de §7 |
| Approved | Línea base vigente; la aprueba un humano ([H00 §3.3](00-preface.md)) |

Ningún agente declara Approved. El agente redacta y propone; quien acepta es la identidad humana que el consumidor designe.

## 6. Cuándo cambia

Exigen un ADR Aceptado y una **versión nueva** de la línea base:

- añadir, retirar o renombrar una unidad;
- cambiar una regla de dependencia;
- cambiar una integración;
- cambiar la prioridad de un atributo de calidad.

Corregir redacción o enlaces no lo exige: se anota en el historial sin ADR. Cuando un ADR deja de estar vigente ([ADR-006](../architecture/decisions/ADR-006-ciclo-de-vida-de-adrs.md)), la sección 6 de la línea base se actualiza.

## 7. Gate 0 y QG-Arch

- **G0.6:** línea base Approved presente en el consumidor.
- **G0.3** se evalúa contra la línea base: un cambio «toca límites» si produce alguno de los cambios de §6.
- **QG-Arch** verifica las reglas de dependencia de la línea base. Si esta no declara reglas, QG-Arch es `N/A` con el motivo en el worklog.

> [!NOTE]
> Estos requisitos se definen en [H05](05-development-workflow.md) y [H10](10-code-review-and-quality-gates.md) para la línea de constitución `0.5.0`, que es opt-in. Quien se quede en `0.4.x` no está obligado a mantener una línea base.

## 8. Prueba de abstracción

Ninguna norma de este capítulo nombra un estilo arquitectónico, una notación, un stack ni un producto. Lo concreto vive en los ADRs del consumidor o en los packs: el estilo, la forma de documentar cada unidad y la herramienta con la que se verifican las reglas de dependencia.

## 9. Migración desde un consumidor existente

Un consumidor que ya tiene ADRs construye la línea base a partir de los ADRs vigentes: lista las unidades y reglas que esos ADRs ya establecen y los enlaza en la sección de decisiones. No se reescriben ADRs ([H08 §7](08-agent-traceability.md)). Lo que ningún ADR establece se escribe `N/A: <motivo>` hasta que una decisión lo cubra.
