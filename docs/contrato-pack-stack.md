# Contrato de pack de stack

Norma operativa para autores de `sdaf-stack-<id>@<semver>`. Anclaje constitucional: [handbook/01 §6](../handbook/01-sdaf-framework.md).

> [!NOTE]
> 📦 El pack aporta playbooks. El stack concreto lo deciden **ADRs del consumidor**.

## Identidad

- Formato: `sdaf-stack-<id>@<semver>` (p. ej. `sdaf-stack-dotnet@0.3.0`).
- El consumidor lo declara en `stack.pack` de `sdaf.config.yaml`.
- El pack declara su propia identidad en el [manifiesto](#manifiesto) `sdaf-pack.yaml`: su `id` es el nombre completo `sdaf-stack-<id>`, el mismo que se escribe en `stack.pack`.
- `null` = solo método; sin playbooks de lenguaje/UI del pack.

## Obligatorio

1. **README** del pack con id@version, stacks cubiertos y límites (sin fijar el runtime como norma del core).
2. **Skills** versionadas (`skills/<id>/SKILL.md`) con prefijo de stack (`csharp-*`, `blazor-*`, etc.).
3. **Contratos y prompts** solo para **ids de extensión** reconocidos por el core (`frontend`, `infrastructure`, `domain-application`, `ai`, … — ver [`sdaf.config.schema.yaml`](../sdaf.config.schema.yaml)).
4. Declaración explícita de qué aporta y qué **no** puede contradecir (capítulos Approved del handbook del core).
5. **Manifiesto** `sdaf-pack.yaml` en la raíz del pack, válido contra el schema del core (ver [Manifiesto](#manifiesto)). Durante `0.6.x` su ausencia es un aviso, no un error.

## Manifiesto

`sdaf-pack.yaml`, en la raíz del pack, declara la identidad del pack, con qué líneas de constitución del core es compatible y qué aporta ([ADR-007 §3](../architecture/decisions/ADR-007-modelo-de-capas-y-precedencia.md)). El core lo valida con [`sdaf-pack.schema.json`](../sdaf-pack.schema.json) y [`scripts/validate-pack.py`](../scripts/validate-pack.py).

| Campo | Obligatorio | Contenido |
|-------|:-----------:|-----------|
| `id` | Sí | Nombre completo `sdaf-stack-<id>`, en minúsculas y guiones. Es el mismo identificador que el consumidor escribe en `stack.pack`. |
| `version` | Sí | Semver estricto `X.Y.Z` del pack. |
| `core` | Sí | Rango semver de líneas de constitución compatibles, p. ej. `">=0.5.0 <0.7.0"`: uno o dos comparadores (`>=`, `>`, `<=`, `<`, `=` o ninguno) sobre `X.Y.Z`, separados por un espacio. Con dos, un límite inferior y uno superior, y el rango no puede quedar vacío. |
| `provides` | Sí | Lo que el pack aporta: al menos una de las listas `extension_ids`, `skills` y `prompts`, con ids en kebab-case y sin repeticiones. |
| `requires` | No | Lista de `{id, version}` con los packs de los que depende: `id` con el formato de `id` y `version` como rango, con la sintaxis de `core`. Un pack no puede requerirse a sí mismo. |

Ejemplo mínimo (pack ficticio `sdaf-stack-example`; la plantilla comentada y completa es [`templates/sdaf-pack.yaml`](../templates/sdaf-pack.yaml)):

```yaml
id: sdaf-stack-example
version: 0.1.0
core: ">=0.5.0 <0.7.0"
provides:
  skills:
    - example-skill
```

### Relación con `stack.pack`

El `id` y la `version` del manifiesto deben coincidir con la referencia `id@version` que escribe el consumidor en `stack.pack` (p. ej. `sdaf-stack-example@0.1.0`).

> [!WARNING]
> Esa comprobación **no existe todavía**. Hoy `validate-pack.py` valida el manifiesto de forma aislada: el schema, la coherencia de los rangos y que un pack no se requiera a sí mismo. Siguen pendientes, para ARQ-4.2: contrastar el manifiesto con `stack.pack`, comparar `core` con `sdaf.version`, detectar colisiones de ids, contrastar `extension_ids` con los ids que reconoce el core y emitir el aviso por manifiesto ausente.

Durante `0.6.x`, un pack sin manifiesto es un aviso, no un error ([ADR-007](../architecture/decisions/ADR-007-modelo-de-capas-y-precedencia.md), Consecuencias). Ese aviso lo implementa ARQ-4.2.

### Validar un manifiesto

```bash
python scripts/validate-pack.py <ruta>
```

Sin argumentos valida la plantilla. La salida es `OK  <ruta>` o una línea `FAIL <ruta>: <motivo>` por problema; el código de salida es 0 si todo valida y 1 si hay algún `FAIL`. Requiere PyYAML y jsonschema.

## Prohibido

> [!WARNING]
> El pack no puede saltar Gate 0 ni contradecir capítulos Approved de sdaf-core.

- Redefinir o sustituir agentes del **núcleo** (specification, architecture, testing-review, stubs del core).
- Saltar Gate 0 o autorizar implementación sin specs Approved.
- Incluir `specs/`, `knowledge/` o handbook de un producto concreto.
- Contradecir el handbook Approved de sdaf-core.

## Relación con ADRs del consumidor

El pack aporta playbooks. El **stack concreto** (lenguaje, UI, BD, topología) sigue decidiéndose por **ADRs del consumidor**.

## Cumplimiento

Gate 0 y el router leen `stack.pack`. Si el pack no cumple este contrato, el consumidor debe corregir el pack o quitar la referencia.

## Pack de referencia

Pack de referencia: [`sdaf-stack-dotnet@0.3.0`](https://github.com/Cyberdine-Systems-Corporation/sdaf-stack-dotnet/releases/tag/v0.3.0) (primera publicación: [`v0.1.0`](https://github.com/Cyberdine-Systems-Corporation/sdaf-stack-dotnet/releases/tag/v0.1.0)).

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| 📖 | [handbook/01 §6](../handbook/01-sdaf-framework.md#6-gobierno-antes-de-implementar) | Ancla constitucional |
| 🛠️ | [adopcion-y-upgrade.md](adopcion-y-upgrade.md) | Cómo declarar `stack.pack` |
| 🛠️ | [examples/README.md](../examples/README.md) | Escenarios 04, 07 y 08 |
