---
name: whatsapp
description: "WhatsApp monitor dashboard for OpenClaw. Shows connection status, monitored groups with last message, config per group (read/write/mute), DM policies, GBrain storage status, and detected-but-unconfigured groups. Subcommands: /whatsapp (status dashboard), /whatsapp add <group>, /whatsapp remove <group>, /whatsapp groups, /whatsapp guide. Triggers: /whatsapp, whatsapp status, que grupos tengo, agrega grupo whatsapp, revisa whatsapp."
allowed-tools: Bash Read Write Agent
user-invocable: true
distribute-to: [claude, openclaw]
---

# /whatsapp — WhatsApp Monitor Dashboard

You are managing the WhatsApp channel on OpenClaw running on Jarvis (EC2).

## IMPORTANT: Always verify against live state

Never trust cached info. Every invocation MUST run the verification commands below and show REAL state.

## IMPORTANT: Self-regenerating behavior

Changes are made via CHAT (user tells you what to change), NOT by editing the .md file.
Every time /whatsapp runs, follow this EXACT sequence:

### Step 1 — Collect fresh data
Run ALL data collection commands (see below) to get real state.

### Step 2 — Apply any requested changes
If the user asked for changes (add group, activate feature, rename, etc.):
- Edit openclaw.json as needed
- Restart gateway: `systemctl --user restart openclaw-gateway`
- Verify: `openclaw channels status --channel whatsapp`

### Step 3 — Regenerate ~/whatsapp-status.md
Rewrite the file with fresh data using the EXACT format from the current ~/whatsapp-status.md.
Preserve all sections: ASCII header, resumen rapido, grupos monitoreados (with full config tables,
features ON/OFF, oportunidades inteligentes, systemPrompt), grupos detectados, DMs, GBrain storage,
configuracion completa, sistema, comandos, troubleshooting, archivos clave, auto-regeneracion.

### Step 4 — Update GBrain
If anything changed, save updated guide to gbrain:
```bash
cat ~/whatsapp-status.md | gbrain put guias/whatsapp-openclaw-setup
```

## OUTPUT FORMAT — Two parts, always both

### Part 1: Text response (directly to user)
A quick functional summary in conversational text. Example:

```
WhatsApp esta conectado y healthy. Tu numero +526624707325 vinculado.

Tienes 1 grupo monitoreado:
  - JPC — read-only, sin visto, guardando todo en GBrain. Ultimo mensaje hace 7 min: "thanks jonathan..."

3 grupos detectados disponibles para agregar:
  - 120363427149546617@g.us (ultimo: "MACBOOK: https://...")
  - 120363418735974556@g.us (ultimo: "Viral Videos")  
  - 5216623573702-1575495688@g.us (ultimo: "Quien renta asador?")

DMs: deshabilitados. Nadie puede escribirte por WhatsApp al bot.
GBrain: guia guardada, datos de JPC pendientes (esperando mensajes).
Sistema: 9h uptime, 5.5GB RAM, load 0.11.

Reporte completo: ~/whatsapp-status.md
```

Key rules for text response:
- Hablar claro, directo, en espanol
- Listar cada grupo con su estado real (read-only, puede responder, visto on/off, GBrain activo/no)
- Decir cuantos grupos detectados hay disponibles
- Mencionar alertas si algo esta mal
- Mention if any changes were applied
- Dar el path al .md al final
- Include the resumen rapido box showing connection, DMs, visto, modo, monitored/detected counts

### Part 2: Detailed .md report (saved to file)
Write a complete report to `~/whatsapp-status.md` using the template below.
The file MUST have:
- ASCII art WHATSAPP header
- Editable sections clearly marked
- Features table per group with ON/OFF toggles
- Custom rules block per group
- Sync rules explanation at the bottom

## FILE TEMPLATE — ~/whatsapp-status.md

Use this EXACT structure (fill with real data):

````markdown
```
 █     █░ ██░ ██  ▄▄▄     ▄▄▄█████▓  ██████  ▄▄▄       ██▓███   ██▓███
▓█░ █ ░█░▓██░ ██▒▒████▄   ▓  ██▒ ▓▒▒██    ▒ ▒████▄    ▓██░  ██▒▓██░  ██▒
▒█░ █ ░█ ▒██▀▀██░▒██  ▀█▄ ▒ ▓██░ ▒░░ ▓██▄   ▒██  ▀█▄  ▓██░ ██▓▒▓██░ ██▓▒
░█░ █ ░█ ░▓█ ░██ ░██▄▄▄▄██░ ▓██▓ ░   ▒   ██▒░██▄▄▄▄██ ▒██▄█▓▒ ▒▒██▄█▓▒ ▒
░░██▒██▓ ░▓█▒░██▓ ▓█   ▓██▒ ▒██▒ ░ ▒██████▒▒ ▓█   ▓██▒▒██▒ ░  ░▒██▒ ░  ░
░ ▓░▒ ▒   ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒ ░░   ▒ ▒▓▒ ▒ ░ ▒▒   ▓▒█░▒▓▒░ ░  ░▒▓▒░ ░  ░
  ▒ ░ ░   ▒ ░▒░ ░  ▒   ▒▒ ░   ░    ░ ░▒  ░ ░  ▒   ▒▒ ░░▒ ░     ░▒ ░
  ░   ░   ░  ░░ ░  ░   ▒    ░      ░  ░  ░    ░   ▒   ░░        ░░
    ░     ░  ░  ░      ░  ░            ░        ░  ░
```

