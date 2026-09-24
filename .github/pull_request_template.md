## Resumen

<!-- 1–3 frases. Si tocas capítulos Approved, declara si el significado normativo permanece. -->

## Clase del cambio

- [ ] **Redacción** — el historial puede decir «sin cambio de norma»; bump patch del capítulo si aplica.
- [ ] **Significado** — cambia una obligación de un capítulo Approved; bump y fila en `handbook/CHANGELOG.md` (H13 §6).

## Plan de prueba

- [ ] CI verde (`validate`: config + metadatos + enlaces estrictos + markdownlint).
- [ ] Si el PR toca markdown: checklist [`docs/checklist-pagina-docs.md`](../docs/checklist-pagina-docs.md).
- [ ] Si el diff toca código de producto: worklog bajo `worklogs/`.
- [ ] Si el diff es un cambio material de handbook o ADR: worklog bajo `worklogs/` (H08 §5). Lo comprueba QG-Review; el script solo mira código de producto.
