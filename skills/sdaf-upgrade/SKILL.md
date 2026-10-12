---
name: sdaf-upgrade
description: Actualiza el pin de sdaf-core en un consumidor (tag, sdaf.version, AGENTS.md, citas). Usar al subir de versión del método.
---

# sdaf-upgrade

| Campo | Valor |
|--------|--------|
| ID | sdaf-upgrade |
| Versión | 0.3.0 |
| Estado | Approved |
| Prioridad | media |
| Fecha | 2026-10-12T18:47+02:00 |
| Norma | [docs/adopcion-y-upgrade.md](../../docs/adopcion-y-upgrade.md), [handbook/CHANGELOG.md](../../handbook/CHANGELOG.md), [H14](../../handbook/14-architecture-description.md) |

## Disparadores

- “Upgrade sdaf-core”, “subir a 0.5.0”, “actualizar submodule del método”.

## Pasos

1. Actualizar pin del submodule/tag al nuevo `vX.Y.Z` (o copiar el árbol si el mecanismo es template).
2. Leer [`handbook/CHANGELOG.md`](../../handbook/CHANGELOG.md) de la versión destino.
3. Actualizar `sdaf.version` en `sdaf.config.yaml`.
4. Si cambió [`AGENTS.md.template`](../../AGENTS.md.template), regenerar `AGENTS.md` (conservar fusiones/activos del consumidor).
5. Revisar citas `skill-id@version` en worklogs nuevos; remapear capítulos si el CHANGELOG indica breaking (tabla 0.1→0.2 en docs).
6. Si el destino es la línea `0.5.0`: leer su sección en la [guía de adopción](../../docs/adopcion-y-upgrade.md); construir o revisar `architecture/description.md` desde los ADRs vigentes ([H14 §9](../../handbook/14-architecture-description.md#9-migración-desde-un-consumidor-existente)) y pedir su aprobación humana (no aprobarla); regenerar `AGENTS.md` desde la plantilla `0.5.0`; adoptar los estados de ADR de [ADR-006](../../architecture/decisions/ADR-006-ciclo-de-vida-de-adrs.md) y los PBIs con [`templates/pbi.md`](../../templates/pbi.md).
7. **No** auto-migrar specs, knowledge ni handbook de producto del consumidor.
8. Registrar `sdaf-upgrade@0.3.0` en worklog.

## Definition of Done

- [ ] Pin y `sdaf.version` alineados.
- [ ] CHANGELOG revisado; breaking de citas aplicados si aplica.
- [ ] `AGENTS.md` coherente con plantilla y config.
- [ ] Si `sdaf.version` pasa a `0.5.0`: línea base Approved o G0.6 declarado como STOP.
- [ ] Worklog de upgrade cerrado.

## Restricciones

- No aprobar norma ni specs.
- No aprobar la línea base.
- No reescribir historia git del consumidor sin orden humana.

## Relacionado

| Destino | Por qué |
|---------|---------|
| [docs/adopcion-y-upgrade.md](../../docs/adopcion-y-upgrade.md) | Checklist de upgrade |
| [handbook/CHANGELOG.md](../../handbook/CHANGELOG.md) | Breaking y parches |
| [H14](../../handbook/14-architecture-description.md) | Línea base arquitectónica que se construye al subir a `0.5.0` |

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.3.0 | 2026-10-12T18:47+02:00 | Salto a la línea `0.5.0`: construir o revisar la línea base desde los ADRs y pedir su aprobación (sin aprobarla); estados de ADR y PBIs con plantilla; DoD y restricción de la línea base |
| 0.2.0 | 2026-08-25 | Primera versión en el core |
