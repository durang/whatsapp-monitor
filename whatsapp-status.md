# WhatsApp Dual-Agent Dashboard
> Generado: 2026-05-09 04:09 UTC
> Skill version: 3.0

---

## 📖 OpenClaw — LECTOR

| Campo | Estado |
|---|---|
| Conexión | ✅ connected |
| Número | +526624707325 |
| Modo | Read-only (observador silencioso) |
| Gateway | ✅ active |

### Configuración
| Setting | Valor | Significado |
|---|---|---|
| enabled | true | Canal activo |
| dmPolicy | allowlist | Solo números autorizados |
| groupPolicy | allowlist | Solo grupos configurados |
| sendReadReceipts | false | Sin visto azul |
| reactionLevel | off | Sin reacciones |

### Grupos Monitoreados (2)
| # | ID | Modo | Injection Protected | Prompt |
|---|---|---|---|---|
| 1 | 120363425126131671@g.us | read-only, mention=false | ✅ | 2652 chars |
| 2 | 120363406840968099@g.us | read-only, mention=false | ✅ | 2696 chars |

### DMs Permitidos (lectura)
| Número | Estado |
|---|---|
| +526624707325 | ✅ Sergio |
| +13058495648 | ✅ Jason |
| +17608285436 | ✅ |

### Grupos Detectados sin Monitorear: 27
Usa `/whatsapp add` para agregar.

---

## ⚕ Hermes — EJECUTOR

| Campo | Estado |
|---|---|
| Conexión | ✅ connected |
| Bridge | port 3000, uptime 1h |
| Gateway | ✅ active |
| Mode | bot |
| Secrets Redaction | ✅ true |
| Session Perms | ✅ 700 |
| Creds Perms | ✅ 600 |
| Config Perms | ✅ 600 |

### Configuración
| Setting | Valor | Significado |
|---|---|---|
| dm_policy | allowlist | Solo contactos autorizados |
| allow_from | [] | ⚠️ VACÍO — nadie activo |
| unauthorized_dm_behavior | ignore | Silencio total |
| group_policy | disabled | No toca grupos |

### Perfiles de Contacto (2)
| # | Nombre | Número | Rol | Perfil | allow_from |
|---|---|---|---|---|---|
| 1 | Sergio Durán | +526624707325 | Admin | ✅ | ❌ inactivo |
| 2 | Jason | +13058495648 | Consultoría | ✅ | ❌ inactivo |

### Seguridad por Contacto
| Contacto | Injection Protection | Approval Required | Prohibited Tools |
|---|---|---|---|
| Sergio | ✅ | No (admin) | Ninguno |
| Jason | ✅ | Sí | put_page, terminal |

---

## 🔐 Seguridad Global

| Check | OpenClaw | Hermes |
|---|---|---|
| Config perms (600) | ✅ | ✅ |
| Session perms (700/600) | ✅ | ✅ |
| Injection protection | ✅ 2/2 | ✅ 2/2 |
| Secrets redaction | N/A | ✅ |
| Bridge port | N/A | ✅ 127.0.0.1 |
| Tailscale exposure | N/A | ✅ NOT exposed |

**Security Score: ██████████████████░░  95%**

---

## 📊 Cuándo usar cada uno

| Escenario | Agente | Ejemplo |
|---|---|---|
| Monitorear grupo de trabajo | 📖 OpenClaw | Lee JPC, guarda en GBrain |
| Cliente pide métricas de ads | ⚕ Hermes | Karina consulta Meta Ads |
| Guardar decisiones de grupo | 📖 OpenClaw | Registra acuerdos en GBrain |
| Traducir PDF en grupo personal | ⚕ Hermes | Tú pides traducción en JCD |
| Ejecutar campaña aprobada | ⚕ Hermes | Sergio autoriza, Hermes ejecuta |

---

## Comandos

| Comando | Qué hace |
|---|---|
| `/whatsapp` | Este dashboard |
| `/whatsapp add <grupo>` | Agregar grupo a OpenClaw |
| `/whatsapp hermes allow <num>` | Autorizar contacto en Hermes |
| `/whatsapp hermes block <num>` | Bloquear contacto en Hermes |
| `/whatsapp hermes list` | Ver contactos |
| `/whatsapp hermes profile <num>` | Ver perfil de contacto |
| `/whatsapp security` | Auditoría de seguridad |

---

## Sistema

| Metrica | Valor |
|---|---|
| Uptime | 10h 50m |
| RAM | 3.0 / 7.6 GB (39%) |
| Load | 0.77 |

---

*Scanned 2026-05-09 04:09 UTC · /whatsapp v3.0 · Dual-Agent Dashboard*
