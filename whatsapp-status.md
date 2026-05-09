```diff
- ╔═══════════════════════════════════════════════════════════════════════════════╗
- ║                                                                             ║
- ║  ██╗    ██╗██╗  ██╗ █████╗ ████████╗███████╗ █████╗ ██████╗ ██████╗        ║
- ║  ██║    ██║██║  ██║██╔══██╗╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗       ║
- ║  ██║ █╗ ██║███████║███████║   ██║   ███████╗███████║██████╔╝██████╔╝       ║
- ║  ██║███╗██║██╔══██║██╔══██║   ██║   ╚════██║██╔══██║██╔═══╝ ██╔═══╝        ║
- ║  ╚███╔███╔╝██║  ██║██║  ██║   ██║   ███████║██║  ██║██║     ██║            ║
- ║   ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝            ║
- ║                                                                             ║
- ║        D U A L - A G E N T   D A S H B O A R D   v 5 . 7                  ║
- ║        2026-05-09 23:54 UTC · +526624707325 · Hermosillo                    ║
- ║        📖 OpenClaw (lector) + ⚕ Hermes (ejecutor)                          ║
- ║                                                                             ║
- ╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 1. ⚡ LIVE STATUS

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                     ║
║   AGENTE                ROLE          STATE            UPTIME       ║
╠═══════════════════════════════════════════════════════════════════════╣
║   📖 OpenClaw           LECTOR        ✅ active         1d 6h       ║
║   ⚕ Hermes             EJECUTOR      ✅ active (tmux)  17h         ║
║   🌉 WhatsApp Bridge    TRANSPORTE    ✅ connected      17h         ║
║   🔌 dm-block-claw      PROTECCIÓN    ✅ enabled        plugin      ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║   RAM    █████████░░░░░░░░░░░  4211/7823 MB (54%)                   ║
║   DISCO  █████████████████░░░  51/60 GB (84%)                       ║
║   LOAD   █░░░░░░░░░░░░░░░░░░░  0.33 (low)                          ║
║   UPTIME 1 día, 6h 35m                                              ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   🧠 MODELO PRIMARIO    openai/gpt-5.5 (Codex OAuth)               ║
║   🔄 FALLBACKS          gpt-5.5 → deepseek-v4-pro →                ║
║                          grok-4-1-fast → deepseek-v4-flash          ║
║   🔗 CADENA             5 niveles — nunca se queda mudo             ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 2. 📖 OpenClaw — LECTOR

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                     ║
║   ROL: Observador silencioso. Lee todo, guarda en GBrain.           ║
║   NUNCA responde. NUNCA envía visto. NUNCA reacciona.               ║
║   Invisible para todos los participantes.                           ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   CONFIGURACIÓN                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   enabled           true          Canal activo                      ║
║   dmPolicy          allowlist     Solo números autorizados          ║
║   groupPolicy       allowlist     Solo grupos configurados          ║
║   sendReadReceipts  false         Sin visto azul                    ║
║   reactionLevel     off           Sin reacciones                    ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   GRUPOS MONITOREADOS (2)                                           ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║   ✅ JPC - Full Deck 🎯                                            ║
║      ID:    120363425126131671@g.us                                  ║
║      Modo:  read-only · mention: off · 🔒 injection ✅              ║
║      Slug:  📁 whatsapp/jpc/YYYY-MM-DD                              ║
║      Prompt: 2652 chars (observador grupo de trabajo)                ║
║      Tipo:  🏗️ Construcción y proyectos (bilingual es/en)            ║
║                                                                     ║
║   ✅ JPC - Dev - Duran 🎯                                          ║
║      ID:    120363406840968099@g.us                                  ║
║      Modo:  read-only · mention: off · 🔒 injection ✅              ║
║      Slug:  📁 whatsapp/jpc-dev/YYYY-MM-DD                          ║
║      Prompt: 2696 chars (observador grupo desarrollo)                ║
║      Tipo:  💻 Desarrollo técnico                                    ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   PERMISOS POR GRUPO (idénticos para todos)                         ║
╠═══════════════════════════════════════════════════════════════════════╣
║   Leer mensajes ..................... ✅ lee todo sin excepción      ║
║   Responder en grupo ................ ❌ jamás                      ║
║   Responder con @mención ............ ❌ ignora                     ║
║   Enviar visto azul ................. ❌ invisible                   ║
║   Enviar reacciones ................. ❌ invisible                   ║
║   Llamadas / videollamadas .......... ❌ no participa               ║
║   Enviar archivos ................... ❌ solo recibe                 ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   DMs PERMITIDOS (lectura — dm-block-claw impide responder)         ║
╠═══════════════════════════════════════════════════════════════════════╣
║   ✅ +13058495648                                                   ║
║   ✅ +17608285436                                                   ║
║   ❌ Sergio removido — Hermes maneja sus DMs                        ║
║                                                                     ║
║   Bot lee sus DMs ................... ✅ solo lo que le mandan      ║
║   Bot les responde .................. ❌ dm-block-claw cancela      ║
║   Saben que el bot existe ........... ❌ completamente invisible    ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   GRUPOS DETECTADOS SIN MONITOREAR: 28+                             ║
║   Usa /whatsapp add para agregar                                    ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 3. ⚕ Hermes — EJECUTOR

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                     ║
║   ROL: Responde a contactos autorizados. Ejecuta MCP tools.         ║
║   Cada contacto tiene perfil .md (reglas) + GBrain page (estado).   ║
║   En grupos, solo responde al owner cuando dice "hermes".           ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   CONFIGURACIÓN                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   dm_policy          allowlist      Solo contactos autorizados      ║
║   allow_from         [4 entries]    Sergio (phone + LID x2)         ║
║   unauthorized_dm    ignore         Silencio total                  ║
║   group_policy       allowlist      Solo grupos autorizados         ║
║   mention_patterns   hermes         Invocación en grupos            ║
║   secrets_redaction  true           Tokens ocultos en logs          ║
║   gateway            tmux           hermes-gw (17h uptime)          ║
║   bridge             connected      17h uptime                      ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   CONTACTOS                                                         ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║   👤 Sergio Durán     +526624707325    Admin (Full Access)          ║
║      📄 Perfil: +526624707325.md                                    ║
║      🔒 security ✅   🔒 injection ✅                               ║
║      🧠 GBrain scope: TODOS (admin)                                 ║
║      📡 GBrain live: contacts/sergio ✅                              ║
║      ⚠️ approval: no (admin)   ❌ prohibited: 0                     ║
║      ✅ ACTIVO en allow_from                                        ║
║                                                                     ║
║   👤 Jason            +13058495648     Consultoría & Desarrollo     ║
║      📄 Perfil: +13058495648.md                                     ║
║      🔒 security ✅   🔒 injection ✅                               ║
║      🧠 GBrain scope: whatsapp/jpc/* only                           ║
║      📡 GBrain live: contacts/jason ✅                               ║
║      ⚠️ approval: sí   ❌ prohibited: 2 tools                       ║
║      ❌ NO ACTIVO (perfil listo, no en allow_from)                   ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   GRUPOS HERMES (ejecutor)                                          ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║   ✅ Curso             120363427149546617@g.us                      ║
║      mention: "hermes" / "Hermes" / "HERMES"                        ║
║      Solo owner (Sergio) · require_mention: true                    ║
║      Otros dicen "hermes" → SILENCIO                                ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   CAPACIDADES DE HERMES                                             ║
╠═══════════════════════════════════════════════════════════════════════╣
║   Hermes responde DMs ............... ✅ solo allow_from            ║
║   Hermes ejecuta MCP tools .......... ✅ según perfil .md          ║
║   Hermes responde en grupos ......... ✅ solo con "hermes"         ║
║   Hermes genera imágenes ............ ✅ Higgsfield MCP            ║
║   Hermes lee PDFs/documentos ........ ✅ baileys media cache       ║
║   Hermes transcribe audios .......... ✅ Whisper/Groq STT         ║
║   Hermes consulta GBrain ............ ✅ mcp_gbrain_query          ║
║   Contacto no autorizado ............ ❌ silencio total            ║
║   Contacto pide algo prohibido ...... ❌ "No puedo hacer eso"      ║
║   Acción destructiva ................ ⚠️ pide aprobación owner     ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 4. 🔐 SEGURIDAD — 5 CAPAS

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                     ║
║   CAPA    QUÉ CONTROLA              CÓMO                           ║
╠═══════════════════════════════════════════════════════════════════════╣
║   1. Bridge    Quién pasa            WHATSAPP_ALLOWED_USERS         ║
║   2. Gateway   Quién se procesa      dm_policy: allowlist           ║
║   3. Perfil    Qué puede hacer       archivo .md por contacto       ║
║   4. Approval  Acciones peligrosas   Owner dice "autorizado"        ║
║   5. MCP       Qué tools usa         include/exclude por server     ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║   AUDITORÍA CRUZADA                OPENCLAW         HERMES          ║
╠═══════════════════════════════════════════════════════════════════════╣
║   Config perms (600)               ✅ 600           ✅ 600          ║
║   .env perms (600)                 N/A              ✅ 600          ║
║   Session perms (700/600)          ✅               ✅ 700/600      ║
║   Injection protection             ✅ 2/2 grupos    ✅ 2/2 contacts ║
║   GBrain scope per contact         N/A              ✅ definido     ║
║   Secrets redaction                N/A              ✅ true         ║
║   Bridge port (localhost)          N/A              ✅ 127.0.0.1    ║
║   Tailscale exposure               N/A              ✅ NOT exposed  ║
║   DM blocking                      ✅ allowlist     ✅ allowlist    ║
║   Group blocking                   ✅ allowlist     ✅ allowlist    ║
║   DM response block                ✅ dm-block-claw ✅ allow_from   ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   Score: ████████████████████  95%                                  ║
║   -5% Jason perfil listo pero no activo (por diseño)                ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 5. 📊 CÓMO FUNCIONA — ESCENARIOS

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                     ║
║   ESCENARIO                         AGENTE        RESULTADO         ║
╠═══════════════════════════════════════════════════════════════════════╣
║   Monitorear grupo de trabajo       📖 OpenClaw   → GBrain slug    ║
║   Cliente pide métricas de ads      ⚕ Hermes     → MCP Meta Ads   ║
║   Guardar decisiones de grupo       📖 OpenClaw   → GBrain auto    ║
║   "hermes traduce esto" en grupo    ⚕ Hermes     → responde       ║
║   "hermes genera imagen"            ⚕ Hermes     → Higgsfield MCP ║
║   Amigo dice "hermes" en grupo      ⚕ Hermes     → IGNORA         ║
║   Random te escribe DM              ⚕ Hermes     → IGNORA         ║
║   Ejecutar campaña con approval     ⚕ Hermes     → pide tu OK     ║
║   Alguien manda PDF en grupo        ⚕ Hermes     → puede leerlo   ║
║   Audio de voz en grupo             ⚕ Hermes     → transcribe     ║
║   DM llega a OpenClaw               📖 OpenClaw   → lee, NO resp   ║
║   Prompt injection en grupo         📖 OpenClaw   → registra       ║
║   Prompt injection a Hermes         ⚕ Hermes     → "No puedo"     ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   CROSS-PLATFORM MEMORY                                             ║
╠═══════════════════════════════════════════════════════════════════════╣
║   OpenClaw captura → GBrain guarda → Hermes lee                    ║
║   Cada contacto: .md (reglas) + GBrain page (estado vivo)           ║
║   Hermes consulta contacts/NAME antes de responder                  ║
║   GBrain dream sintetiza y limpia ruido cada noche                  ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 6. 📂 GRUPOS DETECTADOS (sin monitorear)

```
╔═══════════════════════════════════════════════════════════════════════╗
║   NOMBRE                           ID                    AGENTE     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   Alteca AI SAAS Proj             ...25417288448@g.us     —         ║
║   ANUNCIOS AUTOMASTER #02         ...93646266492@g.us     —         ║
║   Arrabaleros 8:30 - tribu        ...43798637237@g.us     —         ║
║   BODEGAS 100%                    ...42186775980@g.us     —         ║
║   Ceremonia 2 ☀️🍄                ...65326555888@g.us     —         ║
║   Comunidad smokers GDL           ...26301731770@g.us     —         ║
║   Cursos Online 16                ...03285196921@g.us     —         ║
║   JCD                             ...09433133093@g.us     —         ║
║   JCD 🇲🇽🇺🇸                       ...00982572432@g.us     —         ║
║   JPC - Noha / Duran              ...24454821294@g.us     —         ║
║   JPC: ALL DEV                    ...09620535087@g.us     —         ║
║   JPC - Sales + Marketing         ...26301646187@g.us     —         ║
║   JPC: JB / Bud / Duran           ...28749155017@g.us     —         ║
║   Jóvenes CANACO🏦                ...05450522950@g.us     —         ║
║   Locales comerciales             ...15203578639@g.us     —         ║
║   MC- Mayoreo                     ...60074611206@g.us     —         ║
║   PRIMER DIPLOMADO 2024           ...30437971242@g.us     —         ║
║   + más grupos detectados                                           ║
║                                                                     ║
║   📖 Para MONITOREAR: /whatsapp add                                 ║
║   ⚕ Para EJECUTAR: "activa hermes en un grupo"                     ║
║   📖+⚕ AMBOS: se recomienda cuando activas Hermes                  ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 7. 📁 GBRAIN — Almacenamiento Cross-Platform

