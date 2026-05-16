# IAM sergio-admin — MFA Setup + Root Keys Cleanup

**Estado actual (2026-05-16):**
- ✅ User `sergio-admin` creado con AdministratorAccess
- ✅ Access keys nuevas en `~/.aws/credentials` (EC2 jarvis-v3)
- ✅ Verified: `aws sts get-caller-identity` retorna `:user/sergio-admin` (ya NO `:root`)
- 🔴 Root access keys aún ACTIVAS (Sergio decide cuándo borrarlas via consola)
- 🔴 MFA en sergio-admin NO configurado (Sergio lo hace manualmente)

## Paso 1 — Configurar MFA en sergio-admin

Tu Claude no puede hacerlo (requiere tu teléfono). Hazlo así:

1. Login en AWS Console como **root** (todavía) → https://signin.aws.amazon.com
2. Search bar → "IAM"
3. Users → `sergio-admin` → Security credentials tab
4. Multi-factor authentication (MFA) → Assign MFA device
5. Recomendado: **Virtual MFA device** (Google Authenticator, 1Password, Authy)
6. Scan QR con tu app
7. Type 2 consecutive 6-digit codes
8. ✅ MFA activo

## Paso 2 — También MFA en root user (CRÍTICO)

Mismo proceso pero para root:
1. Console as root → tu nombre arriba derecha → "Security credentials"
2. "Multi-factor authentication (MFA)" → Assign MFA device
3. Misma app authenticator (puedes tener 2 entradas, una para root, otra para sergio-admin)

## Paso 3 — Si Mac también usa AWS CLI, rotar ahí también

```bash
# En tu Mac:
cat ~/.aws/credentials
# Si tiene aws_access_key_id = AKIA3H... (root) → REEMPLAZAR

# Crear access keys de sergio-admin (de la consola o desde la EC2):
# Console: IAM → users → sergio-admin → Security credentials → Create access key
# O desde la EC2 (con las nuevas creds): aws iam create-access-key --user-name sergio-admin

# Editar ~/.aws/credentials:
[default]
aws_access_key_id = AKIA3HLNVAV2...        # las nuevas
aws_secret_access_key = ...                 # las nuevas
```

## Paso 4 — Probar 24-48h y luego BORRAR root access keys

Espera 24-48 horas operando con sergio-admin. Si nada se rompe:

1. Login as root en consola
2. IAM → Users → root (en realidad: Account settings → Security credentials)
3. **Access keys** section → 2 keys activas (AKIA3H...)
4. Para cada una: **Deactivate** primero (revierte si algo se rompe)
5. Esperar otras 24h
6. Si sigue funcionando → **Delete** ambas keys

**ALTERNATIVA SEGURA:** En lugar de borrar, dejar **deactivated** permanentemente.
Si se reactivan accidentalmente, AWS lo loguea en CloudTrail → GuardDuty alerta.

## Paso 5 — Verificación post-rotation

Desde la EC2:
```bash
# Re-correr lie-detector — claim 14 debería seguir ✅
bash /home/ec2-user/.openclaw/skills/gbrain/run.sh verify | grep "AWS CLI"
# → | 14 | AWS CLI no usa root keys | arn:aws:iam::771713467764:user/sergio-admin | ✅ |
```

## Mejor práctica futura

- **Root account**: solo para tareas que requieren root (cambiar plan, cerrar cuenta, billing root). Cero access keys, solo password + MFA.
- **sergio-admin**: tu uso diario. AdministratorAccess. MFA obligatorio. Keys rotadas cada 90 días.
- **Otros users**: específicos por servicio (ej. github-actions-user). Permisos mínimos. Keys rotadas auto.

## Backup files

```
~/.aws/credentials.bak-root-20260516-012610  ← root keys originales (para emergency rollback)
```

Borrar este backup SOLO cuando MFA + sergio-admin probados por 48h.