# 📡 WhatsApp Command Center
> **Generado:** YYYY-MM-DD HH:MM UTC
> **Numero vinculado:** +526624707325 (Hermosillo)
> **Estado:** 🟢/🔴 CONNECTED/DISCONNECTED · HEALTHY/DEGRADED
> **Gateway:** active/inactive, uptime Xh, XMB RAM
> **Skill version:** 2.0

---

> **⚠️ ESTE ARCHIVO ES EDITABLE Y VIVO**
> (sync rules explanation here)

---

## 📊 Estado General
(connection status block + settings table)

---

## 📋 GRUPOS MONITOREADOS

### 🏗️ NOMBRE — Descripcion corta (EDITABLE)

| Campo | Valor |
|---|---|
| **Nombre** | NOMBRE |
| **ID** | `ID@g.us` |
| **Descripcion** | (EDITABLE — descripcion del grupo) |
| **Ultimo mensaje** | "texto..." (fecha) |
| **GBrain slug** | `whatsapp/slug/YYYY-MM-DD` |

**Resumen reciente:** (EDITABLE)
> Parrafo breve de contexto reciente del grupo.

#### Permisos y modo
(table: leer, responder, visto, reacciones, guardar, mencion)

#### Features activas
(table of ON features)

#### Features disponibles (se pueden activar)
(table with ⬜ OFF toggles — user can change to ✅ ON)

Features list:
- 📧 Alerta por correo — Cuando se mencione un tema critico, envia correo
- 📱 Forward a Telegram — Reenvia mensajes importantes a Telegram
- 🔍 Filtro por personas — Prioriza mensajes de personas especificas
- 🚨 Alertas por keyword — Alerta cuando se mencionen palabras clave
- 📅 Extractor de fechas — Detecta y lista fechas/deadlines
- 💰 Detector de montos — Detecta y registra montos/presupuestos

#### Reglas custom (EDITABLE)
```
# Agrega reglas aqui. Formato: una regla por linea, espanol natural.
# Se aplicaran en la proxima sincronizacion con /whatsapp.
```

#### SystemPrompt completo
(the full prompt in a code block)

---

(repeat for each monitored group)

## 🔍 GRUPOS DETECTADOS
(table of unmonitored groups seen in logs)

## 📨 DMs
(DM status)

## 🧠 GBrain Storage
(table of stored slugs)

## 🖥️ Sistema
(system metrics)

## 🛠️ Comandos Disponibles
(commands table)

## 📖 Como Crear un Agente para un Grupo Nuevo
(step by step guide)

## 🔧 Troubleshooting
(problems + solutions table)

## 📁 Archivos Clave
(paths table)

