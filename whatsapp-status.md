```
 __        ___         _       _
 \ \      / / |__   __ _| |_ ___/ \   _ __  _ __
  \ \ /\ / /| '_ \ / _` | __/ __| |  | '_ \| '_ \
   \ V  V / | | | | (_| | |_\__ \ |__| |_) | |_) |
    \_/\_/  |_| |_|\__,_|\__|___/\____| .__/| .__/
                                       |_|   |_|
    M O N I T O R    v2.5    ·    C O M M A N D    C E N T E R
```

> Generado: 2026-05-05 08:13 UTC · Numero: +526624707325 · Hermosillo
> Cambios: dimelo por chat y yo lo aplico, actualizo y subo automaticamente

---

## ESTADO

```
    CONEXION ............. CONNECTED         HEALTHY
    GATEWAY .............. ACTIVE            735 MB RAM  (uptime: 7m)
    DMs .................. ALLOWLIST         2 contactos read-only (dm-block-claw)
    VISTO AZUL ........... OFF               invisible, sin palomitas azules
    REACCIONES ........... OFF               no pone emojis
    MODO ................. OBSERVADOR        solo lee, jamas responde
```

```
    MONITOREANDO        1 grupo activo + 1 DM read-only
    DETECTADOS          3 grupos disponibles
    GBRAIN              2 guias + 0 datos grupo (esperando mensajes)
```

```
    MODELO PRIMARIO     openai/gpt-5.5-pro (Codex)
    FALLBACKS           gpt-5.5 > deepseek-v4-pro > grok-4-1-fast > deepseek-v4-flash
    CADENA              5 niveles — nunca se queda mudo
```

---

## DMs MONITOREADOS

```
PROTECCION:   dm-block-claw plugin (deterministico, sin LLM)
MODO:         TODOS los DMs son READ-ONLY — el bot jamas responde
MECANISMO:    Plugin intercepta outbound antes de enviar y cancela
VERIFICACION: openclaw plugins list | grep dm-block (debe decir "enabled")
```

### Directorio de numeros

```
#   NOMBRE               NUMERO              ULTIMOS 3   ESTADO                  FECHA
------------------------------------------------------------------------
1   Sergio (owner)       +526624707325       ..325        OWNER                  siempre
2   Cynthia Cruz         +13058495648        ..648        READ-ONLY verificado   2026-05-05
3   Jason Prescott       +17608285436        ..436        READ-ONLY              2026-05-05
------------------------------------------------------------------------
```

Para agregar: dime "agrega a [nombre] +[numero]"
Para quitar: dime "quita a [nombre]" (se marca REMOVED, no se borra)

### Permisos (identicos para TODOS los numeros)

```
                                        ESTADO
    Bot lee sus DMs ...................  SI      solo lo que le mandan a Sergio
    Bot les responde .................. NO       jamas (dm-block-claw cancela)
    Bot les envia visto ............... NO       invisible
    Bot les envia reacciones .......... NO       invisible
    Pueden controlar el bot ........... NO       cero influencia
    Saben que el bot existe ........... NO       completamente invisible
```

### Que se guarda de los DMs

```
GUARDAR (lo profesional)                         IGNORAR (lo personal)
--------------------------------------------     --------------------------
Solicitudes de trabajo / consultas               Conversaciones personales
Decisiones de proyecto                           Chismes, quejas personales
Fechas, deadlines, reuniones                     Memes, stickers
Presupuestos, pagos, montos                      Saludos sin contenido
Tareas asignadas                                 Temas de entretenimiento
Preguntas tecnicas                               Emojis sueltos
Acuerdos y compromisos
Links y documentos compartidos
```

### Contexto cruzado

```
Los DMs complementan lo del grupo JPC.
Si alguien pide algo por DM que se discutio en JPC, queda como referencia cruzada.

Preguntas utiles:
  "que me pidio Jason esta semana?"        busca en DM + JPC
  "Cynthia menciono algo de marketing?"    busca en DMs
  "resumeme los DMs del mes"               resumen cruzado completo
