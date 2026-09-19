# Plantilla — Contrato de agente

| Campo | Valor |
|--------|--------|
| Versión | 0.1.0 |
| Estado | Draft / Approved |
| Fecha | YYYY-MM-DD |
| Modo | active / stub |
| Prompt base | prompts/agents/... |

## Objetivo

## Responsabilidades

## Entradas

## Salidas

## Restricciones

## Checklist

## KPIs

## Definition of Done

## Prompt base

Ruta versionada en `prompts/agents/`.

## Contexto autorizado

Índice. No sustituye al prompt base. No concatenar en un mega-prompt. Si resumen y prompt discrepan, gana el prompt.

| Capa | Artefacto | Resumen (1 línea) | Obligatorio |
|------|-----------|-------------------|-------------|
| Rol | prompts/agents/… | … | sí |
| Flujo | skills/… | … | según gate |
| IDE | .cursor/rules/idioma-castellano.mdc | Castellano en artefactos | si runtime Cursor |
| IDE | .cursor/rules/git-remoto-encargo.mdc | Git/remoto solo si este turno lo nombra (H06 §7) | si runtime Cursor |