```
╔═══════════════════════════════════════════════════════════════════════╗
║   SLUG                                 TIPO          ESTADO         ║
╠═══════════════════════════════════════════════════════════════════════╣
║   whatsapp/jpc/YYYY-MM-DD             Grupo JPC      ✅ ACTIVO     ║
║   whatsapp/jpc-dev/YYYY-MM-DD         Grupo JPC-Dev  ✅ ACTIVO     ║
║   contacts/sergio                      Estado vivo    ✅ CREADO     ║
║   contacts/jason                       Estado vivo    ✅ CREADO     ║
║   guias/whatsapp-openclaw-setup        Guía setup     ✅ ACTIVA    ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║   CÓMO FUNCIONA:                                                    ║
║   OpenClaw escribe → whatsapp/GROUP/YYYY-MM-DD (automático)         ║
║   Hermes lee → contacts/NAME (antes de responder)                   ║
║   Hermes escribe → contacts/NAME (después de interacción)           ║
║   GBrain dream → sintetiza y limpia ruido cada noche                ║
║                                                                     ║
║   Cada grupo nuevo genera slug automáticamente.                     ║
║   Un documento por día, acumulado.                                  ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 8. ⚡ FEATURES

```
╔═══════════════════════════════════════════════════════════════════════╗
║   ACTIVAS (OpenClaw)                                    ESTADO      ║
╠═══════════════════════════════════════════════════════════════════════╣
║   Guardar todo              cada mensaje → GBrain        ✅ ON      ║
║   Resumen diario            decisiones, tareas, fechas   ✅ ON      ║
║   Registro multimedia       marca imagen/audio/video     ✅ ON      ║
║   Acumulación diaria        un documento por día         ✅ ON      ║
║   Injection protection      anti-inyección por prompt    ✅ ON      ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   ACTIVAS (Hermes)                                      ESTADO      ║
╠═══════════════════════════════════════════════════════════════════════╣
║   Responder al owner        "hermes" + instrucción       ✅ ON      ║
║   MCP tools                 Meta Ads, Higgsfield, etc    ✅ ON      ║
║   Generación de imágenes    via Higgsfield MCP           ✅ ON      ║
║   Lectura de PDFs           descarga y analiza           ✅ ON      ║
║   Transcripción de audio    Whisper/Groq STT             ✅ ON      ║
║   Perfiles por contacto     .md con permisos únicos      ✅ ON      ║
║   Approval flow             destructivas → pide OK       ✅ ON      ║
║   GBrain live state         contacts/NAME por contacto   ✅ ON      ║
║   Cross-platform memory     consulta GBrain antes de resp ✅ ON     ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   DISPONIBLES (pídeme activar)                          ESTADO      ║
╠═══════════════════════════════════════════════════════════════════════╣
║   Alerta por correo         tema crítico → email          ⬜ OFF    ║
║   Forward a Telegram        msgs importantes → TG         ⬜ OFF    ║
║   Alertas por keyword       palabras clave → alerta       ⬜ OFF    ║
║   Filtro por personas       prioriza a alguien            ⬜ OFF    ║
║   Extractor de fechas       detecta deadlines             ⬜ OFF    ║
║   Detector de montos        cifras y presupuestos         ⬜ OFF    ║
║   Extractor de tareas       tareas asignadas              ⬜ OFF    ║
║   Tagger de temas           clasifica por tema            ⬜ OFF    ║
║   Filtro anti-ruido         ignora "ok", "jaja"           ⬜ OFF    ║
║   Reporte semanal           resumen 7 días                ⬜ OFF    ║
║   Traducción auto           en→es al guardar              ⬜ OFF    ║
║   Extractor de links        lista URLs compartidos        ⬜ OFF    ║
║   Detector de acuerdos      compromisos verbales          ⬜ OFF    ║
║   Historial por persona     actividad por miembro         ⬜ OFF    ║
║   CRM ligero WhatsApp       contactos + seguimiento       ⬜ OFF    ║
║   Voice-to-action           audio → acción directa        ⬜ OFF    ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 9. 💡 OPORTUNIDADES INTELIGENTES

