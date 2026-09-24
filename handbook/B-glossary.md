# Apéndice B — Glossary

> Andamiaje (cabecera, TOC, Relacionado, Historial): `_meta/B-glossary.yaml`.

> [!NOTE]
> Glosario de **método**, no de dominio de producto.

## 1. Propósito

Glosario de **ingeniería y SDAF**. No sustituye el ubiquitous language de negocio en `specs/domain/` del consumidor.

---

## 2. Términos

| Término | Definición |
|---------|------------|
| **SDAF** | Spec-Driven AI Development Framework: marco de ingeniería de este core |
| **Handbook** | Constitución (método en este core; producto en el consumidor) |
| **Knowledge** | Fuente primaria inmutable de expertos (`knowledge/` del consumidor) |
| **Spec** | Especificación testeable en `specs/` del consumidor |
| **ADR** | Architecture Decision Record |
| **PBI** | Product Backlog Item |
| **Gate 0** | Condiciones pre-implementación (spec, acceptance, ADR si aplica, worklog) |
| **Gate 1–3** | Durante implementación, listo para merge, cierre de release (H05) |
| **ATF** | Agent Traceability Framework (`worklogs/` del consumidor) |
| **Worklog** | Registro de una iteración de agente/humano |
| **Agente activo** | Agente de ingeniería en uso regular |
| **Stub (agente)** | Contrato+prompt listos; activación bajo demanda |
| **QG-Build / Unit / Accept / Arch / Docs / Sec / Review** | Quality gates técnicos de H10 |
| **QG-Sec** | Gate de H12 §5.2: secreto en claro, bypass de auth, injection, SSRF o CVE crítica identificada en el review |
| **QG-Review** | Checklist H10 §3 más aprobación humana nominada del merge; el dictamen de un agente no basta |
| **Overlay (H12)** | Control N/A salvo ADR del consumidor (mismo patrón que QG-Docs) |
| **Origen de cambios** | Campo ATF: `humano` / `ia` / `mixto` / `dependencia` (H08 §4.3) |
| **OWASP Top 10** | Mapa de riesgos web usado como marco en el baseline de H12 |
| **IA de producto** | Asistencia al usuario final en el producto consumidor |
| **Agente de ingeniería** | Agente que produce artefactos del repo |
| **Runtime local autocontenido** | App + dependencias levantables en local sin exigir cloud (H11) |
| **Vertical slice** | Unidad de feature coherente de extremo a extremo (H05); no implica un patrón de stack |
| **Encargo vigente** | El mensaje de usuario **de este turno**; no el historial de la conversación (H06 §7) |
| **Pack de stack** | Overlay técnico opcional (`sdaf-stack-*`); no contradice este handbook |

---
