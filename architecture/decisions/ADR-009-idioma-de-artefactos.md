# ADR-009 — Idioma fijo de los artefactos de ingeniería

| Campo | Valor |
|--------|--------|
| Estado | Aceptado |
| Fecha | 2026-10-12T18:23+02:00 |
| Decisores | Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS) |
| Aceptación | 2026-10-12T18:37+02:00, por Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS). El agente transcribe la aceptación dada en el encargo; no la autodeclara ([H00 §3.3](../../handbook/00-preface.md)). |
| Relacionado | [H02 §2.12](../../handbook/02-engineering-principles.md) (castellano para artefactos de ingeniería), [H03 §6](../../handbook/03-repository-organization.md) (idioma y nombres), [esquema de config](../../sdaf.config.schema.yaml), [ADR-001](ADR-001-nucleo-reutilizable.md), [ADR-006](ADR-006-ciclo-de-vida-de-adrs.md), [plan de la iniciativa](../../docs/iniciativas/INIT-arquitectura.md) (decisión D-8) |

## Contexto

El core fija hoy `project.language: es`: el esquema de configuración declara `const: es`, los ejemplos lo usan y [H02 §2.12](../../handbook/02-engineering-principles.md) exige castellano en los artefactos de ingeniería. Es una decisión deliberada, pero ningún ADR ni capítulo recoge por qué se fija ni quién puede cambiarla. Solo vive en el plan de la iniciativa, que no es constitución: no es citable por un consumidor ni sustituible por el ciclo de vida de [ADR-006](ADR-006-ciclo-de-vida-de-adrs.md).

Sin un registro citable, quien quiera abrir otro idioma no sabe qué decisión revisa, y quien lo evite no puede remitir a una fuente estable.

## Decisión

1. **Castellano neutro.** Los artefactos de ingeniería del método y de los consumidores que adoptan el core se escriben en castellano neutro: commits, PRs, specs, ADRs, prompts, worklogs y handbook.
2. **Un solo valor admitido.** `project.language` solo admite `es` mientras el core no soporte otros idiomas. Cualquier otro código queda fuera de la configuración válida.
3. **Alcance acotado.** La restricción no traduce el código fuente ni los identificadores: eso lo decide el ADR de coding standards del consumidor o el pack.
4. **Cómo se abre otro idioma.** Admitir otro idioma exige un ADR nuevo que sustituya a este ([ADR-006](ADR-006-ciclo-de-vida-de-adrs.md)) y que declare el alcance del soporte: handbook, prompts, validadores y plantillas.

## Alternativas consideradas

- **Abrir internacionalización.** Rechazada: multiplica el mantenimiento de handbook, prompts y validadores con un solo mantenedor, y no hay demanda registrada.
- **Idioma configurable sin soporte.** Rechazada: promete lo que el core no valida; un código distinto de `es` pasaría por válido sin que ningún artefacto del método lo respaldara.
- **Dejarlo implícito en la regla de castellano.** Rechazada: la regla describe la práctica, no la restricción de configuración; no es citable ni sustituible como decisión.

## Consecuencias

- El esquema de configuración, los ejemplos y las reglas de IDE siguen como están. La nota del esquema enlaza este ADR.
- No cambia ningún capítulo del handbook ni ningún gate.
- Es reversible por un ADR sustituto ([ADR-006](ADR-006-ciclo-de-vida-de-adrs.md)); mientras tanto, el valor `es` es el único válido.
- Los consumidores que necesiten otro idioma para su código lo resuelven en su propio ADR de coding standards, sin tocar esta restricción.
