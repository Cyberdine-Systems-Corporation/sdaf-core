# Apéndice B — Glossary

| Campo | Valor |
|--------|--------|
| **Versión** | 0.3.2 |
| **Estado** | Approved |
| **Fecha** | 2026-09-19 |
| **Parte** | Apéndices |
| **Norma superior** | Este handbook; el glossary de dominio canónico vive en `specs/domain/` del consumidor |

---

**En esta página:** [Propósito](#1-propósito) · [Términos](#2-términos)

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
| **Pack de stack** | Overlay técnico opcional (`sdaf-stack-*`); no contradice este handbook |

---

## Relacionado

| Destino | Por qué |
|---------|---------|
| [README.md](README.md) | Índice y estados |
| [01-sdaf-framework.md](01-sdaf-framework.md) | Definición del marco |
| [12-security-standards.md](12-security-standards.md) | QG-Sec y OWASP |

## 3. Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.3.2 | 2026-09-19 | QG-Sec §5.2, QG-Review HITL, overlay, origen de cambios |
| 0.3.0 | 2026-09-19 | Approved (aprobación humana del director técnico) |
| 0.3.0 | 2026-09-18 | Draft: términos de método (extract A; sin dominio de producto) |
