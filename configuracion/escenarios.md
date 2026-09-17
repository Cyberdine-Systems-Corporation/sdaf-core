# Escenarios de referencia

> [!NOTE]
> 🛠️ Página generada por MkDocs; cada bloque se incrusta en vivo desde [`examples/`](../examples/README.md). Copia el escenario que más se acerque y cambia `project.name`.

**En esta página:** [01 Default core](#01-default-core-recomendado) · [02 Mínimo](#02-mínimo) · [03 Rutas custom](#03-rutas-custom) · [04 Pack de stack](#04-pack-de-stack) · [05 Fusiones MVP](#05-fusiones-mvp) · [06 Agentes desacoplados](#06-agentes-desacoplados) · [07 Pack frontend](#07-pack-frontend) · [08 Completo](#08-completo) · [Relacionado](#relacionado)

## 01 — Default core (recomendado)

Solo método, 3 activos, stubs del core, sin pack ni fusiones extra.

```yaml
--8<-- "examples/01-default-core.yaml"
```

## 02 — Mínimo

Mínimo obligatorio (defaults de rutas).

```yaml
--8<-- "examples/02-minimo.yaml"
```

## 03 — Rutas custom

Código/tests fuera de `src/` y `tests/`.

```yaml
--8<-- "examples/03-rutas-custom.yaml"
```

## 04 — Pack de stack

Overlay técnico (`stack.pack`) sin cambiar el modelo de agentes del core.

```yaml
--8<-- "examples/04-pack-stack.yaml"
```

## 05 — Fusiones MVP

`testing-review` y `domain-application` como fusiones explícitas.

```yaml
--8<-- "examples/05-fusiones-mvp.yaml"
```

## 06 — Agentes desacoplados

Testing y Review separados; Domain y Application activos.

```yaml
--8<-- "examples/06-agentes-desacoplados.yaml"
```

## 07 — Pack frontend

Pack + agente `frontend` (extensión; el core no lo envía).

```yaml
--8<-- "examples/07-pack-frontend.yaml"
```

## 08 — Completo

Todas las claves rellenadas a la vez (referencia de techo).

```yaml
--8<-- "examples/08-completo.yaml"
```

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| 🛠️ | [Esquema sdaf.config.yaml](schema.md) | Catálogo de claves usadas aquí |
| 🛠️ | [examples/README.md](../examples/README.md) | Árbol de decisión para elegir escenario |
| 🛠️ | [docs/adopcion-y-upgrade.md](../docs/adopcion-y-upgrade.md) | Cómo copiar el escenario |
