# Contrato de pack de stack

Norma operativa para autores de `sdaf-stack-<id>@<semver>`. Anclaje constitucional: [handbook/01 §6](../handbook/01-sdaf-framework.md).

> [!NOTE]
> 📦 El pack aporta playbooks. El stack concreto lo deciden **ADRs del consumidor**.

## Identidad

- Formato: `sdaf-stack-<id>@<semver>` (p. ej. `sdaf-stack-dotnet@0.1.0`).
- El consumidor lo declara en `stack.pack` de `sdaf.config.yaml`.
- `null` = solo método; sin playbooks de lenguaje/UI del pack.

## Obligatorio

1. **README** del pack con id@version, stacks cubiertos y límites (sin fijar el runtime como norma del core).
2. **Skills** versionadas (`skills/<id>/SKILL.md`) con prefijo de stack (`csharp-*`, `blazor-*`, etc.).
3. **Contratos y prompts** solo para **ids de extensión** reconocidos por el core (`frontend`, `infrastructure`, `domain-application`, `ai`, … — ver [`sdaf.config.schema.yaml`](../sdaf.config.schema.yaml)).
4. Declaración explícita de qué aporta y qué **no** puede contradecir (capítulos Approved del handbook del core).

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

Primer pack publicado: [`sdaf-stack-dotnet@0.1.0`](https://github.com/Cyberdine-Systems-Corporation/sdaf-stack-dotnet/releases/tag/v0.1.0).

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| 📖 | [handbook/01 §6](../handbook/01-sdaf-framework.md#6-gobierno-antes-de-implementar) | Ancla constitucional |
| 🛠️ | [adopcion-y-upgrade.md](adopcion-y-upgrade.md) | Cómo declarar `stack.pack` |
| 🛠️ | [examples/README.md](../examples/README.md) | Escenarios 04, 07 y 08 |
