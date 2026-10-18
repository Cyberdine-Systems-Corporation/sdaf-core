---
pbi: INIT-arquitectura
iteracion: Iteration-023
fecha: 2026-10-18
inicio: 2026-10-18T19:20:00+02:00
fin: 2026-10-18T19:56:00+02:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargos del humano en la sesión: cerrar v0.5.1 (preparación, tag, GitHub Release, chore de publicación y limpieza de ramas) y completar lo diferido en un parche v0.5.2 («Lo hacemos ahora», 2026-10-18)."
contexto: "Parche de línea v0.5.2: completa lo diferido de v0.5.1 para la adopción sobre código existente (ADR-008 Aceptado): catálogo de H06, tabla de worklog de H08, Gate 0 y bootstrap."
especificaciones_utilizadas: "ADR-008; handbook/05 §3 y §8; handbook/13 §3; handbook/06 §6; handbook/08 §5; docs/iniciativas/INIT-arquitectura.md (bloque 5)"
archivos_leidos: "ADR-008; handbook/06 y 08 con sus sidecars; handbook/index.yaml; skills/sdaf-gate0, skills/sdaf-bootstrap y skills/sdaf-adopt-existing; skills/README.md; AGENTS.md.template; worklog Iteration-022 y plantilla de worklog; preparación de v0.5.1 (cb369ed y 2357e82); docs/adopcion-y-upgrade.md; plan de la iniciativa"
archivos_modificados: "handbook/06 y 08 (con sus handbook/_meta/*.yaml) y handbook/index.yaml; skills/sdaf-gate0/SKILL.md y skills/sdaf-bootstrap/SKILL.md; handbook/CHANGELOG.md, CHANGELOG.md y README.md; docs/adopcion-y-upgrade.md; docs/iniciativas/INIT-arquitectura.md (plan 0.1.21) y docs/iniciativas/README.md; este worklog."
origen_cambios: "Capítulos, skills, changelogs, guía y plan: redacción de subagentes escritores delegados, revisada por el orquestador; ver cuerpo."
resultado: "Contenido de v0.5.2 listo en rama local, pendiente de revisión y de publicación: commit del contenido (6390201) y este segundo commit con la preparación de la release, el worklog y el plan. La skill sdaf-adopt-existing sigue en Draft."
tiempo: PT30M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "El inicio (19:20) es aproximado: justo tras fusionar el PR #50. El tiempo es una estimación de trabajo activo y es menor o igual que la diferencia entre fin e inicio (hubo esperas entre pasos). Sin piloto (parche): la verificación son los checks del repo. Sin push ni PR salvo orden posterior."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (revisar; push y PR solo con orden; después preparación de la release)
commit: null
pr: null
rama: docs/completar-adopcion-v0.5.2
sha: null
resumen_acumulado: "ad hoc — v0.5.2 / lo diferido de v0.5.1 en rama local, pendiente de revisión; sin PR/tag"
---

# INIT-arquitectura / Iteration-023

## Línea de decisión

- `v0.5.1` queda cerrada con tag y GitHub Release confirmados expresamente por el humano (#50, #51 y #52).
- Decisión N (2026-10-18, antes de las 19:44+02:00; la hora exacta no se registró): el humano decide completar lo diferido en un parche («Lo hacemos ahora»). Entrega en un PR a `main` con dos commits: contenido y preparación.
- Bumps: H08 `0.5.0` (minor: la fila nueva de §5 es normativa, obliga a abrir worklog), H06 `0.3.5` (patch: catálogo, sin cambio de norma), `sdaf-gate0` `0.4.0` (minor: comportamiento nuevo en el perímetro heredado; Gate 0 no cambia en el gobernado) y `sdaf-bootstrap` `0.5.1` (patch: derivación).
- Siguen abiertas la aprobación de la skill `sdaf-adopt-existing` (decisión M) y la adopción en el consumidor del piloto (decisión K). Los agentes no aceptan ni aprueban ([H00 §3.3](../../handbook/00-preface.md)): la skill sigue en Draft.
- La Definition of Done de la iniciativa sigue en 2 de 6 casillas.

## Pruebas

`check-version-metadata.py`, `check-history-append-only.py`, `check-adrs.py`, `test-adrs.py`, `measure-handbook-scaffolding.py`, `validate-config.py`, `validate-examples.py`, `validate-worklog.py` (Iteration-001 a 023) y `check-local-links.py --strict-anchors --strict-orphans` sobre copia limpia. markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | Redacción IA revisada; sin ejecutable nuevo. |
