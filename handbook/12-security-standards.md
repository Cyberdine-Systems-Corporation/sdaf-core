# 12 — Security Standards

| Campo | Valor |
|--------|--------|
| **Versión** | 0.3.0 |
| **Estado** | Approved |
| **Fecha** | 2026-09-19 |
| **Parte** | III — Calidad y entrega |
| **Norma superior** | [02-engineering-principles.md](02-engineering-principles.md), [05-development-workflow.md](05-development-workflow.md) |
| **Deriva hacia** | [10-code-review-and-quality-gates.md](10-code-review-and-quality-gates.md), `templates/security.md`, Testing+Review, skill `security-review` |

---

**En esta página:** [Propósito](#1-propósito) · [Alcance](#2-alcance-y-no-alcance) · [Referencias](#3-referencias-externas) · [Baseline](#4-baseline-obligatorio) · [Gates](#5-gates-y-review) · [Roles](#6-roles)

## 1. Propósito

Fijar el **baseline de seguridad** obligatorio para humanos y agentes: qué hay que cumplir ya, qué queda diferido, y cómo se revisa.

Este capítulo **no** convierte al producto consumidor en sistema hardened de producción. Complementa el ADR de auth del consumidor, los QG de [H10](10-code-review-and-quality-gates.md) y la plantilla de reporte [`templates/security.md`](../templates/security.md).

---

## 2. Alcance y no-alcance

### 2.1 En alcance (método)

- Secretos y credenciales en repo, runbooks, colecciones de API y worklogs.
- Controles básicos alineados a riesgos OWASP Top 10 **relevantes al stack del consumidor**.
- Checklist de review y gate técnico mínimo (QG-Sec).
- Autorización coherente API / UI según el ADR de auth del consumidor.

### 2.2 Fuera de alcance (salvo enmienda o ADR del consumidor)

- Certificación ASVS completa, pentest formal obligatorio, bug bounty.
- SSO / OIDC / MFA, IAM multi-tenant, WAF, SIEM — salvo que el MVP del consumidor los declare In.
- Cloud hardening como DoD del método (H11: local-first).

Lo diferido en ADR/specs del consumidor **no** es “bug” por sí solo; sí lo es un bypass de lo **sí** especificado (p. ej. endpoint de producto sin auth cuando el ACC lo exige).

---

## 3. Referencias externas (marco, no checklist interminable)

| Referencia | Uso en el método |
|------------|------------------|
| [OWASP Top 10](https://owasp.org/www-project-top-ten/) | Mapa de riesgos; baseline §4 |
| OWASP ASVS (nivel 1, selectivo) | Inspiración; **no** se exige cobertura ASVS completa |
| ADR de auth del consumidor | Decisión concreta de sesión / roles |
| `SECURITY.md` del consumidor | Cómo reportar vulnerabilidades (plantilla en `templates/security.md`) |

Los agentes **enlazan** estas referencias; no pegan el Top 10 entero en cada PR.

---

## 4. Baseline obligatorio

### 4.1 Secretos y datos sensibles

- Prohibido commitear passwords, connection strings con credenciales, API keys, `.env` con secretos, almacenes locales de secretos.
- Credenciales de demo: user-secrets / env / runbook; no como verdad en git salvo placeholder documentado de desarrollo.
- Colecciones de API: sin tokens reales.
- Logs y worklogs: sin secretos ni PII innecesaria.

### 4.2 Autenticación y autorización

- Cumplir el ADR de auth del consumidor y los ACC de auth.
- Endpoints de producto protegidos según ese ADR, salvo rutas explícitamente públicas.
- No “abrir” autorización en UI sin la misma regla en API.

### 4.3 Mapa OWASP Top 10 → controles del método

| Riesgo (categoría) | Control mínimo |
|--------------------|----------------|
| Broken Access Control | Políticas/roles en API; tests ACC de auth; no confiar solo en ocultar UI |
| Cryptographic Failures | No almacenar secretos en claro en repo; transporte según ADR del consumidor |
| Injection | Acceso a datos parametrizado; sin concatenar input en SQL/comandos; validar entradas de API |
| Insecure Design | Specs + ADR antes de features sensibles; no inventar auth ad hoc |
| Security Misconfiguration | No exponer trazas sensibles en demos; secretos fuera de git |
| Vulnerable Components | Tras actualizar dependencias, QG-Build / tests verdes; anotar CVEs críticas si aparecen |
| Identification / Auth Failures | Cumplir ADR de auth; no registrar contraseñas |
| Software / Data Integrity | No ejecutar scripts no versionados con secretos; PRs revisados (H10) |
| Security Logging Failures | Errores de auth sin filtrar secretos; no loguear passwords |
| SSRF | No introducir fetch a URLs controladas por usuario sin spec/ADR |

### 4.4 Sesión

Flags de cookie / token (HttpOnly, Secure, SameSite, etc.) los fija el ADR de auth del consumidor. Documentar el flujo en el runbook si cambia.

---

## 5. Gates y review

### 5.1 Checklist (añadir a H10)

Al tocar auth, sesión, endpoints, secretos o input externo:

- [ ] Sin secretos nuevos en el diff.
- [ ] Autorización coherente API (y UI si aplica).
- [ ] Sin injection obvia (SQL / comandos).
- [ ] Alineado al ADR de auth / specs ACC si el PBI las toca.
- [ ] Runbook / `SECURITY.md` del consumidor no contradichos.

### 5.2 QG-Sec

| Gate | Condición | Bloquea |
|------|-----------|---------|
| QG-Sec | Diff no introduce secreto en claro ni bypass de auth de lo especificado | Merge |

Hallazgos QG-Sec son **bloqueantes** (H10 §5).

### 5.3 Reporte

Vulnerabilidades descubiertas: `SECURITY.md` del consumidor (plantilla [`templates/security.md`](../templates/security.md)). Sin PoC en issue público.

Skill operativa: [`skills/security-review`](../skills/security-review/SKILL.md).

---

## 6. Roles

| Actor | Responsabilidad |
|-------|-----------------|
| Architecture | ADR de auth / sesión / controles nuevos |
| Implementación del consumidor | Cumplir baseline en el slice |
| Testing+Review | Checklist §5 + ACC auth; dictamen merge |
| Humano | Aprobar enmiendas de este capítulo; severidad en demos externas |

---

## Relacionado

| Destino | Por qué |
|---------|---------|
| [10-code-review-and-quality-gates.md](10-code-review-and-quality-gates.md) | QG-Sec y checklist de review |
| [11-devops.md](11-devops.md) | Secretos y runbook |
| [templates/security.md](../templates/security.md) | Plantilla de reporte del consumidor |
| [skills/security-review](../skills/security-review/SKILL.md) | Playbook de review de seguridad |

## 7. Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.3.0 | 2026-09-19 | Approved (aprobación humana del director técnico) |
| 0.3.0 | 2026-09-18 | Draft: trasplante genérico del extract H20; auth concreta fuera del core |
