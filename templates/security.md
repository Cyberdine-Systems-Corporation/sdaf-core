# Plantilla — SECURITY.md del consumidor

| Campo | Valor |
|--------|--------|
| Versión | 0.3.2 |
| Estado | Approved |
| Fecha | 2026-09-19 |
| Norma | [handbook/12-security-standards.md](../handbook/12-security-standards.md) |

El consumidor copia esta plantilla a `SECURITY.md` en la raíz de su repo. No sustituye H12 ni el ADR de auth.

---

## Cómo reportar

1. **No** abras un issue público con PoC explotable ni secretos.
2. Contacta al canal privado que el producto declare (correo, Security advisory de GitHub, etc.).
3. Incluye: componente afectado, versión/commit, impacto, pasos **mínimos** (sin payload de ataque si se puede describir el defecto).

## Alcance

Baseline del método: [H12](../handbook/12-security-standards.md) (QG-Sec §5.2, secretos, authz según ADR del consumidor).

Fuera de alcance del método salvo ADR: ASVS completo, pentest obligatorio, MFA/SSO, overlays de H12 §3 (SSDF, SBOM/AIBOM, AIMS / AI Act / CRA).

## Historial

| Versión | Fecha | Cambio |
|---------|--------|--------|
| 0.3.2 | 2026-09-19 | Alcance: QG-Sec §5.2; overlays H12 §3 N/A salvo ADR |
| 0.3.0 | 2026-09-19 | Approved (aprobación humana del director técnico) |
| 0.3.0 | 2026-09-18 | Borrador de plantilla para el trasplante H12 |
