# ADR-007 — Modelo de capas del método y precedencia

| Campo | Valor |
|--------|--------|
| Estado | Propuesto |
| Fecha | 2026-09-28T18:08+02:00 |
| Decisores | Manuel Ortiz de Villajos Quirós (@mortiz-iadev, CODEOWNERS) |
| Relacionado | [H01](../../handbook/01-sdaf-framework.md), [H05](../../handbook/05-development-workflow.md), [contrato de pack](../../docs/contrato-pack-stack.md), [adopción y upgrade](../../docs/adopcion-y-upgrade.md), [esquema de config](../../sdaf.config.schema.yaml), [ADR-004](ADR-004-tooling-externo-de-agentes.md), [ADR-005](ADR-005-linea-base-arquitectonica.md), [worklog](../../worklogs/INIT-arquitectura/Iteration-001.md) |

## Contexto

En la práctica un repo consumidor combina tres capas: el core, un pack de stack y un overlay de producto (por ejemplo, un overlay de adopción con `sdaf-core` y `sdaf-stack-dotnet` como submodules). El core solo formaliza las dos primeras, y de forma incompleta:

- **Precedencia incoherente.** El diagrama de [H01 §3](../../handbook/01-sdaf-framework.md) y el flujo de [H05 §2](../../handbook/05-development-workflow.md) ponen las specs antes que los ADRs, pero la prioridad ante conflicto (H01 §3.2) pone los ADRs por encima de las specs. No se resuelve qué ocurre si una spec Approved exige algo que un ADR Aceptado prohíbe.
- **El pack no tiene lugar en la precedencia.** H01 §3.2 no lo menciona, mientras que el tooling externo sí tiene cláusula de precedencia ([ADR-004](ADR-004-tooling-externo-de-agentes.md)).
- **Un solo pack.** `stack.pack` es un escalar; no se pueden componer dos packs (por ejemplo, backend y frontend).
- **Contrato de pack sin compatibilidad ni manifiesto.** El pack no declara con qué líneas del core es compatible ni qué ids aporta de forma legible por máquina. El cumplimiento es «el consumidor debe corregir el pack».
- **Colisiones sin regla.** No está definido qué ocurre si core, pack y overlay aportan una skill, un contrato o un prompt con el mismo id.
- **Materialización fuera del core.** El script de referencia de materialización vive en un repo consumidor ([adopción y upgrade](../../docs/adopcion-y-upgrade.md)); el core depende de un consumidor para su propia distribución.
- **Topología plana.** `stack.src_path` y `stack.tests_path` son rutas únicas: un monorepo o un sistema con varios desplegables no se puede representar, y `check-worklog-presence.py` no ve el código fuera de esas rutas.

## Decisión

1. **Tres capas de método.**
   - **Core**: constitución del método (este repo).
   - **Packs** (0..n): playbooks de stack que cumplen el contrato de pack.
   - **Overlay del consumidor**: handbook de producto, línea base y ADRs ([ADR-005](ADR-005-linea-base-arquitectonica.md)), specs, `AGENTS.md` y artefactos locales (contratos, prompts, skills).

   El tooling externo sigue fuera del modelo, como capa de entorno subordinada ([ADR-004](ADR-004-tooling-externo-de-agentes.md)).
2. **Precedencia única** (sustituye a H01 §3.2; pendiente de la decisión D-3 del [plan de la iniciativa](../../docs/iniciativas/INIT-arquitectura.md)):
   1. Handbook del core, capítulos Approved.
   2. Handbook de producto Approved.
   3. Línea base Approved y ADRs vigentes del consumidor **junto con** specs Approved. No se ordenan entre sí: la spec manda sobre *qué* debe cumplirse y el ADR sobre *cómo* se construye. Un conflicto entre ambos es **STOP** y se resuelve enmendando uno de los dos; nunca en silencio durante la implementación.
   4. Packs. Un pack no contradice capas superiores; si choca con un ADR del consumidor, gana el ADR y la skill del pack se marca `N/A: <motivo>` en el worklog.
   5. Backlog.
   6. Prompts, skills locales, worklogs e implementación.
3. **Manifiesto de pack.** Cada pack publica `sdaf-pack.yaml` con: `id`, `version`, `core` (rango semver de líneas de constitución compatibles, p. ej. `">=0.5.0 <0.7.0"`), `provides` (ids de extensión, skills y prompts) y `requires` (otros packs, opcional). Schema validable en el core.
4. **Varios packs.** La config admite `stack.packs` (lista de `id@version`). `stack.pack` se mantiene como alias de un solo elemento, marcado como obsoleto (decisión D-6 del [plan de la iniciativa](../../docs/iniciativas/INIT-arquitectura.md)).
5. **Resolución por id.**
   - Los ids de agente del núcleo no se sustituyen desde un pack ni desde el overlay. El overlay puede añadir prompts adicionales y contexto autorizado, no reemplazar el prompt base.
   - Un mismo id aportado por dos packs, o por un pack y el overlay, es error de validación, salvo sustitución explícita del overlay sobre un id de **extensión** declarada en la config.
   - Las skills de pack mantienen el prefijo de stack del contrato vigente.
6. **Validación.** `validate-config.py` comprueba el rango `core` de cada pack frente a `sdaf.version`, las colisiones de ids y el invariante I4 con todos los packs.
7. **Materialización en el core.** El core publica el contrato de materialización (orden core → packs → overlay, symlinks relativos, copia como fallback con marca de origen) y un script de referencia multiplataforma en `scripts/`. Revisa la exclusión «CLI de materialización» de la línea 0.3.x.
8. **Topología.** La config admite `stack.units`: lista de unidades con `name`, `src` y `tests`. Sus nombres coinciden con las unidades de la línea base ([ADR-005](ADR-005-linea-base-arquitectonica.md)). `src_path` y `tests_path` siguen siendo el atajo de una sola unidad. Los scripts que hoy leen `src_path` usan todas las unidades.
9. **Versionado.** Los puntos 3 a 8 cambian el contrato de pack y el esquema de config: línea de constitución nueva y opt-in (`0.6.0`). El punto 2 entra antes, en `0.5.0`, porque [ADR-005](ADR-005-linea-base-arquitectonica.md) necesita la precedencia resuelta.

## Alternativas consideradas

- **Mantener un pack y un overlay informal.** Cada consumidor resuelve colisiones y precedencia a su manera; es lo que ADR-004 evitó para el tooling externo.
- **Precedencia estricta ADR > spec** (H01 §3.2 actual). Permite que una decisión técnica anule en silencio un comportamiento aprobado por negocio.
- **Precedencia estricta spec > ADR.** Permite que una spec imponga una solución técnica sin decisión registrada.
- **El overlay puede sustituir cualquier artefacto del core.** Rompe la garantía de que los capítulos Approved no se contradicen.
- **Fusionar packs como subtree en el consumidor.** Pierde la identidad y la versión del pack.

## Consecuencias

- Cambian H01 §3, el contrato de pack, `sdaf.config.schema.yaml` y `.json`, `validate-config.py`, `check-worklog-presence.py`, `sdaf-bootstrap`, `sdaf-upgrade`, `AGENTS.md.template`, `docs/adopcion-y-upgrade.md` y `examples/` (escenarios nuevos de varios packs y varias unidades).
- `sdaf-stack-dotnet` necesita una release con `sdaf-pack.yaml`; hasta entonces el validador trata la ausencia de manifiesto como aviso.
- El overlay de adopción existente sirve de piloto externo; no se cita como norma en el core.
- La materialización deja de depender de un script de un consumidor.
