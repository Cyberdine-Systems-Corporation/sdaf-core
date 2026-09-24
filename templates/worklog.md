---
pbi: PBI-XXX
iteracion: Iteration-NNN
fecha: YYYY-MM-DD
inicio: YYYY-MM-DDThh:mm:ss+hh:mm
fin: YYYY-MM-DDThh:mm:ss+hh:mm
agente: specification | architecture | testing-review | humano | …
modelo: id del modelo
version_prompt: MAJOR.MINOR
prompt_base: prompt_id@version
prompts_adicionales: ninguno
skills: skill-id@version
reglas_ide: idioma-castellano, git-remoto-encargo
ad_hoc: ninguno
contexto: breve
especificaciones_utilizadas: rutas
archivos_leidos: rutas
archivos_modificados: rutas
origen_cambios: N/A
resultado: breve
tiempo: PT0H0M
coste:
  modalidad: api | suscripcion | local | mixta
  importe: null
  moneda: EUR
  tokens: null
  fuente: de dónde sale el dato (consola, factura, get_usage…)
observaciones: ""
pruebas_ejecutadas: ninguna | lista
estado: en_curso
siguiente_agente: architecture | humano | …
commit: null
pr: null
rama: null
sha: null
resumen_acumulado: "prompt_id@version — una línea; commit/PR/rama/SHA ausentes"
---

# PBI-XXX / Iteration-NNN

## Línea de decisión

- N/A (o spec/ADR/capítulo § que justificó cada elección)

## Origen de cambios

| Archivo | Origen | Notas |
|---------|--------|-------|
| N/A (esta iteración no toca código de producto) | | |

`inicio` y `fin` llevan hora y zona horaria (ISO 8601); `fecha` es el día de `inicio`. `tiempo` es una duración ISO 8601 que no supera `fin − inicio`. `coste` dice modalidad, importe, moneda, tokens y de dónde sale el dato. Si algo no se conoce, `N/D: <motivo>`; `N/D` a secas no vale.

`commit`, `pr`, `rama` y `sha` en el frontmatter son la cadena de trazabilidad (H08 §6). `null` declara ausencia explícita. `resumen_acumulado` es un índice de una línea (H07 §7): apunta a `id@version` y a esos refs; no sustituye al prompt ni al historial del handbook.

Los worklogs anteriores en tabla markdown siguen válidos; no se reescriben.