```
╔═══════════════════════════════════════════════════════════════════════╗
║   AHORRO DE TIEMPO                                   IMPACTO       ║
╠═══════════════════════════════════════════════════════════════════════╣
║   Auto-respuestas programadas (Hermes)               ~3h/semana    ║
║   Generador de minutas (OpenClaw → GBrain)           ~2h/semana    ║
║   Asistente de seguimiento (Hermes DMs)              ~4h/semana    ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   OPORTUNIDADES DETECTADAS                           POTENCIAL     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   Meta Ads desde WhatsApp (Hermes MCP)               ✅ ACTIVO     ║
║   Imagen/video generation (Higgsfield)               ✅ ACTIVO     ║
║   Sync bidireccional GBrain-Notion                   ALTO          ║
║   Calendario auto desde WhatsApp                     ALTO          ║
║   Dashboard de productividad del equipo              MEDIO         ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   INNOVACIÓN                                         ESTADO        ║
╠═══════════════════════════════════════════════════════════════════════╣
║   Transcripción de audios                            ✅ ACTIVO     ║
║   Análisis de imágenes (vision)                      ✅ ACTIVO     ║
║   Per-contact AI agent via .md profiles              ✅ ACTIVO     ║
║   Cross-platform memory via GBrain                   ✅ ACTIVO     ║
║   GBrain live state per contact                      ✅ ACTIVO     ║
║   Pipeline WA → GBrain → TG → Correo                ⬜ POSIBLE    ║
║   Resumen ejecutivo multi-canal                      ⬜ POSIBLE    ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 10. 🔌 dm-block-claw — Protección de DMs

```
╔═══════════════════════════════════════════════════════════════════════╗
║   PLUGIN        dm-block-claw v1.0.0                                ║
║   ESTADO        ✅ ENABLED                                          ║
║   MECANISMO     Hook message_sending → { cancel: true }            ║
╠═══════════════════════════════════════════════════════════════════════╣
║   1. Mensaje sale del agente hacia WhatsApp                         ║
║   2. Plugin intercepta en pipeline de dispatch                      ║
║   3. Si destino es @g.us (grupo): PERMITE                          ║
║   4. Si destino es @s.whatsapp.net (DM): CANCELA                   ║
║   5. Mensaje NUNCA llega al destinatario                            ║
╠═══════════════════════════════════════════════════════════════════════╣
║   ⚠️ FAIL-OPEN: Si NO carga, DMs SE RESPONDEN                      ║
║   Verificar después de CADA restart:                                ║
║   openclaw plugins list | grep dm-block                             ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 11. ⚙️ CONFIGURACIÓN COMPLETA