```

---

## GRUPOS MONITOREADOS


### [ JPC ]  Grupo de Trabajo — Proyecto de Jason

    Tipo:     Construccion y proyectos
    Que es:   Coordinacion de equipo de obra. Decisiones de proyecto,
              presupuestos, materiales, fechas de entrega, acuerdos
              con clientes, reuniones de avance. Bilingual (es/en).
    Miembros
    clave:    Jonathan (coordinacion frecuente), Jason (cliente)

    Ultimo mensaje:   "thanks jonathan, see you wendsday"
    Fecha:            2026-05-04
    Hoy:              Sin actividad aun

    GBrain:           whatsapp/jpc/YYYY-MM-DD
    Formato:          [HH:MM] Nombre: mensaje
    Acumulacion:      Todo el dia en una sola pagina


#### Permisos y modo

```
                                        ESTADO
    Leer mensajes ................... SI       lee todo sin excepcion
    Responder en grupo .............. NO       jamas envia mensajes
    Responder con @mencion .......... NO       ignora menciones
    Enviar visto azul ............... NO       invisible para todos
    Enviar reacciones ............... NO       no pone emojis
    Fijar mensajes .................. NO       sin permisos de admin
    Borrar mensajes ................. NO       sin permisos de admin
    Llamadas / videollamadas ........ NO       no participa
    Agregar/quitar miembros ......... NO       sin permisos de admin
    Silenciado (mute) ............... NO       procesa cada mensaje
    Enviar archivos ................. NO       solo recibe
    Leer info del grupo ............. SI       nombre, descripcion, foto
    Detectar quien esta en linea .... NO       no trackea presencia
    Requiere @mencion para leer ..... NO       lee todo automaticamente
```


#### Features

```
ACTIVAS                                                     ESTADO
------------------------------------------------------------------------
Guardar todo                 cada mensaje integro a GBrain     ON
Resumen diario               decisiones, tareas, fechas        ON
Registro multimedia          marca imagen/audio/video/doc       ON
Acumulacion diaria           un documento por dia               ON
------------------------------------------------------------------------

DISPONIBLES (pideme activar cualquiera)                     ESTADO
------------------------------------------------------------------------
Alerta por correo            tema critico -> email a ti        OFF
Forward a Telegram           msgs importantes -> tu Telegram   OFF
Alertas por keyword          palabras clave -> alerta          OFF
Filtro por personas          prioriza mensajes de alguien      OFF
Extractor de fechas          detecta deadlines y eventos        OFF
Detector de montos           registra cifras y presupuestos     OFF
Extractor de tareas          detecta tareas asignadas           OFF
Tagger de temas              clasifica por tema                 OFF
Filtro anti-ruido            ignora stickers, "ok", "jaja"     OFF
Reporte semanal              resumen de 7 dias cada domingo     OFF
Traduccion auto              traduce en->es al guardar          OFF
Extractor de links           lista URLs compartidos             OFF
Detector de acuerdos         identifica compromisos verbales    OFF
Historial por persona        perfil de actividad por miembro    OFF
------------------------------------------------------------------------
```


#### Oportunidades inteligentes

```
AHORRO DE TIEMPO                                          IMPACTO
------------------------------------------------------------------------
Auto-respuestas programadas                               ~3h/semana
Generador de minutas                                      ~2h/semana
Asistente de seguimiento                                  ~4h/semana
------------------------------------------------------------------------

OPORTUNIDADES DETECTADAS                                  POTENCIAL
------------------------------------------------------------------------
Sync bidireccional GBrain-Notion                          ALTO
Calendario auto desde WhatsApp                            ALTO
Dashboard de productividad del equipo                     MEDIO
------------------------------------------------------------------------

INNOVACION 2026                                           ESTADO
------------------------------------------------------------------------
Transcripcion de audios (Whisper/DeepSeek)                CONFIGURABLE
Analisis de imagenes (vision model)                       EN ROADMAP
Contexto persistente por persona (GBrain graph)           POSIBLE
------------------------------------------------------------------------

