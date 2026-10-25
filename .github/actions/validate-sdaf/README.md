# Composite action — validar sdaf.config del consumidor

Usar desde un repo consumidor pinneado a un tag de sdaf-core que incluya esta action.

```yaml
- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
  with:
    fetch-depth: 0 # necesario para el chequeo de worklog en PRs
- uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
  with:
    python-version: "3.12"
- uses: Cyberdine-Systems-Corporation/sdaf-core/.github/actions/validate-sdaf@v0.5.2
  with:
    config-paths: sdaf.config.yaml
```

Disponible desde `v0.4.0`. Un consumidor pinneado a `v0.2.1` o `v0.3.3` no la recibe hasta que mueva el pin.

## Inputs

| Input | Default | Uso |
|-------|---------|-----|
| `config-paths` | `sdaf.config.yaml` | Rutas YAML a validar (separadas por espacio). No asume `examples/` del core. |
| `check-worklog` | `true` | Exige un fichero bajo `worklogs/` si el diff toca código de producto. |
| `strict-i4` | `false` | Si `true`, I4 (ids de extensión sin `stack.pack`) es error. |
| `check-adrs` | `false` | Si `true`, comprueba los ADRs del consumidor con `check-adrs.py --consumer`. |
| `adrs-legacy-up-to` | `0` | Número del último ADR heredado (anterior a la adopción); `0` = ninguno. Solo se usa con `check-adrs`. |
| `check-gate0` | `false` | Si `true`, ejecuta las comprobaciones mecánicas de Gate 0 con `check-gate0.py`. Bloqueante: un `FAIL` falla el paso. |
| `gate0-pbi` | vacío | IDs o rutas de PBI a comprobar, separados por espacio; anula la selección por diff. Vacío = el PBI en curso se deduce del diff del PR. Solo se usa con `check-gate0`. |

Los scripts se ejecutan desde el checkout de **esta** action (el árbol de sdaf-core), sobre ficheros del workspace del consumidor.

## ADRs del consumidor

Con `check-adrs: "true"` la action ejecuta `scripts/check-adrs.py --consumer` sobre los ADRs del workspace. Es opt-in: con los inputs por defecto no se comprueban.

```yaml
- uses: Cyberdine-Systems-Corporation/sdaf-core/.github/actions/validate-sdaf@v0.5.3
  with:
    check-adrs: "true"
    adrs-legacy-up-to: "12"
```

`adrs-legacy-up-to` es `N`: los ADRs con número ≤ `N` son heredados y solo ellos reciben las relajaciones de contenido; los ADRs nuevos (número > `N`) mantienen las reglas del core. Un valor vacío cuenta como `0`; uno no numérico lo rechaza el script. Qué se relaja y cómo elegir `N`: [Validar los ADRs del consumidor](../../../docs/adopcion-y-upgrade.md#validar-los-adrs-del-consumidor).

Disponible desde `v0.5.3` (se crea tras el merge del parche).

## Gate 0 (comprobaciones mecánicas)

Con `check-gate0: "true"` la action ejecuta `scripts/check-gate0.py` sobre el workspace: comprobaciones **mecánicas** de G0.1, G0.2, G0.4, G0.5 y G0.6 del PBI en curso. Es opt-in y **bloqueante**: con algún `FAIL` el paso falla. G0.3 es juicio humano: sale siempre como `AVISO` y solo se verifica que los ADRs citados existan y estén Aceptados.

```yaml
- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
  with:
    fetch-depth: 0 # necesario para deducir el PBI del diff
- uses: Cyberdine-Systems-Corporation/sdaf-core/.github/actions/validate-sdaf@v0.5.3
  with:
    check-gate0: "true"
    gate0-pbi: "PBI-PRD-001" # opcional: sin él, el PBI se deduce del diff
```

- Sin `gate0-pbi`, el PBI en curso sale del diff del PR: solo si toca código de producto (`stack.src_path`, `stack.tests_path`), con los PBIs de `backlog/` tocados y los que citan un worklog tocado. Si el diff toca producto y no identifica ningún PBI, es un `FAIL` (STOP).
- `gate0-pbi` admite IDs o rutas separados por espacio (una ruta no puede contener espacios). Un valor que empiece por `-` se rechaza; el valor nunca se interpreta como código.
- Con `sdaf.version` anterior a `0.5.0` el comprobador avisa y no comprueba nada.
- Sin diff de PR y sin `gate0-pbi`, el comprobador avisa y no comprueba; con un diff de PR que no se puede calcular, el paso **falla**.

Qué comprueba, sus límites (la excepción de adopción no se detecta y un PR correctivo en perímetro heredado fallará el paso) y cómo desactivarlo en ese caso: [Comprobar Gate 0 en el PR](../../../docs/adopcion-y-upgrade.md#comprobar-gate-0-en-el-pr). El comprobador no aprueba nada ni sustituye la revisión de la persona responsable.

Disponible desde `v0.5.3` (se crea tras el merge del parche).

Checkout del consumidor: en PRs, `fetch-depth: 0`. Si `check-worklog` es `true` y el diff contra la base no se puede calcular, el paso **falla**; no se da por bueno. Con `check-gate0` y sin `gate0-pbi` rige lo mismo.
