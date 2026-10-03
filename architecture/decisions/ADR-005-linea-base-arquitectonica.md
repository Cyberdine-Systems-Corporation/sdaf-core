# ADR-005 — Línea base arquitectónica del consumidor

| Campo | Valor |
|--------|--------|
| Estado | Aceptado |
| Fecha | 2026-09-28T18:08+02:00 |
| Decisores | Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS) |
| Aceptación | 2026-10-03T11:01+02:00, por Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS). El agente transcribe la aceptación dada en el encargo; no la autodeclara ([H00 §3.3](../../handbook/00-preface.md)). |
| Relacionado | [H01](../../handbook/01-sdaf-framework.md), [H03](../../handbook/03-repository-organization.md), [H04](../../handbook/04-specification-standard.md), [H05](../../handbook/05-development-workflow.md), [H10](../../handbook/10-code-review-and-quality-gates.md), [contrato del Architecture Agent](../../agents/architecture-agent.md), [ADR-006](ADR-006-ciclo-de-vida-de-adrs.md), [ADR-007](ADR-007-modelo-de-capas-y-precedencia.md), [worklog](../../worklogs/INIT-arquitectura/Iteration-001.md) |

## Contexto

El core trata la arquitectura solo como un conjunto de decisiones (ADRs), pero varias normas Approved presuponen una **descripción** de la arquitectura que ningún artefacto define:

- [H10 §3.2](../../handbook/10-code-review-and-quality-gates.md) exige respetar «dependencias y límites del ADR de arquitectura del consumidor».
- QG-Arch ([H10 §4](../../handbook/10-code-review-and-quality-gates.md)) bloquea «violaciones nuevas de dependencia» sin decir dónde están declaradas las dependencias permitidas.
- G0.3 ([H05 §3](../../handbook/05-development-workflow.md)) exige ADR «si el cambio toca límites», sin artefacto que diga cuáles son los límites.
- El prompt del Architecture Agent lee la «arquitectura de solución, si existe».
- [H04 §3](../../handbook/04-specification-standard.md) menciona NFRs de producto, pero §5 no les da contenido mínimo: las decisiones arquitectónicas no tienen atributos de calidad medibles contra los que evaluarse.
- La cadena de trazabilidad ([H08 §6](../../handbook/08-agent-traceability.md)) no vincula una spec o un PBI con la parte del sistema que lo implementa.

Sin ese artefacto, G0.3 y QG-Arch no son auditables: dependen del juicio de quien revisa, que es justo lo que el método quiere evitar. Además, con ADRs acumulados, la arquitectura vigente solo puede reconstruirse leyendo todos los ADRs en orden.

El contrato del Architecture Agent también fija como norma que «el dominio no dependa de infra/UI», que presupone un estilo arquitectónico concreto sin ADR que lo decida.

## Decisión

1. **Artefacto.** Todo consumidor que adopte la línea de constitución que incluya este ADR mantiene una **línea base arquitectónica**: una descripción de la arquitectura vigente, versionada, en `architecture/description.md` (ruta fijada por la decisión D-2 del [plan de la iniciativa](../../docs/iniciativas/INIT-arquitectura.md), cerrada el 2026-10-02).
2. **Contenido mínimo, neutral de estilo.** La línea base declara, con nombres estables:
   1. contexto del sistema y actores o sistemas externos;
   2. **unidades** arquitectónicas (nombre, responsabilidad y tipo libre: módulo, capa, servicio, bounded context…);
   3. **reglas de dependencia** entre unidades, expresadas de forma verificable (permitido o prohibido), manual o por test;
   4. integraciones y contratos entre unidades o con terceros, enlazando las specs que los definen;
   5. **atributos de calidad** priorizados, cada uno con al menos un escenario medible, enlazando las specs de producto;
   6. índice de **decisiones vigentes**: ADRs Aceptados y no sustituidos que la configuran ([ADR-006](ADR-006-ciclo-de-vida-de-adrs.md));
   7. riesgos y deuda arquitectónica conocidos.

   Una sección puede escribirse `N/A: <motivo>`. Una línea base de una página es conforme.
3. **Sin estilo ni notación impuestos.** El core no fija estilo (capas, hexagonal, microservicios…), notación (C4, arc42, UML…) ni stack. El estilo es un ADR del consumidor; la línea base lo refleja.
4. **Ciclo de vida.** La línea base tiene versión, estado `Draft` o `Approved` e historial. Solo un humano la aprueba ([H00 §3](../../handbook/00-preface.md)). Añadir, retirar o renombrar una unidad, o cambiar una regla de dependencia, una integración o la prioridad de un atributo de calidad, exige un ADR Aceptado y una nueva versión de la línea base.
5. **Gate 0.** Nuevo requisito G0.6: línea base Approved presente. G0.3 se evalúa contra ella: un cambio «toca límites» si produce alguno de los cambios del punto 4.
6. **QG-Arch.** Verifica las reglas de dependencia de la línea base. Si la línea base no declara reglas, QG-Arch es `N/A` con motivo en el worklog.
7. **Trazabilidad.** Specs y PBIs declaran las **unidades** afectadas con los nombres de la línea base.
8. **Architecture Agent.** Sus salidas pasan a ser ADRs y línea base. Deja de aplicar «dominio sin infra/UI» como norma del core: aplica las reglas de dependencia que declare la línea base.
9. **Versionado del método.** Añadir G0.6 cambia el significado de un gate de forma incompatible ([H13 §5](../../handbook/13-enmienda-excepciones-ciclo-de-vida.md)): entra en una línea de constitución nueva y opt-in (`0.5.0`). Quien se quede en `0.4.x` no está obligado.

## Alternativas consideradas

- **Mantener solo ADRs.** No resuelve la auditabilidad de G0.3 ni de QG-Arch, y obliga a reconstruir la arquitectura vigente leyendo todos los ADRs.
- **Imponer una notación o plantilla externa (arc42, C4).** Estatiza el core a una forma concreta de documentar; el método debe servir a cualquier adopción.
- **Sección de arquitectura dentro del handbook de producto.** Mezcla constitución de producto con la descripción técnica, que cambia con otro ritmo y otro revisor.
- **Línea base recomendada, no exigida por Gate 0.** Sin gate, G0.3 y QG-Arch siguen sin ser auditables; sería documentación opcional.

## Consecuencias

- G0.3 y QG-Arch pasan a ser comprobables contra un artefacto; la review arquitectónica deja de depender del recuerdo del revisor.
- Coste inicial para el consumidor: redactar la línea base antes del primer Gate 0 de la línea `0.5.0`. Se mitiga con el mínimo de una página y las secciones `N/A`.
- Migración de consumidores existentes: construir la línea base a partir de sus ADRs vigentes; no se reescriben ADRs ([H08 §7](../../handbook/08-agent-traceability.md)).
- Los packs pueden aportar playbooks para verificar reglas de dependencia (tests de arquitectura del stack) sin que el core los fije.
- Cambian: H01, H03, H04, H05, H10, el contrato y los prompts del Architecture Agent, `adr-propose`, `sdaf-gate0`, `sdaf-bootstrap` y las plantillas (nueva `templates/architecture-description.md`, `templates/pbi.md`).
- Prueba de abstracción: ninguna sección obligatoria nombra un estilo, una notación, un stack ni un producto.
