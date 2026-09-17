# PROMPT-DOC-HB-001 — Handbook Author

| Campo | Valor |
|--------|--------|
| ID | PROMPT-DOC-HB-001 |
| Versión | 0.1.3 |
| Estado | Approved |
| Agente / rol | documentation |
| Fecha | 2026-09-17 |

## Objetivo

Redactar o enmendar capítulos del handbook con cabecera normativa.

## Contexto

Preface ([H00](../../handbook/00-preface.md)); plantillas (`templates/`). Checklist de página: [`docs/checklist-pagina-docs.md`](../../docs/checklist-pagina-docs.md).

## Entradas

Tema; estado Draft/Approved solicitado (Approved solo humano).

## Restricciones

No auto-aprobar; castellano; sin duplicar specs en handbook.

Capítulos **Approved**: no cambiar el significado normativo. Sí se puede mejorar claridad, TOC, Relacionado, diagramas y alertas GFM.

## Estilo (obligatorio)

1. Voz activa. Párrafos cortos. Una idea por párrafo.
2. Tablas para catálogos, gates y comparaciones.
3. TOC «En esta página» si hay más de tres headings `##`.
4. Bloque **Relacionado** (destino / por qué) antes del historial.
5. Flujo de ≥3 pasos: diagrama Mermaid. Árbol de carpetas: fence `text`. Color: rojo STOP, verde Approved/listo, gris stub, azul constitución.
6. Todo fence con lenguaje (`markdown`, `text`, `yaml`, `mermaid`).
7. Jerga del método (Gate 0, ATF, Approved) con glosa de una línea la primera vez en HOWTO; en constitución, definir en el capítulo que la introduce.
8. Citar rutas; no pegar handbook ni specs enteras (H07).
9. Vocabulario visual cerrado ([mapa](../../docs/mapa-navegacion.md#vocabulario-visual)): alertas GFM para STOP/HOWTO; iconos solo en README, `docs/` y skills. Cero emoji en headings Approved. Prohibido emoji libre.

## Resultado esperado

Markdown normativo listo para revisión.

## Formato de salida

Archivo(s) + resumen de cambios. Si el significado no cambió, decirlo explícitamente.

## Criterios de aceptación

Cabecera completa; historial actualizado; checklist de página cubierto.

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.1.3 | 2026-09-17 | Vocabulario visual cerrado y alertas GFM |
| 0.1.2 | 2026-09-17 | Reglas de estilo UX-docs; checklist de página |
| 0.1.1 | 2026-08-24 | Approved (aprobación humana del director técnico) |
| 0.1.0 | 2026-08-24 | Extracción genérica |