CROSS-PLATFORM                                            CATEGORIA
------------------------------------------------------------------------
Conexion con exchange (grupo de trading)                  TRADING
Pipeline WhatsApp -> GBrain -> Telegram -> Correo         AUTOMATIZACION
CRM ligero desde WhatsApp                                 NEGOCIO
Voice-to-action (proximo release OpenClaw)                INNOVACION
Agente multi-grupo con memoria compartida                 INNOVACION
Resumen ejecutivo multi-canal                             INNOVACION
------------------------------------------------------------------------
```


#### SystemPrompt del grupo

```
Eres un observador silencioso del grupo de trabajo JPC.

IDENTIDAD:
- Agente de monitoreo profesional de OpenClaw
- Solo escuchar, registrar y organizar
- JAMAS intervenir en la conversacion

COMPORTAMIENTO:
1. NUNCA respondas. Bajo ninguna circunstancia.
2. NUNCA reacciones, emojis, ni visto azul.
3. @mencion = IGNORAR.
4. No modificar el grupo.

REGISTRO:
5. GUARDAR TODO en gbrain put whatsapp/jpc/YYYY-MM-DD
6. FORMATO: [HH:MM] Nombre/Numero: mensaje
7. MULTIMEDIA: [HH:MM] Nombre: [tipo recibido]
8. Sin filtro. Todo integro.

RESUMEN DIARIO:
9. Decisiones, tareas, fechas, acuerdos, reuniones, problemas,
   personas activas.

CONTEXTO:
- Construccion/proyectos, bilingual es/en
- Miembros clave: Jonathan, Jason (cliente)

AUTO-MEJORA:
- Detectar patrones nuevos y actualizar contexto
- Tema 3+ veces/semana = tema principal
```

---

## GRUPOS DETECTADOS

```
#   GRUPO                                  ULTIMO MENSAJE               TIPO
------------------------------------------------------------------------
1   120363427149546617@g.us                "MACBOOK: https://claude..."  Personal/Tech
    (sin nombre)                            Links de Claude Code, ideas

2   120363418735974556@g.us                "Viral Videos"                Entretenimiento
    Viral Videos                            Videos virales, contenido

3   5216623573702-1575495688@g.us          "Quien renta asador????"     Social/Amigos
    (sin nombre, grupo legacy pre-2022)     Grupo social local
