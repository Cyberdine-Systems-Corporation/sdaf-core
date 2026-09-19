---
name: security-review
description: Revisa diffs contra el baseline H12 (QG-Sec §5.2). Usar en Testing+Review o al tocar superficie de seguridad.
---

# security-review

| Campo | Valor |
|--------|--------|
| ID | security-review |
| Versión | 0.3.2 |
| Estado | Approved |
| Prioridad | alta |
| Fecha | 2026-09-19 |
| Norma | [handbook/12](../../handbook/12-security-standards.md), [handbook/10](../../handbook/10-code-review-and-quality-gates.md), `templates/security.md` |

## Disparadores

- Diff que toca auth, roles, sesión, login, endpoints de API, manejo de secretos, dependencias o input externo.
- Gate 2 / review de PR con superficie de seguridad.
- Pedido explícito de “security review”.

## Pasos

1. Leer [H12](../../handbook/12-security-standards.md) §4–§5 (no pegar OWASP ni marcos overlay).
2. Comprobar secretos en el diff (passwords, connection strings, tokens).
3. Comprobar authz: rutas de producto vs públicas; coherencia con el **ADR de auth del consumidor** y ACC.
4. Buscar injection obvia (SQL crudo, comandos con input) y fetch a URL controlada por usuario (SSRF) sin spec/ADR.
5. Dependencias nuevas o actualizadas: si el review identifica CVE crítica, QG-Sec falla salvo ADR de excepción fechado. No exigir scanner salvo overlay §3 con ADR.
6. Overlays de H12 §3: `N/A` o cumplidos según ADR del consumidor (justificar en worklog). No inventar umbrales.
7. Si hay hallazgo explotable nuevo: orientar a `SECURITY.md` del consumidor ([plantilla](../../templates/security.md)); no publicar PoC en issue abierto.
8. Registrar en worklog `security-review@0.3.2` + dictamen (bloqueante / mayor / menor según H10).

> [!CAUTION]
> QG-Sec fallido es bloqueante. No merge.

## Definition of Done

- [ ] Checklist H12 §5.1 recorrido en el alcance del diff.
- [ ] QG-Sec evaluado (pass/fail) según H12 §5.2.
- [ ] Worklog actualizado.

## Restricciones

- No exigir MFA/SSO ni ASVS completo salvo que el MVP del consumidor lo declare In.
- No marcar como bug el Out documentado en el ADR de auth del consumidor.
- No exigir overlays de H12 §3 (SSDF, SBOM, AIMS, …) sin ADR.
- No inventar controles de producción fuera de norma.

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.3.2 | 2026-09-19 | Prioridad alta; QG-Sec §5.2 (injection, SSRF, CVE identificada); overlays N/A salvo ADR |
| 0.3.0 | 2026-09-19 | Approved (aprobación humana del director técnico) |

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| 📖 | [H12](../../handbook/12-security-standards.md) | Baseline, catálogo §3 y QG-Sec |
| 📖 | [H10](../../handbook/10-code-review-and-quality-gates.md) | Severidad |
| 📝 | [templates/security.md](../../templates/security.md) | Reporte sin PoC público |
