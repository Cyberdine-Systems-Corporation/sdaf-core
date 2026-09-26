# Composite action — validar sdaf.config del consumidor

Usar desde un repo consumidor pinneado a un tag de sdaf-core que incluya esta action.

```yaml
- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
  with:
    fetch-depth: 0 # necesario para el chequeo de worklog en PRs
- uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
  with:
    python-version: "3.12"
- uses: Cyberdine-Systems-Corporation/sdaf-core/.github/actions/validate-sdaf@v0.4.1
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

Los scripts se ejecutan desde el checkout de **esta** action (el árbol de sdaf-core), sobre ficheros del workspace del consumidor.

Checkout del consumidor: en PRs, `fetch-depth: 0`. Si `check-worklog` es `true` y el diff contra la base no se puede calcular, el paso **falla**; no se da por bueno.
