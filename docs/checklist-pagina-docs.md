# Checklist de página (docs / handbook / skills)

Usar en el DoD de un PR que toque markdown. Marcar lo aplicable.

1. **Título** dice qué es la página en una línea.
2. **Rol** explícito: constitución, HOWTO, contrato, playbook o plantilla.
3. **Puerta de entrada:** un lector nuevo llega en ≤3 clics desde el README.
4. **En esta página** (TOC) si hay más de tres headings `##`.
5. **Relacionado** al cierre (tabla destino / por qué), sin bucles vacíos.
6. **Enlaces** relativos a archivos que existen (CI: `scripts/check-local-links.py`).
7. **Anclas** coinciden con el slug GFM del heading (minúsculas, sin puntuación; tildes se conservan). MkDocs usa el mismo criterio (`slugify_unicode` en `mkdocs/mkdocs.yml`).
8. **Un diagrama** (Mermaid) si hay un flujo de ≥3 pasos; árboles de carpetas pueden seguir en ` ```text `. Color: rojo STOP, verde Approved/listo, gris stub, azul constitución.
9. **Tablas** para catálogos, gates y comparaciones; no párrafos-lista de 10 ítems.
10. **Fences** con lenguaje (`text`, `yaml`, `markdown`, `mermaid`).
11. **Voz activa**, párrafos cortos, castellano directo.
12. **Jerga del método** (Gate 0, ATF, Approved, pack) con glosa de una línea la primera vez en páginas HOWTO.
13. **Sin pegar** handbook ni specs enteras (economía de tokens, H07).
14. **Versión** de release coherente con [handbook/CHANGELOG.md](../handbook/CHANGELOG.md) cuando se cite un tag.
15. **Significado normativo** de capítulos Approved intacto: solo claridad, TOC, Relacionado, diagrama o alerta GFM.
16. **Vocabulario visual cerrado** ([mapa](mapa-navegacion.md#vocabulario-visual)): icono o alerta GFM cuando hay STOP, Draft/Approved o cambio de rol (constitución vs HOWTO). Prohibido emoji libre. Cero emoji en headings Approved.

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| 🧭 | [mapa-navegacion.md](mapa-navegacion.md) | Ocho tareas, clics y vocabulario visual |
| 🛠️ | [adopcion-y-upgrade.md](adopcion-y-upgrade.md) | HOWTO de pin y upgrade |
| 📖 | [H00](../handbook/00-preface.md) | Qué es y qué no es el handbook |