------------------------------------------------------------------------
```

---

## GBRAIN

```
SLUG                                    TIPO              FECHA        ESTADO
------------------------------------------------------------------------
guias/whatsapp-openclaw-setup           Guia viva         2026-05-05   ACTIVA
guias/whatsapp-history/2026-05-04       Historial v1.0    2026-05-04   ARCHIVADO
whatsapp/jpc/*                          Datos grupo JPC   ---          ESPERANDO
whatsapp/dm/jason/*                     DMs de Jason      ---          ESPERANDO
------------------------------------------------------------------------
```

---

## CONFIGURACION COMPLETA

```
PARAMETRO                       VALOR ACTUAL              OPCIONES
------------------------------------------------------------------------
enabled                         true                      true / false
dmPolicy                        allowlist                 disabled / allowlist / open
groupPolicy                     allowlist                 allowlist / open / disabled
sendReadReceipts                false                     true / false
reactionLevel                   off                       off / auto / manual
selfChatMode                    false                     true / false
allowFrom                       +526624707325 (tu)        lista de numeros
                                +17608285436 (Jason)
groups                          1 grupo (JPC)             objeto con IDs
  requireMention (JPC)          false                     true / false
  systemPrompt (JPC)            guardar todo + resumen    texto libre
------------------------------------------------------------------------

MODELO DEL AGENTE MAIN
------------------------------------------------------------------------
primary                         openai/gpt-5.5-pro        Codex OAuth
fallback 1                      openai/gpt-5.5            Codex OAuth
fallback 2                      deepseek/deepseek-v4-pro  API key directa
fallback 3                      xai/grok-4-1-fast         API key directa
fallback 4                      deepseek/deepseek-v4-flash API key directa
------------------------------------------------------------------------
```

---

## SISTEMA

```
    UPTIME ............... 16h 28m
    RAM .................. 3.3 GB / 7.6 GB  (43%)
    LOAD ................. 0.68 / 0.80 / 0.67
    GATEWAY .............. active   PID 232367   735 MB
    VERSION .............. OpenClaw v2026.4.11
    WHATSAPP PLUGIN ...... @openclaw/whatsapp v2026.5.3
    NODE ................. v24.14.0
```

---

## COMANDOS

```
/whatsapp                      este dashboard completo
/whatsapp add                  agregar grupo (guiado)
/whatsapp remove               quitar grupo
/whatsapp groups               solo tabla de grupos
/whatsapp guide                guia desde GBrain
/whatsapp dm add <num>         habilitar DMs de un numero
/whatsapp dm remove <num>      deshabilitar DMs de un numero
"activa [feature] en [grupo]"  activar feature especifica
"que me dijo Jason hoy"        consultar DMs en GBrain
"que se dijo en JPC"           consultar grupo en GBrain
```

---

## COMO CREAR UN AGENTE PARA UN GRUPO

```
Paso 1   Detectar — manda mensaje o espera actividad
Paso 2   Pedir — "/whatsapp add" o "agrega el grupo X"
Paso 3   Elegir template (guardar todo / solo importante / custom)
Paso 4   Listo — yo configuro, reinicio, verifico y regenero todo
```

---

## TROUBLESHOOTING

```
PROBLEMA                              SOLUCION
------------------------------------------------------------------------
WhatsApp desconectado                 openclaw channels login --channel whatsapp
No llegan mensajes                    verificar ID del grupo en la config
Gateway caido                         systemctl --user restart openclaw-gateway
Agente no responde                    verificar modelo (codex oauth puede expirar)
Ver logs en vivo                      journalctl --user -u openclaw-gateway -f
Cambios no se aplican                 reiniciar gateway despues de editar
```

---

## ARCHIVOS CLAVE

```
~/.openclaw/openclaw.json                 config principal
~/.openclaw/credentials/whatsapp/         sesion WhatsApp Web (Baileys)
/tmp/openclaw/openclaw-YYYY-MM-DD.log     logs del dia
~/whatsapp-status.md                      ESTE ARCHIVO (auto-regenerable)
~/whatsapp-monitor/                       repo git (github.com/durang/whatsapp-monitor)
gbrain: guias/whatsapp-openclaw-setup     guia viva sincronizada
gbrain: whatsapp/jpc/YYYY-MM-DD           mensajes grupo JPC
gbrain: whatsapp/dm/jason/YYYY-MM-DD      mensajes DM Jason
```

---

## DM PROTECTION — dm-block-claw plugin

```
PLUGIN:       dm-block-claw v1.0.0
UBICACION:    ~/dm-block-claw/index.js
ESTADO:       ENABLED (verificado)
MECANISMO:    Hook message_sending -> { cancel: true } para DMs
BLOQUEADOS:   2 mensajes cancelados desde instalacion (2026-05-05)

COMO FUNCIONA:
  1. Mensaje sale del agente hacia WhatsApp
  2. Plugin intercepta en el pipeline de dispatch (ANTES de enviar)
  3. Si destino es @g.us (grupo): PERMITE (pass-through)
  4. Si destino es @s.whatsapp.net (DM): CANCELA (return { cancel: true })
  5. Mensaje nunca llega a sendMessageWhatsApp

FAIL-OPEN WARNING:
  Si el plugin NO carga, los DMs SE RESPONDEN.
  Verificar despues de CADA restart: openclaw plugins list | grep dm-block
```

---

## AUTO-REGENERACION

```
Cada cambio que hagas por chat:

  1. APLICAR     modifico config, reinicio gateway
  2. VERIFICAR   channels status + plugin dm-block enabled
  3. REGENERAR   reescribo este archivo con datos frescos
  4. GBRAIN      subo version actualizada
  5. GIT         commit + push a github.com/durang/whatsapp-monitor

Nunca te pregunto si quieres actualizar. Lo hago automaticamente.
```
