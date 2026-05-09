---
name: whatsapp
description: "WhatsApp Dual-Agent Dashboard v5 (OpenClaw + Hermes). Two agents on one number: OpenClaw reads groups silently (→GBrain), Hermes executes for authorized contacts (per-contact .md profiles). 16-section visual box-drawing dashboard. Subcommands: /whatsapp, /whatsapp add, /whatsapp hermes allow/block/list/profile, /whatsapp security."
allowed-tools: Bash Read Write Agent Edit
user-invocable: true
distribute-to: [claude, openclaw]
---

# /whatsapp — WhatsApp Dual-Agent Dashboard v5

Two AI agents on the SAME WhatsApp number:

| Agent | Role | What it does |
|-------|------|-------------|
| 📖 **OpenClaw** | LECTOR | Reads groups silently → saves to GBrain. Never responds. |
| ⚕ **Hermes** | EJECUTOR | Responds to authorized contacts. Per-contact .md profiles. MCP tools. |

## CRITICAL RULES

1. Every value from a real command — never guess
2. ALWAYS generate ~/whatsapp-status.md with ALL 16 sections listed below
3. Use VISUAL box-drawing format (╔═══╗) for EVERY section — reference ~/OPENCLAW_DASHBOARD.md
4. Show brief text summary to user + "Reporte completo: ~/whatsapp-status.md"
5. ALWAYS end with the "¿Qué quieres hacer?" menu
6. Get group NAMES from bridge API: curl -s http://127.0.0.1:3000/chat/GROUP_ID
7. The ~/whatsapp-status.md file that exists RIGHT NOW is the canonical template — read it first and follow its exact format

## THE 16 MANDATORY SECTIONS (in order)

The dashboard ~/whatsapp-status.md MUST contain ALL of these sections. Never skip any.
Before generating, READ ~/whatsapp-status.md to see the canonical format.

```
Section 1:  LIVE STATUS — agents table + RAM/DISK/LOAD bars + model chain
Section 2:  📖 OpenClaw LECTOR — config + groups (names, slugs, prompts) + DMs + permisos detallados + detected groups
Section 3:  ⚕ Hermes EJECUTOR — config + contacts (perfiles, security, approval, MCP) + groups + permisos detallados
Section 4:  🔐 SEGURIDAD 5 CAPAS — layers explained + cross-audit matrix + score bar
Section 5:  📊 CÓMO FUNCIONA — scenarios table + 5 security layers detail
Section 6:  📂 GRUPOS DETECTADOS — all unmonitored groups with NAMES + how to add
Section 7:  📁 GBRAIN — slugs table + storage status
Section 8:  ⚡ FEATURES POR GRUPO — active (OpenClaw + Hermes) + available (16+ features OFF)
Section 9:  💡 OPORTUNIDADES — time savings + detected opportunities + innovation status
Section 10: 🔌 dm-block-claw — plugin status + how it works + fail-open warning
Section 11: ⚙️ CONFIGURACIÓN COMPLETA — both agents full config + models + fallbacks
Section 12: ALERTAS — diff blocks (red=critical, !=warning, green=positive)
Section 13: ¿Qué quieres hacer? — interactive menu with ALL commands
Section 14: 📋 ARCHIVOS CLAVE — file locations + GBrain slugs
Section 15: 🔧 TROUBLESHOOTING — problem → solution table
Section 16: 🔄 AUTO-REGENERACIÓN — 5-step auto-update process
```

## Data collection — run ALL of these