```
╔═══════════════════════════════════════════════════════════════════════╗
║   OPENCLAW (lector)                                                 ║
╠═══════════════════════════════════════════════════════════════════════╣
║   enabled               true                                       ║
║   dmPolicy              allowlist       2 números                   ║
║   groupPolicy           allowlist       2 grupos                    ║
║   sendReadReceipts      false           invisible                   ║
║   reactionLevel         off             sin emojis                  ║
║   groups                2 (JPC, JPC-Dev)                            ║
║   allowFrom             +13058495648, +17608285436                  ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   HERMES (ejecutor)                                                 ║
╠═══════════════════════════════════════════════════════════════════════╣
║   dm_policy             allowlist       1 contacto activo           ║
║   allow_from            Sergio (4 formatos phone+LID)               ║
║   unauthorized_dm       ignore          silencio total              ║
║   group_policy          allowlist       1 grupo (Curso)             ║
║   mention_patterns      hermes/Hermes/HERMES                        ║
║   require_mention       true            en grupos                   ║
║   secrets_redaction     true            tokens ocultos              ║
║   gateway               tmux (hermes-gw)                            ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   MODELOS                                                           ║
╠═══════════════════════════════════════════════════════════════════════╣
║   Primary               openai/gpt-5.5 (Codex OAuth)               ║
║   Fallback 1            deepseek/deepseek-v4-pro                    ║
║   Fallback 2            xai/grok-4-1-fast                           ║
║   Fallback 3            deepseek/deepseek-v4-flash                  ║
║   Hermes MCP            GBrain, Higgsfield, Meta Ads                ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 12. ALERTAS

```diff
- ⚠️  DISCO al 84% (51/60 GB) — planear limpieza antes de 90%
```

```
! ⚠️  28+ grupos detectados sin monitorear
! ⚠️  Jason tiene perfil .md listo pero no activado (por diseño)
! ⚠️  skills-auto-update.timer DESACTIVADO (protección contra sobreescritura)
```

```diff
+ ✅ OpenClaw: 2 grupos monitoreados, ambos injection-protected
+ ✅ Hermes: bridge connected 17h, gateway en tmux
+ ✅ Sergio activo en allow_from — DMs + grupo Curso
+ ✅ Grupo Curso activo con mention_patterns "hermes"
+ ✅ Higgsfield: token renovado, cron cada 50min
+ ✅ Seguridad: 95% — permisos correctos, bridge localhost
+ ✅ GBrain live state: contacts/sergio + contacts/jason
+ ✅ Cross-platform memory: OpenClaw captura → GBrain → Hermes lee
+ ✅ dm-block-claw: enabled (OpenClaw no responde DMs)
+ ✅ 5 niveles de fallback — agente nunca se queda mudo
+ ✅ SKILL.md v5.7 protegido contra sobreescritura (chmod 444)
```

---

## 13. ¿Qué quieres hacer?

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                     ║
║   📖 OpenClaw (lector de grupos)                                    ║
║   ├─ "agrega un grupo"              → /whatsapp add                ║
║   ├─ "quita un grupo"               → /whatsapp remove             ║
║   └─ "muestra los grupos"           → /whatsapp groups             ║
║                                                                     ║
║   ⚕ Hermes (ejecutor por contacto)                                 ║
║   ├─ "autoriza a un contacto"       → /whatsapp hermes allow       ║
║   ├─ "bloquea un contacto"          → /whatsapp hermes block       ║
║   ├─ "muestra contactos"            → /whatsapp hermes list        ║
║   ├─ "perfil de contacto"           → /whatsapp hermes profile     ║
║   └─ "activa hermes en un grupo"    → te guío paso a paso          ║
║                                                                     ║
║   🔐 "auditoría de seguridad"       → /whatsapp security           ║
║                                                                     ║
║   💬 Lenguaje natural:                                              ║
║   "agrega el grupo Viral Videos"                                    ║
║   "autoriza a un contacto para Meta Ads"                            ║
║   "activa hermes en el grupo JCD"                                   ║
║   "haz una auditoría de seguridad"                                  ║
║   "qué se dijo en JPC hoy"                                         ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 14. 📋 ARCHIVOS CLAVE

```
╔═══════════════════════════════════════════════════════════════════════╗
║   ARCHIVO                              PROPÓSITO                    ║
╠═══════════════════════════════════════════════════════════════════════╣
║   ~/.openclaw/openclaw.json            Config OpenClaw WA           ║
║   ~/.openclaw/credentials/whatsapp/    Sesión WhatsApp (Baileys)    ║
║   ~/.hermes/config.yaml                Config Hermes WA             ║
║   ~/.hermes/.env                       Env vars (tokens, mode)      ║
║   ~/.hermes/whatsapp/session/          Baileys session (700)        ║
║   ~/.hermes/whatsapp/contacts/*.md     Perfiles de contacto         ║
║   ~/whatsapp-status.md                 Este dashboard               ║
║   ~/dm-block-claw/index.js             Plugin protección DMs        ║
║   bridge.js (parcheado)                Bridge WhatsApp               ║
║   /tmp/openclaw/openclaw-*.log         Logs del día                 ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   GBRAIN                                                            ║
║   whatsapp/jpc/YYYY-MM-DD             Mensajes grupo JPC           ║
║   whatsapp/jpc-dev/YYYY-MM-DD         Mensajes grupo JPC-Dev       ║
║   contacts/sergio                      Estado vivo Sergio           ║
║   contacts/jason                       Estado vivo Jason            ║
║   guias/whatsapp-openclaw-setup        Guía viva sincronizada       ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 15. 🔧 TROUBLESHOOTING

```
╔═══════════════════════════════════════════════════════════════════════╗
║   PROBLEMA                            SOLUCIÓN                      ║
╠═══════════════════════════════════════════════════════════════════════╣
║   OpenClaw WA desconectado            restart openclaw-gateway      ║
║   Hermes no responde                  check tmux hermes-gw          ║
║   Bridge disconnected                 hermes whatsapp → re-pair     ║
║   No llegan msgs a Hermes             check LID en allow_from       ║
║   Hermes ignora en grupo              check group_allow_from        ║
║   dm-block-claw no carga              openclaw plugins list         ║
║   Gateway caído                       systemctl restart             ║
║   Modelo no responde                  verificar Codex OAuth         ║
║   SKILL.md se sobreescribió           chmod 444 en openclaw/skills  ║
║   Ver logs OpenClaw                   journalctl -u openclaw-gw     ║
║   Ver logs Hermes                     tmux attach -t hermes-gw      ║
║   Ver logs bridge                     tail ~/.hermes/wa/bridge.log  ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 16. 🔄 AUTO-REGENERACIÓN

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                     ║
║   Cada cambio que hagas por chat:                                   ║
║                                                                     ║
║   1. APLICAR      modifico config, reinicio gateway                 ║
║   2. VERIFICAR    channels status + bridge health                   ║
║   3. REGENERAR    reescribo este dashboard con datos frescos        ║
║   4. GBRAIN       subo versión actualizada                          ║
║   5. GIT          commit + push a durang/whatsapp-monitor           ║
║                                                                     ║
║   Nunca te pregunto si quieres actualizar.                          ║
║   Lo hago automáticamente.                                          ║
║                                                                     ║
║   PROTECCIÓN: SKILL.md en ~/.openclaw/skills/ tiene chmod 444       ║
║   (read-only). skills-auto-update.timer está DESACTIVADO.           ║
║   Nadie puede sobreescribir la versión canónica.                    ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

*Scanned 2026-05-09 23:54 UTC · /whatsapp v5.7 · Dual-Agent Dashboard*
*📖 OpenClaw (lector) + ⚕ Hermes (ejecutor) · 2 grupos monitoreados · 1 grupo Hermes*
*2 contactos · GBrain live state · Cross-platform memory · Security: 95%*
*28+ grupos detectados · 9 features activas · 16 disponibles*
