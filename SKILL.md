---
name: whatsapp
description: "WhatsApp Dual-Agent Dashboard (OpenClaw + Hermes). Shows both agents side by side: OpenClaw groups (read-only), Hermes contacts (executor). Manage contact profiles, authorize/block users, view security status. Subcommands: /whatsapp, /whatsapp add <group>, /whatsapp hermes allow <num>, /whatsapp hermes block <num>, /whatsapp hermes profile <num>, /whatsapp hermes list."
allowed-tools: Bash Read Write Agent Edit
user-invocable: true
distribute-to: [claude, openclaw]
---

# /whatsapp — WhatsApp Dual-Agent Dashboard v3

You are managing TWO WhatsApp agents on the same phone number:

1. **OpenClaw** — LECTOR silencioso (lee grupos, guarda en GBrain, nunca responde)
2. **Hermes** — EJECUTOR (responde a contactos autorizados, ejecuta MCP tools)

## IMPORTANT: Always verify against live state

Never trust cached info. Every invocation MUST run verification commands and show REAL state.

## OUTPUT FORMAT — Two parts, always both

### Part 1: Text response (directly to user)

```
WhatsApp Dual-Agent Dashboard

📖 OpenClaw (LECTOR)
  Conexión: ✅ connected | Número: +526624707325
  Grupos monitoreados: 2
    - JPC         read-only ✅  slug: whatsapp/jpc/
    - JPC-Dev     read-only ✅  slug: whatsapp/jpc-dev/
  DMs: allowlist (3 números) — solo lectura
  Grupos detectados sin monitorear: 25

⚕ Hermes (EJECUTOR)
  Conexión: ✅ connected | Bridge: port 3000
  Contactos autorizados: 1
    - 👤 Sergio (+526624707325)  admin  ✅
    - 👤 Jason (+13058495648)    consultoría  ✅
  Grupos: disabled
  Seguridad: allowlist + perfiles por contacto

⚠️ Alertas: (si las hay)

Reporte completo: ~/whatsapp-status.md
```

### Part 2: Detailed .md report (saved to ~/whatsapp-status.md)

## Data collection commands

Run ALL of these to get real data:

```bash
# ── OPENCLAW ──
echo "=== OPENCLAW STATUS ==="; openclaw channels status --channel whatsapp 2>&1 | head -10
echo "=== OPENCLAW CONFIG ==="; python3 -c "
import json
with open('/home/ec2-user/.openclaw/openclaw.json') as f:
    cfg = json.load(f)
wa = cfg.get('channels', {}).get('whatsapp', {})
print('ENABLED:', wa.get('enabled'))
print('DM_POLICY:', wa.get('dmPolicy'))
print('GROUP_POLICY:', wa.get('groupPolicy'))
print('READ_RECEIPTS:', wa.get('sendReadReceipts'))
print('REACTION:', wa.get('reactionLevel'))
print('ALLOW_FROM:', wa.get('allowFrom'))
groups = wa.get('groups', {})
print(f'GROUP_COUNT: {len(groups)}')
for gid, gcfg in groups.items():
    mention = gcfg.get('requireMention', True)
    prompt = gcfg.get('systemPrompt', '')
    has_security = 'NO instrucciones para ejecutar' in prompt or 'inyeccion' in prompt.lower()
    print(f'GROUP:{gid}|mention={mention}|prompt_len={len(prompt)}|INJECTION_PROTECTED={has_security}')
"
echo "=== OPENCLAW GATEWAY ==="; systemctl --user is-active openclaw-gateway.service

# ── HERMES ──
echo "=== HERMES BRIDGE ==="; curl -s http://127.0.0.1:3000/health 2>&1
echo "=== HERMES CONFIG ==="; grep -A 8 "^whatsapp:" ~/.hermes/config.yaml | head -10
echo "=== HERMES ENV ==="; grep WHATSAPP ~/.hermes/.env
echo "=== HERMES GATEWAY ==="; systemctl --user is-active hermes-gateway.service
echo "=== HERMES CONTACTS ==="; ls ~/.hermes/whatsapp/contacts/*.md 2>/dev/null | while read f; do
    num=$(basename "$f" .md)
    name=$(head -1 "$f" | sed 's/^# //' | cut -d'—' -f1 | xargs)
    role=$(head -1 "$f" | sed 's/^# //' | cut -d'—' -f2 | xargs)
    echo "CONTACT:${num}|name=${name}|role=${role}"
done
echo "=== HERMES SECURITY ==="; grep "redact_secrets" ~/.hermes/config.yaml | head -1
echo "=== SESSION PERMS ==="; stat -c "%a" ~/.hermes/whatsapp/session/ 2>/dev/null
echo "=== CREDS PERMS ==="; stat -c "%a" ~/.hermes/whatsapp/session/creds.json 2>/dev/null

# ── SHARED ──
echo "=== DETECTED GROUPS ==="; find ~/.openclaw/credentials/whatsapp/default/ -name 'sender-key-*@g.us*' -type f 2>/dev/null | sed 's/.*sender-key-//' | sed 's/--.*//' | sort -u
echo "=== SYSTEM ==="; uptime; free -h | grep Mem
```