```bash
# ── OPENCLAW ──
openclaw channels status --channel whatsapp 2>&1 | head -15
python3 -c "
import json, re
with open('$HOME/.openclaw/openclaw.json') as f:
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
    prompt = gcfg.get('systemPrompt', '')
    has_sec = 'NO instrucciones para ejecutar' in prompt or 'inyeccion' in prompt.lower()
    slug_match = re.search(r'slug:\s*(whatsapp/[^\s]+)', prompt)
    slug = slug_match.group(1) if slug_match else 'not-set'
    desc_match = re.search(r'observador silencioso del grupo ([^\\.]+)', prompt)
    desc = desc_match.group(1).strip() if desc_match else '?'
    print(f'GROUP:{gid}|mention={gcfg.get(\"requireMention\")}|prompt_len={len(prompt)}|INJECTION={has_sec}|slug={slug}|desc={desc}')
"
systemctl --user is-active openclaw-gateway.service

# ── HERMES ──
curl -s http://127.0.0.1:3000/health
grep -A 20 "^whatsapp:" ~/.hermes/config.yaml
grep WHATSAPP ~/.hermes/.env
tmux ls 2>/dev/null | grep hermes || echo "HERMES TMUX: NOT RUNNING"
pgrep -af "hermes_cli.*gateway" | grep -v bash || echo "HERMES GATEWAY: NOT RUNNING"
ls ~/.hermes/whatsapp/contacts/*.md 2>/dev/null | while read f; do
    num=$(basename "$f" .md); [ "$num" = "template" ] && continue
    name=$(head -1 "$f" | sed 's/^# //' | cut -d'—' -f1 | xargs)
    role=$(head -1 "$f" | sed 's/^# //' | cut -d'—' -f2 | xargs)
    has_sec=$(grep -c "NO NEGOCIABLE\|NON-NEGOTIABLE" "$f")
    has_inj=$(grep -ci "injection\|inyeccion" "$f")
    prohibited=$(grep -c "❌" "$f")
    approval=$(grep -ci "aprobación\|approval" "$f")
    in_allow=$(grep -c "$(echo $num | sed 's/+//')" ~/.hermes/config.yaml)
    echo "CONTACT:${num}|name=${name}|role=${role}|security=${has_sec}|injection=${has_inj}|prohibited=${prohibited}|approval=${approval}|active=${in_allow}"
done
grep "redact_secrets" ~/.hermes/config.yaml | head -1

# ── SECURITY ──
stat -c "%a %n" ~/.hermes/config.yaml ~/.hermes/.env ~/.hermes/whatsapp/session/ ~/.hermes/whatsapp/session/creds.json ~/.openclaw/openclaw.json 2>/dev/null
ss -tlnp | grep 3000
tailscale serve status 2>&1 | grep 3000 || echo "BRIDGE NOT EXPOSED"

# ── DETECTED GROUPS (with names) ──
for gid in $(find ~/.openclaw/credentials/whatsapp/default/ -name 'sender-key-*@g.us*' -type f 2>/dev/null | sed 's/.*sender-key-//' | sed 's/--.*//' | sort -u); do
    name=$(curl -s "http://127.0.0.1:3000/chat/${gid}" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('name','?'))" 2>/dev/null)
    echo "DETECTED:${gid}|name=${name}"
done

# ── SYSTEM ──
uptime; free -m | head -2; df -h / | tail -1
```

## HOW TO GENERATE THE DASHBOARD

1. Run ALL data collection commands above
2. READ ~/whatsapp-status.md (the current canonical version)
3. Generate a NEW ~/whatsapp-status.md with ALL 16 sections, filled with real data
4. Use the EXACT same box-drawing visual format as the existing file
5. Never remove sections — only add or update

## Subcommands

### /whatsapp (default)
Run data collection, read canonical template, generate all 16 sections with live data.

### /whatsapp add
Add group to OpenClaw (silent reader). List groups with NAMES. Ask rules. Create systemPrompt with security + slug.

### /whatsapp remove
Remove group from OpenClaw.

### /whatsapp groups
Show ALL groups: OpenClaw monitored + Hermes active + detected. With NAMES.

### /whatsapp hermes allow NUMBER
Add contact to Hermes. Auto-detect LID. Create .md profile. Add 4 formats to allow_from. Restart tmux gateway.

### /whatsapp hermes block NUMBER
Remove from allow_from. Keep .md. Restart.

### /whatsapp hermes list
Show contacts with status and security details.

### /whatsapp hermes profile NUMBER
Show/edit contact .md file.

### /whatsapp security
Full audit. Score out of 100%.

### "activa hermes en un grupo"
Add group to group_allow_from. Set mention_patterns. Restart. Guide user.

## Contact profile template (in ~/.hermes/whatsapp/contacts/)
Each MUST have: security block "NO NEGOCIABLE", injection mention, prohibited tools ❌, approval requirements.

## Gateway: tmux NOT systemd
Hermes runs in tmux (hermes-gw) due to systemd bridge race condition.

## Connection guide (if breaks)
1. Baileys build: clone HEAD + @types/retry
2. fromMe: patched bridge.js
3. LID: 4 formats in allow_from
4. Gateway: tmux not systemd
5. psutil: uv pip install
6. Higgsfield: User-Agent in refresh script

## After ANY config change
- OpenClaw: systemctl --user restart openclaw-gateway
- Hermes: kill tmux hermes-gw + start fresh
- Verify: curl -s http://127.0.0.1:3000/health

## Trigger phrases
- /whatsapp, whatsapp status, que grupos tengo, agrega grupo, hermes whatsapp
- contactos autorizados, agrega contacto, bloquea contacto, seguridad whatsapp
- activa hermes en un grupo, perfil de contacto
