# Contribuir a sdaf-core

## Norma

La constitución está en [`handbook/`](handbook/README.md). Cómo se enmienda está en [`handbook/13-enmienda-excepciones-ciclo-de-vida.md`](handbook/13-enmienda-excepciones-ciclo-de-vida.md) (Approved) y [ADR-002](architecture/decisions/ADR-002-gobernanza-del-metodo.md) (Aceptado), que desarrollan [H00 §3](handbook/00-preface.md).

## Qué no hace un agente

No marca un capítulo como Approved ni un ADR como Aceptado ([H00 §3.3](handbook/00-preface.md)). No abre commit, push, PR, tag, release ni merge salvo que el encargo vigente lo nombre ([H06 §7](handbook/06-ai-agent-framework.md)).

## Cómo proponer una enmienda

1. PR con la clase marcada en [`.github/pull_request_template.md`](.github/pull_request_template.md): **significado** o **redacción** (H13 §6).
2. Si el cambio es de significado de un capítulo Approved: bump declarado, fila en [`handbook/CHANGELOG.md`](handbook/CHANGELOG.md), worklog si el cambio es material ([H08 §5](handbook/08-agent-traceability.md)).
3. Revisión humana nominada del merge ([H10](handbook/10-code-review-and-quality-gates.md)): la identidad está en [`CODEOWNERS`](CODEOWNERS).

## Commits

Castellano. Prefijo corto opcional (`docs:`, `fix:`, `feat:`) más el porqué. Distinguir norma (significado) de redacción.

## Cómo publicar una release

La publica una persona con permiso sobre `main` y los tags. Un agente prepara y propone, pero no crea el tag ni la Release salvo orden expresa ([H06 §7](handbook/06-ai-agent-framework.md)). Orden de cierre:

1. **Preparación.** PR a `main` (o cadena de PRs si el cambio es incompatible) con la entrada nueva de [`handbook/CHANGELOG.md`](handbook/CHANGELOG.md) (versiones finales, si rompe o no citas, migración), el `CHANGELOG.md` raíz, el README y la sección de la línea en [`docs/adopcion-y-upgrade.md`](docs/adopcion-y-upgrade.md). Aún no cambian el badge, el pin recomendado ni los tags publicados: los textos dicen «se crea tras el merge». Si la release abre una línea de constitución nueva, antes del tag se hace un piloto sobre un consumidor real; sus hallazgos entran al core como cambios genéricos, sin citar ese consumidor.
2. **Tag anotado** `vX.Y.Z` sobre el commit de la fusión en `main`, con mensaje `sdaf-core X.Y.Z: …`. Al publicar el tag, [`docs-deploy`](.github/workflows/docs-deploy.yml) despliega esa versión de la documentación.
3. **GitHub Release** sobre ese tag, con título `sdaf-core X.Y.Z` y como notas la entrada del CHANGELOG sin enlaces relativos. Es imprescindible: el chip de versión del encabezado de la documentación lee la última Release de GitHub, no los tags, y sin ella sigue mostrando la anterior. Comando: `gh release create vX.Y.Z --verify-tag --title "sdaf-core X.Y.Z" --notes-file <notas> --latest`.
4. **Chore de publicación.** PR `chore: preparar la publicación de vX.Y.Z` con el badge, el pin recomendado, los tags publicados y la referencia `validate-sdaf@vX.Y.Z` del README de la action; se retira «se crea tras el merge».
5. **Limpieza.** Borrar las ramas ya fusionadas, en local y en remoto, tras comprobar que están contenidas en `main`.
6. **Plan.** Si la release cierra PBIs de una iniciativa, actualizar su plan en [`docs/iniciativas/`](docs/iniciativas/README.md).

## Seguridad

Avisos de **este** repo: [`SECURITY.md`](SECURITY.md). La plantilla de reporte del consumidor es [`templates/security.md`](templates/security.md).