## 🔄 Reglas de Sincronizacion
(explanation of what's editable and what gets overwritten)
````

## Data collection commands

Run ALL of these to get real data. OpenClaw runs LOCALLY (not via SSH):

```bash
# 1. Channel status
openclaw channels status --channel whatsapp 2>&1 | grep -i whatsapp

# 2. Current config
python3 -c "
import json
with open('/home/ec2-user/.openclaw/openclaw.json') as f:
    cfg = json.load(f)
wa = cfg.get('channels', {}).get('whatsapp', {})
groups = wa.get('groups', {})
print('ENABLED:', wa.get('enabled'))
print('DM_POLICY:', wa.get('dmPolicy'))
print('GROUP_POLICY:', wa.get('groupPolicy'))
print('READ_RECEIPTS:', wa.get('sendReadReceipts'))
print('REACTION:', wa.get('reactionLevel'))
print('SELF_CHAT:', wa.get('selfChatMode'))
print('ALLOW_FROM:', wa.get('allowFrom'))
print('GROUP_COUNT:', len(groups))
for gid, gcfg in groups.items():
    mention = gcfg.get('requireMention', True)
    prompt = gcfg.get('systemPrompt', '')
    print(f'GROUP:{gid}|mention={mention}|prompt_len={len(prompt)}')
    print(f'PROMPT_FULL:{prompt}')
"

# 3. Groups seen in logs (today + yesterday)
for day in $(date +%Y-%m-%d) $(date -d yesterday +%Y-%m-%d); do
  grep "@g.us" /tmp/openclaw/openclaw-${day}.log 2>/dev/null | python3 -c "
import sys, json
groups = {}
for line in sys.stdin:
    try:
        d = json.loads(line)
        info = d.get('1', {})
        frm = info.get('from', '')
        body = info.get('body', '')
        ts = info.get('timestamp', 0)
        if '@g.us' in frm and body:
            groups[frm] = {'body': body[:80], 'ts': ts}
    except:
        pass
for gid, data in sorted(groups.items(), key=lambda x: x[1]['ts'], reverse=True):
    print(gid + '  |  ' + data['body'])
" 2>/dev/null
done

# 4. GBrain stored data
gbrain list 2>/dev/null | grep -i whatsapp

# 5. Gateway health
uptime; free -h | grep Mem
systemctl --user status openclaw-gateway 2>&1 | grep -E "Active|Memory"
```

## Subcommands

### `/whatsapp add`
User says "agrega grupo X" or "/whatsapp add":
1. List detected groups not yet in config
2. Ask which one to add and what name to give it
3. Ask what rules (save everything, only important, custom prompt)
4. Edit openclaw.json to add the group
5. Restart gateway
6. Verify with channels status
7. Regenerate ~/whatsapp-status.md with the new group included
8. Update gbrain guide

### `/whatsapp remove`
1. Show current monitored groups
2. Confirm which to remove
3. Edit openclaw.json
4. Restart gateway
5. Regenerate ~/whatsapp-status.md
6. Update gbrain guide

### `/whatsapp groups`
Just show the groups table (monitored + detected), no full dashboard.

### `/whatsapp guide`
Pull and display the guide from gbrain:
```bash
gbrain get guias/whatsapp-openclaw-setup
```

### `/whatsapp dm add <number>`
1. Change dmPolicy from disabled to allowlist (if not already)
2. Add number to allowFrom
3. Restart gateway
4. Regenerate ~/whatsapp-status.md
5. Update guide

### `/whatsapp dm remove <number>`
Reverse of add.

## Feature activation logic

When a feature is toggled ON (⬜ → ✅) in the .md file, append to the group's systemPrompt:

| Feature | What to append to systemPrompt |
|---|---|
| 📧 Alerta por correo | "7. CORREO: Si alguien menciona un tema critico o urgente, usa el plugin de correo para notificar a sergioduran@correo.com" |
| 📱 Forward a Telegram | "7. TELEGRAM: Reenvia mensajes importantes (decisiones, tareas, urgencias) al chat de Telegram del usuario" |
| 🔍 Filtro por personas | "7. PERSONAS PRIORITARIAS: Guarda TODO de las personas listadas en reglas custom. De los demas solo lo importante" |
| 🚨 Alertas por keyword | "7. ALERTAS: Cuando se mencionen las palabras clave listadas en reglas custom, marca el mensaje como ALERTA" |
| 📅 Extractor de fechas | "7. FECHAS: Detecta y lista todas las fechas, deadlines y eventos mencionados en una seccion ## Fechas detectadas" |
| 💰 Detector de montos | "7. MONTOS: Detecta y registra todos los montos, presupuestos y cifras mencionados en una seccion ## Montos detectados" |

## Rules for systemPrompt per group

Each group gets its own systemPrompt in the config. Current templates:

### Template: Save everything + summary (DEFAULT)
```
Eres un observador silencioso del grupo NOMBRE. REGLAS:
1. NUNCA respondas en el grupo.
2. GUARDA TODO en gbrain con slug whatsapp/SLUG/YYYY-MM-DD.
3. Formato: [HH:MM] Nombre: mensaje
4. Multimedia: [HH:MM] Nombre: [tipo recibido]
5. Al final: seccion "Resumen del dia" con decisiones, tareas, fechas, acuerdos.
```

### Template: Only important
```
Eres un observador silencioso del grupo NOMBRE. REGLAS:
1. NUNCA respondas en el grupo.
2. Solo guarda en gbrain lo importante: decisiones, tareas, fechas, acuerdos, problemas.
3. Ignora saludos, emojis, conversacion casual.
4. Slug: whatsapp/SLUG/YYYY-MM-DD
```

### Template: Focused on specific people
```
Eres un observador silencioso del grupo NOMBRE. REGLAS:
1. NUNCA respondas en el grupo.
2. Guarda TODO lo que digan: PERSONA1 (+52...), PERSONA2 (+52...).
3. De los demas, solo guarda decisiones y tareas.
4. Slug: whatsapp/SLUG/YYYY-MM-DD
```

## After ANY change

Always:
1. Restart: `systemctl --user restart openclaw-gateway`
2. Verify: `openclaw channels status --channel whatsapp`
3. Regenerate ~/whatsapp-status.md
4. Update gbrain guide
5. Save history snapshot if significant change

## Trigger phrases

- /whatsapp
- whatsapp status
- que grupos tengo
- como esta whatsapp
- agrega grupo whatsapp
- quita grupo whatsapp
- revisa whatsapp
- monitorea este grupo
- agrega a este numero
