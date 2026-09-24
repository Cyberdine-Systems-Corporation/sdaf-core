# Composite action — validar sdaf.config del consumidor

Usar desde un repo consumidor pinneado a un tag de sdaf-core que incluya esta action.

```yaml
- uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4.3.0
  with:
    fetch-depth: 0 # necesario para el chequeo de worklog en PRs
- uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5.6.0
  with:
    python-version: "3.12"
- uses: Cyberdine-Systems-Corporation/sdaf-core/.github/actions/validate-sdaf@<tag-o-SHA-posterior-a-v0.3.3>
  with:
    config-paths: sdaf.config.yaml
```

Hasta que exista un tag posterior a esta action, referencia el SHA o la rama del core que la contenga. Un consumidor pinneado a `v0.2.1` o `v0.3.3` no la recibe.

## Inputs

| Input | Default | Uso |
|-------|---------|-----|
| `config-paths` | `sdaf.config.yaml` | Rutas YAML a validar (separadas por espacio). No asume `examples/` del core. |
| `check-worklog` | `true` | Exige un fichero bajo `worklogs/` si el diff toca código de producto. |
| `strict-i4` | `false` | Si `true`, I4 (ids de extensión sin `stack.pack`) es error. |

Los scripts se ejecutan desde el checkout de **esta** action (el árbol de sdaf-core), sobre ficheros del workspace del consumidor.

Checkout del consumidor: en PRs, `fetch-depth: 0`. Si `check-worklog` es `true` y el diff contra la base no se puede calcular, el paso **falla**; no se da por bueno.
