# Contrato de pack de stack

Norma operativa para autores de `sdaf-stack-<id>@<semver>`. Anclaje constitucional: [handbook/01 §6](../handbook/01-sdaf-framework.md).

> [!NOTE]
> 📦 El pack aporta playbooks. El stack concreto lo deciden **ADRs del consumidor**.

## Identidad

- Formato: `sdaf-stack-<id>@<semver>` (p. ej. `sdaf-stack-dotnet@0.3.0`).
- El consumidor lo declara en `stack.packs` de `sdaf.config.yaml`, una referencia `id@version` por pack (p. ej. `["sdaf-stack-example@0.1.0"]`). `stack.pack`, con una sola referencia, es un alias obsoleto (ver [Relación con `stack.packs`](#relación-con-stackpacks)).
- El pack declara su propia identidad en el [manifiesto](#manifiesto) `sdaf-pack.yaml`: su `id` es el nombre completo `sdaf-stack-<id>`, el mismo que se escribe en `stack.packs`.
- `stack.packs: []` (o el alias `stack.pack: null`) = solo método; sin playbooks de lenguaje/UI del pack.

## Obligatorio

1. **README** del pack con id@version, stacks cubiertos y límites (sin fijar el runtime como norma del core).
2. **Skills** versionadas (`skills/<id>/SKILL.md`) con prefijo de stack (`csharp-*`, `blazor-*`, etc.).
3. **Contratos y prompts** solo para **ids de extensión** reconocidos por el core (`frontend`, `infrastructure`, `domain-application`, `ai`, … — ver [`sdaf.config.schema.yaml`](../sdaf.config.schema.yaml)).
4. Declaración explícita de qué aporta y qué **no** puede contradecir (capítulos Approved del handbook del core).
5. **Manifiesto** `sdaf-pack.yaml` en la raíz del pack, válido contra el schema del core (ver [Manifiesto](#manifiesto)). Durante `0.6.x` su ausencia es un aviso, no un error (ver [Aviso por manifiesto ausente](#cruzar-la-config-con-los-manifiestos)).

## Manifiesto

`sdaf-pack.yaml`, en la raíz del pack, declara la identidad del pack, con qué líneas de constitución del core es compatible y qué aporta ([ADR-007 §3](../architecture/decisions/ADR-007-modelo-de-capas-y-precedencia.md)). El core lo valida con [`sdaf-pack.schema.json`](../sdaf-pack.schema.json) y [`scripts/validate-pack.py`](../scripts/validate-pack.py).

| Campo | Obligatorio | Contenido |
|-------|:-----------:|-----------|
| `id` | Sí | Nombre completo `sdaf-stack-<id>`, en minúsculas y guiones. Es el mismo identificador que el consumidor escribe en `stack.packs`. |
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

### Relación con `stack.packs`

El consumidor declara los packs en `stack.packs`, una lista de referencias `id@version` (p. ej. `sdaf-stack-example@0.1.0`) sin repetidos. Reglas que comprueba [`scripts/validate-config.py`](../scripts/validate-config.py):

- **Alias obsoleto.** `stack.pack` equivale a `stack.packs` con un único elemento. Con un valor no nulo, la config valida pero avisa (`WARN`): `stack.pack está obsoleto; usar stack.packs: ["<id@version>"]`. Con `stack.pack: null` no hay aviso. Una config de `0.5.x` con `stack.pack` sigue validando.
- **Sin coexistencia.** `stack.pack` (no nulo) y `stack.packs` en la misma config son un error, también con `packs: []`; se usa solo `stack.packs`. `stack.pack: null` junto a `stack.packs` no entra en conflicto.
- **Un id por pack.** Dos referencias con el mismo `id` son un error aunque difiera la versión.
- **Sin espacios ni saltos en los extremos.** `sdaf.version`, `stack.pack`, cada elemento de `stack.packs` y `tooling.gentle_ai` se rechazan si llevan espacios o saltos de línea al inicio o al final (p. ej. un bloque literal `|` de YAML, que deja un salto final). Lo comprueba el validador; el schema JSON, por sí solo, sigue admitiendo el salto final porque sus patrones terminan en `$`.
- **Un YAML roto no rompe el validador.** Un YAML inválido, un fichero que no es UTF-8 o una raíz que no es un mapa dan `FAIL` con un motivo, nunca un traceback.

Estas reglas operan sobre la config sola. Para cruzarla con los manifiestos hay que pasarlos con `--pack-manifest` ([ver más abajo](#cruzar-la-config-con-los-manifiestos)).

### Validar un manifiesto

```bash
python scripts/validate-pack.py <ruta>
```

Sin argumentos valida la plantilla. La salida es `OK  <ruta>` o una línea `FAIL <ruta>: <motivo>` por problema; el código de salida es 0 si todo valida y 1 si hay algún `FAIL`. Requiere PyYAML y jsonschema.

Valida el manifiesto de forma aislada: el schema, la coherencia de los rangos, que un pack no se requiera a sí mismo y que ningún `id`, `version`, `core`, valor de `requires` ni elemento de `provides` lleve espacios o saltos de línea en los extremos. No lo cruza con ninguna config; de eso se ocupa `validate-config.py`.

### Cruzar la config con los manifiestos

```bash
python scripts/validate-config.py sdaf.config.yaml \
  --pack-manifest <ruta/a/sdaf-pack.yaml> --pack-manifest <otra/ruta/sdaf-pack.yaml>
```

`--pack-manifest RUTA` es repetible, una vez por manifiesto. **Sin el flag no se lee ningún manifiesto** y el resto de reglas no cambia. El core no impone dónde vive el manifiesto de cada pack: se pasa la ruta. Cada manifiesto se valida con las mismas reglas que `validate-pack.py` y, si es válido, se cruza con la config:

| Regla | Resultado | Condición |
|-------|-----------|-----------|
| Manifiesto inválido o repetido | `FAIL` | El manifiesto no valida (mismos motivos que `validate-pack.py`), no se puede leer, o se pasa dos veces. Un manifiesto así queda fuera de los demás cruces; su `FAIL` ya hace que el resultado sea 1. |
| Coincidencia con la referencia | `FAIL` | El `id@version` del manifiesto debe figurar literalmente en `stack.packs` (o en el alias `stack.pack`). Un manifiesto cuya versión difiere de la referencia, o que ninguna referencia nombra, da `manifiesto no referenciado`. |
| Rango `core` | `FAIL` | El rango `core` del manifiesto debe incluir `sdaf.version`. |
| Colisión de ids | `FAIL` | Un mismo id en `provides.extension_ids`, `provides.skills` o `provides.prompts` de dos manifiestos referenciados ([ADR-007 §5](../architecture/decisions/ADR-007-modelo-de-capas-y-precedencia.md)). |
| I4 con manifiestos | `WARN` (o `FAIL` con `--strict-i4`) | Ver más abajo. |
| Manifiesto ausente | `WARN` | Solo si `sdaf.version` es `0.6.0` o posterior; ver más abajo. |

**Rango `core` y límites `X.Y.0`.** `sdaf.version` nombra una **línea** de constitución (p. ej. `0.6.0`), no un tag (`v0.6.3`). El validador compara la tupla de enteros `X.Y.Z` tal cual: la línea `0.6.0` cumple `<0.7.0` y `>=0.5.0`; una línea con patch distinto de 0, como `0.6.3`, cumple `<0.7.0` pero no `<=0.6.0`. Por eso los rangos de `core` deben usar límites `X.Y.0` (`">=0.5.0 <0.7.0"`), no límites con patch. Un rango fuera de la línea da `FAIL core: el rango '<rango>' de <id@version> (<ruta>) no incluye sdaf.version <línea>`.

**I4 con manifiestos.** Los ids de extensión que usan los agentes (I4, ver [`sdaf.config.schema.yaml`](../sdaf.config.schema.yaml)) se contrastan con `provides.extension_ids` solo si **todos** los packs declarados tienen manifiesto entre los pasados: entonces cada id de extensión usado debe figurar en `provides.extension_ids` de algún pack. Si falta el manifiesto de algún pack declarado no se puede concluir qué ids aporta, y cualquier pack declarado anula I4, igual que sin manifiestos.

**Aviso por manifiesto ausente.** Durante `0.6.x`, un pack sin manifiesto es un aviso, no un error ([ADR-007](../architecture/decisions/ADR-007-modelo-de-capas-y-precedencia.md), Consecuencias). Lo emite `validate-config.py` solo con `sdaf.version` `>= 0.6.0` y por cada pack declarado sin manifiesto entre los pasados: `pack <id@version> sin manifiesto entre los pasados (aviso durante 0.6.x)`. En una config `0.5.x` no se emite nunca; recibe solo el aviso del alias.

### Ruta normada de los packs

Un pack aporta sus agentes, prompts y skills en rutas fijas, las mismas que usa el core. La convención no se declara en el manifiesto: `provides` lista ids, no rutas, y [`sdaf-pack.schema.json`](../sdaf-pack.schema.json) no la lleva.

| Aporte | Ruta en la raíz del pack |
|--------|--------------------------|
| Contrato de agente | `agents/<id>-agent.md` |
| Prompt de agente | `prompts/agents/<id>-agent.md` |
| Skill | `skills/<id>/SKILL.md` |

El `<id>` del contrato y del prompt es el id de extensión del agente. [`scripts/materialize.py`](../scripts/materialize.py) materializa esos aportes en la misma ruta del consumidor y no toca nada que el pack ponga fuera de ellas; el uso y el contrato están en [materializacion.md](materializacion.md#convención-de-rutas).

### Resolución por id

La **regla** (qué ids se sustituyen y cuáles no, qué es una colisión y qué excepción hay) vive en un solo sitio: [handbook/01 §3.3](../handbook/01-sdaf-framework.md#33-capas-y-resolución-por-id), que aplica [ADR-007 §5](../architecture/decisions/ADR-007-modelo-de-capas-y-precedencia.md). Esta sección no la repite: describe el **mecanismo**.

**Declarar la sustitución.** `stack.overlay.replaces` en `sdaf.config.yaml` es una lista, opcional y sin valor por defecto, de ids de extensión que el overlay del consumidor sustituye de forma explícita. `overlay` es un objeto sin otras claves; `overlay: {}` equivale a no declararlo, y una config de `0.5.x` sin la clave sigue validando. El campo está en el [catálogo de la config](../sdaf.config.schema.yaml) y en [`sdaf.config.schema.json`](../sdaf.config.schema.json). Ejemplo (ids ficticios):

```yaml
stack:
  packs:
    - sdaf-stack-example@0.1.0
  overlay:
    replaces:
      - example-extension
agents:
  active:
    - specification
    - example-extension
```

**Qué comprueba hoy [`scripts/validate-config.py`](../scripts/validate-config.py)**, sin ningún flag, sobre cada id de `replaces`:

| Regla | Resultado | Condición |
|-------|-----------|-----------|
| Id del núcleo | `FAIL` | El id figura entre los ids del núcleo del catálogo. Mensaje: `stack/overlay/replaces/0: los ids de agente del núcleo no se sustituyen (ADR-007 §5): architecture`. |
| Id no declarado | `FAIL` | El id no es clave ni miembro de `agents.active`, `agents.stubs` o `agents.fusions`. Mensaje: `stack/overlay/replaces/0: id no declarado en agents: example-extension`. |
| Espacios o saltos en los extremos | `FAIL` | Igual que el resto de valores de la config (p. ej. un bloque literal de YAML, que deja un salto final). |
| Ids repetidos | `FAIL` | Lo comprueba el schema (`uniqueItems`). |
| Forma | `FAIL` | `replaces` no es una lista, o `overlay` lleva otra clave: lo comprueba el schema. |

A efectos del validador, un id de extensión es cualquier id que no sea del núcleo. `replaces` sin packs declarados no da aviso.

**Límite.** No se comprueba que algún pack aporte de verdad el id de `replaces`, ni se cruza con los `provides` de los manifiestos.

**Colisión entre un pack y el overlay.** No la detecta `validate-config.py`, que solo ve la config. La detecta [`scripts/materialize.py`](../scripts/materialize.py) antes de escribir, al materializar, y es el único sitio donde existe esa comprobación: ver [Colisiones](materializacion.md#colisiones) para el mecanismo y los mensajes. La norma sigue siendo la de [handbook/01 §3.3](../handbook/01-sdaf-framework.md#33-capas-y-resolución-por-id).

### Qué no existe todavía

> [!WARNING]
> Siguen sin existir: el contraste de los `extension_ids` de un manifiesto con el catálogo de ids del core; un input de la action `validate-sdaf` para pasar manifiestos; y el manifiesto del pack de referencia (ARQ-4.7). El overlay y la sustitución explícita tienen declaración (`stack.overlay.replaces`) y la validación mínima de arriba; la materialización y la detección de la colisión entre un pack y el overlay existen en [`scripts/materialize.py`](../scripts/materialize.py), sin publicar hasta la línea `0.6.0` ([materializacion.md](materializacion.md)).

## Prohibido

> [!WARNING]
> El pack no puede saltar Gate 0 ni contradecir capítulos Approved de sdaf-core.

- Redefinir o sustituir agentes del **núcleo** (specification, architecture, testing-review, stubs del core; [handbook/01 §3.3](../handbook/01-sdaf-framework.md#33-capas-y-resolución-por-id)).
- Saltar Gate 0 o autorizar implementación sin specs Approved.
- Incluir `specs/`, `knowledge/` o handbook de un producto concreto.
- Contradecir el handbook Approved de sdaf-core.

## Relación con ADRs del consumidor

El pack aporta playbooks. El **stack concreto** (lenguaje, UI, BD, topología) sigue decidiéndose por **ADRs del consumidor**.

## Cumplimiento

Gate 0 y el router leen los packs declarados (`stack.packs`, o el alias obsoleto `stack.pack`). Si el pack no cumple este contrato, el consumidor debe corregir el pack o quitar la referencia.

## Pack de referencia

Pack de referencia: [`sdaf-stack-dotnet@0.3.0`](https://github.com/Cyberdine-Systems-Corporation/sdaf-stack-dotnet/releases/tag/v0.3.0) (primera publicación: [`v0.1.0`](https://github.com/Cyberdine-Systems-Corporation/sdaf-stack-dotnet/releases/tag/v0.1.0)).

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| 📖 | [handbook/01 §6](../handbook/01-sdaf-framework.md#6-gobierno-antes-de-implementar) | Ancla constitucional |
| 📖 | [handbook/01 §3.3](../handbook/01-sdaf-framework.md#33-capas-y-resolución-por-id) | Capas y regla de resolución por id |
| 🛠️ | [adopcion-y-upgrade.md](adopcion-y-upgrade.md) | Cómo declarar el pack en la config |
| 🛠️ | [materializacion.md](materializacion.md) | Cómo se materializan el core y los packs en el consumidor |
| 🛠️ | [examples/README.md](../examples/README.md) | Escenarios 04, 07 y 08 |