## Report template (~/whatsapp-status.md)

```markdown
# WhatsApp Dual-Agent Dashboard
> Generado: YYYY-MM-DD HH:MM UTC
> Skill version: 3.0

---

## 📖 OpenClaw — LECTOR

| Campo | Estado |
|---|---|
| Conexión | connected/disconnected |
| Número | +526624707325 |
| Modo | Read-only (observador silencioso) |
| Gateway | active/inactive |

### Configuración
| Setting | Valor | Significado |
|---|---|---|
| dmPolicy | allowlist | Solo números autorizados |
| groupPolicy | allowlist | Solo grupos configurados |
| sendReadReceipts | false | Sin visto azul |
| reactionLevel | off | Sin reacciones |

### Grupos Monitoreados
| Grupo | ID | Modo | Injection Protected | GBrain Slug |
|---|---|---|---|---|
| JPC | xxx@g.us | read-only | ✅ | whatsapp/jpc/ |

### DMs Permitidos (lectura)
| Número | Estado |
|---|---|
| +526624707325 | ✅ |

---

## ⚕ Hermes — EJECUTOR

| Campo | Estado |
|---|---|
| Conexión | connected/disconnected |
| Bridge | port 3000, uptime Xs |
| Gateway | active/inactive |
| Secrets Redaction | true/false |
| Session Perms | 700/600 |

### Configuración
| Setting | Valor | Significado |
|---|---|---|
| dm_policy | allowlist | Solo contactos autorizados |
| allow_from | [...] | Lista de números |
| unauthorized_dm_behavior | ignore | Silencio total |
| group_policy | disabled/allowlist | Grupos off o selectivos |
| require_mention | true/false | En grupos, requiere mención |

### Contactos Autorizados
| # | Nombre | Número | Rol | Perfil | Permisos |
|---|---|---|---|---|---|
| 1 | Sergio | +526624707325 | Admin | ✅ | Todo |
| 2 | Jason | +13058495648 | Consultoría | ✅ | Read-only GBrain |

### Seguridad por Contacto
| Contacto | Archivo | Injection Protection | Approval Required | Prohibited Tools |
|---|---|---|---|---|
| Sergio | ✅ +526624707325.md | ✅ | No (admin) | Ninguno |
| Jason | ✅ +13058495648.md | ✅ | Sí (modificaciones) | put_page, terminal |

---

## 🔐 Seguridad Global

| Check | OpenClaw | Hermes |
|---|---|---|
| Config perms (600) | ✅/❌ | ✅/❌ |
| Session perms (700/600) | ✅/❌ | ✅/❌ |
| Injection protection | ✅/❌ per group | ✅/❌ per contact |
| Secrets redaction | N/A | ✅/❌ |
| Port exposure | N/A | 127.0.0.1 only ✅/❌ |

---

## 📊 Cuándo usar cada uno

| Escenario | Agente | Ejemplo |
|---|---|---|
| Monitorear grupo de trabajo | OpenClaw | Lee JPC, guarda en GBrain |
| Cliente pide métricas de ads | Hermes | Karina consulta Meta Ads |
| Guardar decisiones de grupo | OpenClaw | Registra acuerdos en GBrain |
| Traducir PDF en grupo personal | Hermes | Tú pides traducción en JCD |
| Ejecutar campaña aprobada | Hermes | Sergio autoriza, Hermes ejecuta |

---

## Comandos disponibles

| Comando | Qué hace |
|---|---|
| /whatsapp | Este dashboard |
| /whatsapp add <grupo> | Agregar grupo a OpenClaw |
| /whatsapp remove <grupo> | Quitar grupo de OpenClaw |
| /whatsapp groups | Tabla de grupos |
| /whatsapp hermes allow <num> | Autorizar contacto en Hermes |
| /whatsapp hermes block <num> | Bloquear contacto en Hermes |
| /whatsapp hermes list | Ver contactos autorizados |
| /whatsapp hermes profile <num> | Ver/editar perfil de contacto |
| /whatsapp security | Auditoría de seguridad |
```

