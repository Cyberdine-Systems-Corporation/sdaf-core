# Contribuir a sdaf-core

## Norma

La constitución está en [`handbook/`](handbook/README.md). Cómo se enmienda está en [`handbook/13-enmienda-excepciones-ciclo-de-vida.md`](handbook/13-enmienda-excepciones-ciclo-de-vida.md) (Approved) y [ADR-002](architecture/decisions/ADR-002-gobernanza-del-metodo.md) (Aceptado), que desarrollan [H00 §3](handbook/00-preface.md).

## Qué no hace un agente

No marca un capítulo como Approved ni un ADR como Aceptado ([H00 §3.3](handbook/00-preface.md)). No abre commit, push, PR, tag, release ni merge salvo que el encargo vigente lo nombre ([H06 §7](handbook/06-ai-agent-framework.md)).

## Cómo proponer una enmienda

1. PR con la clase marcada en [`.github/pull_request_template.md`](.github/pull_request_template.md): **significado** o **redacción** (H13 §6).
2. Si el cambio es de significado de un capítulo Approved: bump declarado, fila en [`handbook/CHANGELOG.md`](handbook/CHANGELOG.md), worklog si el cambio es material ([H08 §5](handbook/08-agent-traceability.md)).
3. Revisión humana nominada del merge ([H10](handbook/10-code-review-and-quality-gates.md)): la identidad está en [`CODEOWNERS`](CODEOWNERS).

## Commits

Castellano. Prefijo corto opcional (`docs:`, `fix:`, `feat:`) más el porqué. Distinguir norma (significado) de redacción.

## Seguridad

Avisos de **este** repo: [`SECURITY.md`](SECURITY.md). La plantilla de reporte del consumidor es [`templates/security.md`](templates/security.md).
