---
name: security-review
description: Revisa diffs de auth, sesión, endpoints o secretos contra el baseline H12 (OWASP-aware, sin secretos). Usar en Testing+Review o al tocar superficie de seguridad.
---

# security-review

| Campo | Valor |
|--------|--------|
| ID | security-review |
| Versión | 0.3.0 |
| Estado | Draft |
| Prioridad | media |
| Fecha | 2026-09-18 |
| Norma | [handbook/12](../../handbook/12-security-standards.md), [handbook/10](../../handbook/10-code-review-and-quality-gates.md), `templates/security.md` |

## Disparadores

- Diff que toca auth, roles, sesión, login, endpoints de API, manejo de secretos o input externo.
- Gate 2 / review de PR con superficie de seguridad.
- Pedido explícito de “security review”.

## Pasos

1. Leer [H12](../../handbook/12-security-standards.md) §4–§5 (no pegar OWASP entero).
2. Comprobar secretos en el diff (passwords, connection strings, tokens).
3. Comprobar authz: rutas de producto vs públicas; coherencia con el **ADR de auth del consumidor** y ACC.
4. Buscar injection obvia (SQL crudo, comandos con input).
5. Si hay hallazgo explotable nuevo: orientar a `SECURITY.md` del consumidor ([plantilla](../../templates/security.md)); no publicar PoC en issue abierto.
6. Registrar en worklog `security-review@0.3.0` + dictamen (bloqueante / mayor / menor según H10).

> [!CAUTION]
> QG-Sec fallido es bloqueante. No merge.

## Definition of Done

- [ ] Checklist H12 §5.1 recorrido en el alcance del diff.
- [ ] QG-Sec evaluado (pass/fail).
- [ ] Worklog actualizado.

## Restricciones

- No exigir MFA/SSO ni ASVS completo salvo que el MVP del consumidor lo declare In.
- No marcar como bug el Out documentado en el ADR de auth del consumidor.
- No inventar controles de producción fuera de norma.

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| 📖 | [H12](../../handbook/12-security-standards.md) | Baseline y QG-Sec |
| 📖 | [H10](../../handbook/10-code-review-and-quality-gates.md) | Severidad |
| 📝 | [templates/security.md](../../templates/security.md) | Reporte sin PoC público |
