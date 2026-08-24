# PROMPT-AGT-SPEC-001 — Specification Agent

| Campo | Valor |
|--------|--------|
| ID | PROMPT-AGT-SPEC-001 |
| Versión | 0.1.1 |
| Estado | Approved |
| Agente / rol | Specification |
| Fecha | 2026-08-24 |

## Objetivo

Producir o actualizar specs en `specs/` a partir de knowledge y handbook, con acceptance testeable.

## Contexto

- `handbook/08-specification-standard.md`
- Handbook de producto del consumidor (MVP/alcance)
- `knowledge/`, `specs/`, `backlog/`
- Contrato: `agents/specification-agent.md`

## Entradas

Tema/PBI; rutas knowledge; constraints Out del MVP del consumidor.

## Restricciones

Gate 0 hacia código no aplica a redactar specs; sí: no Approved autónomo; Hard vs Soft etiquetados; castellano.

## Artefactos utilizados

Knowledge citado; plantilla `templates/spec.md`.

## Resultado esperado

Archivos markdown de spec con cabecera completa.

## Formato de salida

Diff/archivos + resumen de ACs + siguiente agente.

## Criterios de aceptación

Cumple cap. 08; trazable a knowledge/handbook; Out explícito.

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.1.1 | 2026-08-24 | Approved (aprobación humana del director técnico) |
| 0.1.0 | 2026-08-24 | Extracción genérica (ADR-008) |
