---
pbi: INIT-arquitectura
iteracion: Iteration-027
fecha: 2026-10-25
inicio: 2026-10-25T18:54:41+01:00
fin: 2026-10-25T18:59:39+01:00
agente: humano + asistente IA (Claude Code, app de escritorio)
modelo: claude-sonnet-5-5
version_prompt: "N/D: encargo ad hoc en Claude Code, sin prompt versionado de prompts/"
prompt_base: ninguno (encargo ad hoc)
prompts_adicionales: ninguno
skills: ninguna
reglas_ide: idioma-castellano
ad_hoc: "Encargo del humano en la sesión: continuar con el siguiente paso del plan tras cerrar ARQ-6.1 («Continua con el siguiente paso», 2026-10-25), que es publicar el parche con ARQ-6.3 y ARQ-6.1."
contexto: "Preparación del parche v0.5.3 de sdaf-core: publica el modo consumidor de check-adrs.py (ARQ-6.3) y las comprobaciones mecánicas de Gate 0 (ARQ-6.1) con sus inputs opt-in de la action validate-sdaf. Solo tooling y docs."
especificaciones_utilizadas: "CONTRIBUTING.md (Cómo publicar una release, paso 1); docs/iniciativas/INIT-arquitectura.md; worklogs Iteration-025 y Iteration-026; preparación de v0.5.2 (d6f3c5e) como modelo"
archivos_leidos: "CONTRIBUTING.md; preparación de v0.5.2 (d6f3c5e y c7b229b); CHANGELOG.md; README.md; handbook/CHANGELOG.md; docs/adopcion-y-upgrade.md; .github/actions/validate-sdaf/README.md; plan de la iniciativa y su índice; worklogs Iteration-023, 025 y 026"
archivos_modificados: "CHANGELOG.md; README.md; handbook/CHANGELOG.md; docs/adopcion-y-upgrade.md; .github/actions/validate-sdaf/README.md; docs/iniciativas/INIT-arquitectura.md (plan 0.1.26) y docs/iniciativas/README.md; este worklog."
origen_cambios: "Changelogs, guía, README de la action, plan y worklog: redacción de un subagente escritor delegado, revisada por el orquestador; ver cuerpo."
resultado: "Preparación de v0.5.3 lista en rama local, pendiente de revisión: entrada 0.5.3 en el CHANGELOG del handbook, última versión en CHANGELOG.md y README, sección 0.5.3 de la guía y textos de disponibilidad concretados (desde v0.5.3, que se crea tras el merge). Badge, pin recomendado y tags publicados no cambian hasta el chore de publicación."
tiempo: PT4M
coste:
  modalidad: suscripcion
  importe: null
  moneda: null
  tokens: null
  fuente: "N/D: la sesión no expone tokens ni consumo; plan de suscripción sin importe por uso"
observaciones: "El tiempo es una estimación de trabajo activo del escritor delegado y es menor o igual que la diferencia entre fin e inicio. Sin piloto (parche de tooling y docs): la verificación son los checks del repo. Sin commit, push ni PR salvo orden posterior. Tag, GitHub Release y chore de publicación se hacen con confirmación expresa del humano."
pruebas_ejecutadas: "Locales sobre el árbol de trabajo: ver cuerpo."
estado: hecho
siguiente_agente: humano (revisar; commit, push y PR solo con orden; después tag, GitHub Release y chore de publicación)
commit: null
pr: null
rama: docs/preparar-v0.5.3
sha: null
resumen_acumulado: "ad hoc — preparación de v0.5.3 (ARQ-6.3 y ARQ-6.1) en rama local, pendiente de revisión; sin PR/tag"
---

# INIT-arquitectura / Iteration-027

## Línea de decisión

- Publicar ARQ-6.3 y ARQ-6.1 como parche `v0.5.3` viene de lo registrado en [Iteration-025](Iteration-025.md) y [Iteration-026](Iteration-026.md): ambos se publicarían juntos en un parche, con tag y Release confirmados aparte por el humano. El número `0.5.3` es la propuesta del plan, no una decisión nueva; la hora de esas decisiones no se registró.
- Es un parche de línea de solo tooling y docs: no cambia capítulos ni skills, no añade gates ni cambia los existentes, y `sdaf.version` sigue en `"0.5.0"`. No hay bumps de capítulos, skills ni plantillas.
- La preparación no cambia el badge, el pin recomendado ni los tags publicados: los textos dicen que `v0.5.3` se crea tras el merge del parche. El README de la action ya queda con `@v0.5.3` y «Disponible desde `v0.5.3`», y la guía concreta «disponible desde `v0.5.3`» donde decía «en la release que lo incluya».
- El plan pasa a `0.1.26` con la fila de historial, «preparado, pendiente de tag» y el índice de iniciativas; no marca PBIs nuevos (siguen 25 de 34).
- Tag, GitHub Release, chore de publicación (badge, pin, tags publicados y retirada de «se crea tras el merge») y limpieza de ramas siguen pendientes y requieren confirmación expresa del humano.

## Pruebas

`check-version-metadata.py`, `check-history-append-only.py`, `check-adrs.py`, `test-adrs.py`, `test-dates.py`, `test-docs.py`, `test-gate0.py`, `test-worklog.py`, `test-validate-config.py`, `measure-handbook-scaffolding.py`, `validate-config.py`, `validate-examples.py`, `validate-worklog.py` (Iteration-027) y `check-local-links.py --strict-anchors --strict-orphans` sobre copia limpia. markdownlint y `mkdocs build --strict` los cubre CI.

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | Redacción IA revisada; sin ejecutable nuevo. |
