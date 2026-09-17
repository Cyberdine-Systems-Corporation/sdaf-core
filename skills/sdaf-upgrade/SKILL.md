---
name: sdaf-upgrade
description: Actualiza el pin de sdaf-core en un consumidor (tag, sdaf.version, AGENTS.md, citas). Usar al subir de versión del método.
---

# sdaf-upgrade

| Campo | Valor |
|--------|--------|
| ID | sdaf-upgrade |
| Versión | 0.2.0 |
| Estado | Approved |
| Prioridad | media |
| Fecha | 2026-08-25 |
| Norma | [docs/adopcion-y-upgrade.md](../../docs/adopcion-y-upgrade.md), [handbook/CHANGELOG.md](../../handbook/CHANGELOG.md) |

## Disparadores

- “Upgrade sdaf-core”, “subir a 0.2.0”, “actualizar submodule del método”.

## Pasos

1. Actualizar pin del submodule/tag al nuevo `vX.Y.Z` (o copiar el árbol si el mecanismo es template).
2. Leer [`handbook/CHANGELOG.md`](../../handbook/CHANGELOG.md) de la versión destino.
3. Actualizar `sdaf.version` en `sdaf.config.yaml`.
4. Si cambió [`AGENTS.md.template`](../../AGENTS.md.template), regenerar `AGENTS.md` (conservar fusiones/activos del consumidor).
5. Revisar citas `skill-id@version` en worklogs nuevos; remapear capítulos si el CHANGELOG indica breaking (tabla 0.1→0.2 en docs).
6. **No** auto-migrar specs, knowledge ni handbook de producto del consumidor.
7. Registrar `sdaf-upgrade@0.2.0` en worklog.

## Definition of Done

- [ ] Pin y `sdaf.version` alineados.
- [ ] CHANGELOG revisado; breaking de citas aplicados si aplica.
- [ ] `AGENTS.md` coherente con plantilla y config.
- [ ] Worklog de upgrade cerrado.

## Restricciones

- No aprobar norma ni specs.
- No reescribir historia git del consumidor sin orden humana.

## Relacionado

| Destino | Por qué |
|---------|---------|
| [docs/adopcion-y-upgrade.md](../../docs/adopcion-y-upgrade.md) | Checklist de upgrade |
| [handbook/CHANGELOG.md](../../handbook/CHANGELOG.md) | Breaking y parches |

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.2.0 | 2026-08-25 | Primera versión en el core |
