```diff
- ╔═══════════════════════════════════════════════════════════════════════╗
- ║  __        ___         _       _                                    ║
- ║  \ \      / / |__   __ _| |_ ___/ \   _ __  _ __                    ║
- ║   \ \ /\ / /| '_ \ / _` | __/ __| |  | '_ \| '_ \                  ║
- ║    \ V  V / | | | | (_| | |_\__ \ |__| |_) | |_) |                  ║
- ║     \_/\_/  |_| |_|\__,_|\__|___/\____| .__/| .__/                   ║
- ║                                        |_|   |_|                     ║
- ║      DUAL-AGENT DASHBOARD v4.0 · 2026-05-09 07:51 UTC              ║
- ║      Number: +5215551234567                                           ║
- ╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 1. LIVE STATUS

```
╔══════════════════════════════════════════════════════════════╗
║  AGENT              ROLE        STATE          UPTIME       ║
╠══════════════════════════════════════════════════════════════╣
║  📖 OpenClaw        LECTOR      ✅ active       14h         ║
║  ⚕ Hermes          EJECUTOR    ✅ active (tmux) 45min      ║
║  🌉 WA Bridge       TRANSPORT   ✅ connected     45min      ║
╠══════════════════════════════════════════════════════════════╣
║  RAM    ███████████░░░░░░░░░  4470/7823 MB (57%)            ║
║  LOAD   ██░░░░░░░░░░░░░░░░░░  0.47 (low)                   ║
║  UPTIME 0 days, 14h 32m                                     ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. 📖 OpenClaw — LECTOR

```
╔══════════════════════════════════════════════════════════════╗
║  CONFIGURACIÓN                                              ║
╠══════════════════════════════════════════════════════════════╣
║  enabled          true          Canal activo                 ║
║  dmPolicy         allowlist     Solo números autorizados     ║
║  groupPolicy      allowlist     Solo grupos configurados     ║
║  sendReadReceipts false         Sin visto azul               ║
║  reactionLevel    off           Sin reacciones               ║
╠══════════════════════════════════════════════════════════════╣
║  GRUPOS MONITOREADOS (2)                                     ║
╠══════════════════════════════════════════════════════════════╣
║  ✅ Work Group A    EXAMPLE_GROUP_ID_1@g.us               ║
║     read-only · mention: off · 🔒 injection ✅ · 2652 chars ║
║  ✅ Work Group B  EXAMPLE_GROUP_ID_2@g.us               ║
║     read-only · mention: off · 🔒 injection ✅ · 2696 chars ║
╠══════════════════════════════════════════════════════════════╣
║  DMs PERMITIDOS (lectura)                                    ║
╠══════════════════════════════════════════════════════════════╣
║  ✅ +13055559876    Alex                                    ║
║  ✅ +17605558765    (contacto)                               ║
║  ❌ Owner removido — Hermes maneja sus DMs ahora            ║
╠══════════════════════════════════════════════════════════════╣
║  Grupos detectados sin monitorear: 27                        ║
║  Usa /whatsapp add para agregar                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 3. ⚕ Hermes — EJECUTOR

```
╔══════════════════════════════════════════════════════════════╗
║  CONFIGURACIÓN                                              ║
╠══════════════════════════════════════════════════════════════╣
║  dm_policy         allowlist     Solo contactos autorizados  ║
║  allow_from        [4 entries]   Owner (phone+LID x2)      ║
║  unauthorized_dm   ignore        Silencio total              ║
║  group_policy      allowlist     Solo grupos autorizados     ║
║  mention_patterns  hermes        Invocación en grupos        ║
║  secrets_redaction true          Tokens ocultos en logs      ║
║  gateway           tmux          hermes-gw session           ║
╠══════════════════════════════════════════════════════════════╣
║  CONTACTOS                                                   ║
╠══════════════════════════════════════════════════════════════╣
║  👤 Your Name   +5215551234567   Admin (Full Access)       ║
║     🔒 security ✅  ⚠️ approval: no (admin)  ✅ ACTIVO      ║
║                                                              ║
║  👤 Alex          +13055559876    Consultoría & Desarrollo  ║
║     🔒 security ✅  ⚠️ approval: sí  ❌ NO ACTIVO           ║
║     (tiene perfil .md pero NO está en allow_from)            ║
╠══════════════════════════════════════════════════════════════╣
║  GRUPOS HERMES (ejecutor)                                    ║
╠══════════════════════════════════════════════════════════════╣
║  ✅ Curso          EXAMPLE_GROUP_ID_3@g.us                   ║
║     mention: "hermes" · solo owner · require_mention: true   ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 4. 🔐 SEGURIDAD

```
╔══════════════════════════════════════════════════════════════╗
║  CHECK                        OPENCLAW        HERMES        ║
╠══════════════════════════════════════════════════════════════╣
║  Config perms (600)           ✅ 600          ✅ 600         ║
║  .env perms (600)             N/A             ✅ 600         ║
║  Session perms (700/600)      ✅              ✅ 700/600     ║
║  Injection protection         ✅ 2/2 grupos   ✅ 2/2 perfiles║
║  Secrets redaction            N/A             ✅ true        ║
║  Bridge port (localhost)      N/A             ✅ 127.0.0.1   ║
║  Tailscale exposure           N/A             ✅ NOT exposed ║
║  DM blocking                  ✅ allowlist    ✅ allowlist   ║
║  Group blocking               ✅ allowlist    ✅ allowlist   ║
╠══════════════════════════════════════════════════════════════╣
║  Score: ██████████████████░░  95%                           ║
║  -5% Alex tiene perfil pero no está activo (intencionado)  ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 5. 📊 CÓMO FUNCIONA