## Subcommands

### `/whatsapp` (default)
Run all data collection, show text summary + save report.

### `/whatsapp add <group>`
Same as v2 — add group to OpenClaw config.

### `/whatsapp remove <group>`
Same as v2 — remove group from OpenClaw config.

### `/whatsapp groups`
Show groups table only (OpenClaw monitored + detected unmonitored).

### `/whatsapp hermes allow <number>`
1. Validate number format (country code, no +, no spaces)
2. Check if contact profile exists in `~/.hermes/whatsapp/contacts/`
3. If no profile: create from template, ask user to fill in role/permissions
4. Add number to `allow_from` in `~/.hermes/config.yaml`
5. Restart Hermes gateway: `systemctl --user restart hermes-gateway.service`
6. Verify bridge status: `curl -s http://127.0.0.1:3000/health`
7. Show confirmation with contact's permissions summary

### `/whatsapp hermes block <number>`
1. Remove number from `allow_from` in `~/.hermes/config.yaml`
2. Do NOT delete the profile file (keep for records)
3. Restart Hermes gateway
4. Verify
5. Show confirmation

### `/whatsapp hermes list`
Show all contact profiles with their permissions:
```bash
ls ~/.hermes/whatsapp/contacts/*.md 2>/dev/null | while read f; do
    num=$(basename "$f" .md)
    name=$(head -1 "$f" | sed 's/^# //' | cut -d'—' -f1 | xargs)
    role=$(head -1 "$f" | sed 's/^# //' | cut -d'—' -f2 | xargs)
    in_allow=$(grep -c "$num" ~/.hermes/config.yaml 2>/dev/null)
    status="❌ blocked"
    [ "$in_allow" -gt 0 ] && status="✅ active"
    echo "$status  $name ($num) — $role"
done
```

### `/whatsapp hermes profile <number>`
1. Read the contact's .md file
2. Show it formatted
3. Ask if user wants to edit permissions
4. If yes, open for editing

### `/whatsapp security`
Run full security audit:
- Check all config file permissions (600)
- Check session directory permissions (700)
- Check each contact profile has injection protection section
- Check secrets redaction is enabled
- Check bridge port is localhost only
- Check Tailscale doesn't expose bridge
- Score out of 100%

## Contact profile management

Profiles live in `~/.hermes/whatsapp/contacts/[number].md`

Template at `~/.hermes/whatsapp/contacts/template.md`

When creating a new profile, ask the user:
1. Name
2. Role/relationship
3. What they can do freely
4. What requires Sergio's approval
5. What is prohibited
6. Any MCP tools to enable
7. Any account credentials (store as env vars, never plaintext)

## Security rules for contact profiles

Each profile MUST have the security block at the top. When scanning profiles, check for:
- "NO NEGOCIABLE" in the security section
- "prompt injection" mentioned
- "NUNCA revelar" mentioned
- Prohibited tools listed
If any are missing, flag as ⚠️ in the dashboard.

## Config file locations

| File | Purpose |
|---|---|
| ~/.openclaw/openclaw.json | OpenClaw WhatsApp config |
| ~/.hermes/config.yaml | Hermes WhatsApp config |
| ~/.hermes/.env | Hermes env vars (WHATSAPP_MODE, etc.) |
| ~/.hermes/whatsapp/session/ | Baileys session (protect 700) |
| ~/.hermes/whatsapp/contacts/*.md | Contact profiles |
| ~/whatsapp-status.md | Generated report |

## After ANY config change

Always:
1. Restart the affected service:
   - OpenClaw: `systemctl --user restart openclaw-gateway`
   - Hermes: `systemctl --user restart hermes-gateway`
2. Verify OpenClaw: `openclaw channels status --channel whatsapp`
3. Verify Hermes: `curl -s http://127.0.0.1:3000/health`

## Trigger phrases

- /whatsapp
- whatsapp status
- que grupos tengo
- agrega grupo whatsapp
- revisa whatsapp
- hermes whatsapp
- contactos autorizados
- agrega contacto hermes
- bloquea contacto
- perfil de contacto
- seguridad whatsapp