```
╔══════════════════════════════════════════════════════════════╗
║  ESCENARIO                      AGENTE        RESULTADO     ║
╠══════════════════════════════════════════════════════════════╣
║  Monitorear grupo de trabajo    📖 OpenClaw   → GBrain      ║
║  Cliente pide métricas de ads   ⚕ Hermes     → MCP tools   ║
║  Guardar decisiones de grupo    📖 OpenClaw   → GBrain      ║
║  "hermes traduce esto" en grupo ⚕ Hermes     → responde    ║
║  Amigo dice "hermes" en grupo   ⚕ Hermes     → IGNORA      ║
║  Random te escribe DM           ⚕ Hermes     → IGNORA      ║
║  Ejecutar campaña con approval  ⚕ Hermes     → pide tu OK  ║
╠══════════════════════════════════════════════════════════════╣
║  SEGURIDAD: 5 CAPAS                                         ║
╠══════════════════════════════════════════════════════════════╣
║  1. Bridge         WHATSAPP_ALLOWED_USERS    quién pasa     ║
║  2. Gateway        dm_policy: allowlist      quién se procesa║
║  3. Contact .md    perfil por persona        qué puede hacer║
║  4. Approval flow  acciones destructivas     tu aprobación  ║
║  5. MCP filtering  tools include/exclude     qué tools usa  ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 6. ALERTAS

```diff
+ ✅ OpenClaw: 2 grupos monitoreados, ambos injection-protected
+ ✅ Hermes: bridge connected, gateway en tmux, Owner activo
+ ✅ Grupo Curso activo con mention_patterns "hermes"
+ ✅ Higgsfield: token renovado, cron cada 50min
+ ✅ Seguridad: 95% — todos los permisos correctos
```

```
! ⚠️ 27 grupos detectados sin monitorear
! ⚠️ Alex tiene perfil .md pero no está en allow_from (por diseño)
! ⚠️ RAM al 57% — monitorear si sube
```

---

## 7. ¿Qué quieres hacer?

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  📖 OpenClaw (lector de grupos)                              ║
║  ├─ "agrega un grupo"           → /whatsapp add             ║
║  ├─ "quita un grupo"            → /whatsapp remove           ║
║  └─ "muestra los grupos"        → /whatsapp groups           ║
║                                                              ║
║  ⚕ Hermes (ejecutor por contacto)                           ║
║  ├─ "autoriza a un contacto"    → /whatsapp hermes allow     ║
║  ├─ "bloquea un contacto"       → /whatsapp hermes block     ║
║  ├─ "muestra contactos"         → /whatsapp hermes list      ║
║  ├─ "perfil de contacto"        → /whatsapp hermes profile   ║
║  └─ "activa hermes en un grupo" → te guío paso a paso        ║
║                                                              ║
║  🔐 "auditoría de seguridad"    → /whatsapp security         ║
║                                                              ║
║  O dilo en español natural:                                  ║
║  "agrega el grupo FriendsGroup a hermes"                              ║
║  "autoriza a Alex para Meta Ads"                            ║
║  "haz una auditoría de seguridad"                            ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 8. ARCHIVOS CLAVE

```
╔══════════════════════════════════════════════════════════════╗
║  ARCHIVO                            PROPÓSITO               ║
╠══════════════════════════════════════════════════════════════╣
║  ~/.openclaw/openclaw.json          Config OpenClaw WA       ║
║  ~/.hermes/config.yaml              Config Hermes WA         ║
║  ~/.hermes/.env                     Env vars (tokens, mode)  ║
║  ~/.hermes/whatsapp/session/        Baileys session (700)    ║
║  ~/.hermes/whatsapp/contacts/*.md   Perfiles de contacto     ║
║  ~/whatsapp-status.md               Este dashboard           ║
║  bridge.js (parcheado)              Bridge WhatsApp           ║
╚══════════════════════════════════════════════════════════════╝
```

---

*Scanned 2026-05-09 07:51 UTC · /whatsapp v4.0 · Dual-Agent Dashboard*
