```
 __        ___         _       _
 \ \      / / |__   __ _| |_ ___/ \   _ __  _ __
  \ \ /\ / /| '_ \ / _` | __/ __| |  | '_ \| '_ \
   \ V  V / | | | | (_| | |_\__ \ |__| |_) | |_) |
    \_/\_/  |_| |_|\__,_|\__|___/\____| .__/| .__/
                                       |_|   |_|
    M O N I T O R    v2.1    ·    C O M M A N D    C E N T E R
```

> Generado: 2026-05-05 05:43 UTC · Numero: +526624707325 · Hermosillo
> Cambios: dimelo por chat y yo lo aplico

---

## ESTADO

```
    CONEXION ............. CONNECTED         HEALTHY    (in: 5m ago)
    GATEWAY .............. ACTIVE            863 MB RAM  (uptime: 30m)
    DMs .................. DESHABILITADOS    nadie puede escribir al bot
    VISTO AZUL ........... OFF               invisible, sin palomitas azules
    REACCIONES ........... OFF               no pone emojis
    MODO ................. OBSERVADOR        solo lee, jamas responde
```

```
    MONITOREANDO        1 grupo activo
    DETECTADOS          3 grupos disponibles
    GBRAIN              2 guias + 0 datos grupo (esperando mensajes)
```

---

## GRUPOS MONITOREADOS


### [ JPC ]  Grupo de Trabajo

    Tipo:     Construccion y proyectos
    Que es:   Coordinacion de equipo de obra. Decisiones de proyecto,
              presupuestos, materiales, fechas de entrega, acuerdos
              con clientes, reuniones de avance. Bilingual (es/en).
    Miembros
    clave:    Jonathan (coordinacion frecuente)

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
  ejemplo: "Jonathan confirmo presupuesto" -> correo

Forward a Telegram           msgs importantes -> tu Telegram   OFF
  ejemplo: decisiones y tareas llegan al instante

Alertas por keyword          palabras clave -> alerta          OFF
  ejemplo: "urgente", "problema", "deadline"

Filtro por personas          prioriza mensajes de alguien      OFF
  ejemplo: todo de Jonathan destacado, otros normal

Extractor de fechas          detecta deadlines y eventos        OFF
  ejemplo: "entrega el viernes" -> tabla de fechas

Detector de montos           registra cifras y presupuestos     OFF
  ejemplo: "$50,000 del material" -> seccion montos

Extractor de tareas          detecta tareas asignadas           OFF
  ejemplo: "Juan, manda el plano" -> tarea para Juan

Tagger de temas              clasifica por tema                 OFF
  ejemplo: #presupuesto #materiales #reuniones

Filtro anti-ruido            ignora stickers, "ok", "jaja"     OFF
  ejemplo: registro limpio sin basura

Reporte semanal              resumen de 7 dias cada domingo     OFF
  ejemplo: que paso, que falta, que viene

Traduccion auto              traduce en->es al guardar          OFF
  ejemplo: "see you wednesday" -> tambien en espanol

Extractor de links           lista URLs compartidos             OFF
  ejemplo: links por fecha y quien los mando

Detector de acuerdos         identifica compromisos verbales    OFF
  ejemplo: "ok le digo al cliente" -> acuerdo registrado

Historial por persona        perfil de actividad por miembro    OFF
  ejemplo: "Jonathan: 45 msgs, 3 tareas, 2 fechas"
------------------------------------------------------------------------
```


#### Oportunidades inteligentes

Basadas en tu perfil (builder tech, OpenClaw/GBrain, trading, Hermosillo):

```
AHORRO DE TIEMPO                                          IMPACTO
------------------------------------------------------------------------
Auto-respuestas programadas                               ~3h/semana
  "Si preguntan por avance, responde con el ultimo
  resumen de GBrain" (requiere modo respuesta ON)

Generador de minutas                                      ~2h/semana
  Cada reunion mencionada -> minuta auto en GBrain

Asistente de seguimiento                                  ~4h/semana
  Detecta tareas sin cerrar, te recuerda por Telegram
------------------------------------------------------------------------

OPORTUNIDADES DETECTADAS                                  POTENCIAL
------------------------------------------------------------------------
Sync bidireccional GBrain-Notion                          ALTO
  Posible con API key de Notion. Tus datos de obra
  accesibles desde cualquier app.

Calendario auto desde WhatsApp                            ALTO
  Fechas mencionadas en grupo -> Google Calendar events
  automaticamente. "reunion el viernes" -> evento.

Dashboard de productividad del equipo                     MEDIO
  Los datos ya se guardan. Falta visualizacion.
  Quien habla mas, quien asigna tareas, tiempos.
------------------------------------------------------------------------

INNOVACION 2026 (capacidades nuevas)                      ESTADO
------------------------------------------------------------------------
Transcripcion de audios                                   CONFIGURABLE
  Audios de WhatsApp -> texto via Whisper/DeepSeek.
  Se guardan como mensaje normal en GBrain.

Analisis de imagenes                                      EN ROADMAP
  Fotos de obra se analizan: avance, materiales,
  problemas visibles. Descripcion auto en el registro.

Contexto persistente por persona                          POSIBLE
  El agente recuerda historial de cada persona.
  "Jonathan siempre pregunta por presupuestos"
  -> GBrain graph con links entre personas y temas.
------------------------------------------------------------------------

IDEAS CROSS-PLATFORM (lo que Jarvis sabe de ti)           CATEGORIA
------------------------------------------------------------------------
Conexion con exchange (si agregas grupo de trading)       TRADING
  Senales del grupo -> ordenes en exchange via API.
  Requiere configuracion y autorizacion explicita.

Pipeline WhatsApp -> GBrain -> Telegram -> Correo         AUTOMATIZACION
  Mensaje llega -> se guarda -> se filtra -> se
  notifica por el canal correcto segun prioridad.

CRM ligero desde WhatsApp                                 NEGOCIO
  Contactos, acuerdos, seguimientos extraidos de
  conversaciones. Sin instalar nada nuevo.

Voice-to-action (proximo release OpenClaw)                INNOVACION
  Audio en grupo: "necesitamos 500 blocks para el
  lunes" -> tarea + presupuesto + fecha registrados.

Agente multi-grupo con memoria compartida                 INNOVACION
  Lo que se dice en un grupo informa al otro.
  Ejemplo: materiales de JPC aparecen en tu
  grupo personal como recordatorio.

Resumen ejecutivo multi-canal                             INNOVACION
  Lunes 7am: "esto paso en todos tus grupos esta
  semana" -> un solo resumen por Telegram.
------------------------------------------------------------------------
```


#### SystemPrompt del grupo

```
Eres un observador silencioso del grupo de trabajo JPC.

IDENTIDAD:
- Eres un agente de monitoreo profesional de OpenClaw
- Tu unico trabajo es escuchar, registrar y organizar
- JAMAS intervienes en la conversacion

REGLAS DE COMPORTAMIENTO:
1. NUNCA respondas en el grupo. Bajo ninguna circunstancia.
2. NUNCA envies reacciones, emojis, ni visto azul.
3. Si alguien te menciona con @, IGNORA. No respondas.
4. No modifiques el grupo (nombre, foto, miembros).

REGLAS DE REGISTRO:
5. GUARDA TODO: cada mensaje, sin excepcion.
   Comando: gbrain put whatsapp/jpc/YYYY-MM-DD
   Acumula todos los mensajes del dia en UNA sola pagina.
6. FORMATO: [HH:MM] Nombre/Numero: mensaje
7. MULTIMEDIA: [HH:MM] Nombre: [imagen/audio/video/documento recibido]
8. NO filtres nada. Cada mensaje se guarda integro.

RESUMEN DIARIO:
9. Al final de cada pagina, agrega:
   ## Resumen del dia
   - Decisiones tomadas
   - Tareas asignadas (quien, que, cuando)
   - Fechas limite y deadlines
   - Acuerdos alcanzados
   - Reuniones programadas
   - Problemas o bloqueos mencionados
   - Personas mas activas del dia

CONTEXTO:
- Tipo: construccion/proyectos
- Temas: coordinacion de obra, presupuestos, materiales, entregas
- Idiomas: espanol e ingles
- Miembros clave: Jonathan (coordinacion frecuente)

AUTO-MEJORA:
- Si detectas patrones nuevos (personas, temas recurrentes),
  actualiza la seccion CONTEXTO para futuras sesiones.
- Si un tema se repite 3+ veces en una semana, agregalo
  como tema principal.
```

---

## GRUPOS DETECTADOS

No monitoreados. Aparecieron en los logs de 2026-05-04.
Para agregar: dime "agrega el grupo X" o "/whatsapp add".

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

> Si agregas un grupo de trading, Jarvis puede activar: conexion con
> exchange, alertas de precios, registro de senales, analisis de mercado.

---

## DMs

```
    ESTADO:   DESHABILITADOS
    Nadie puede escribirle al bot por WhatsApp.
    Para habilitar: "agrega DMs de +52..."
```

---

## GBRAIN

```
SLUG                                    TIPO              FECHA        ESTADO
------------------------------------------------------------------------
guias/whatsapp-openclaw-setup           Guia viva         2026-05-05   ACTIVA
guias/whatsapp-history/2026-05-04       Historial v1.0    2026-05-04   ARCHIVADO
whatsapp/jpc/*                          Datos grupo       ---          ESPERANDO
------------------------------------------------------------------------

OPCIONES DE STORAGE                                                  ESTADO
------------------------------------------------------------------------
Almacenamiento diario por grupo         un doc por dia                 ON
Historial de versiones de guia          snapshot en cada cambio        ON
Busqueda semantica en mensajes          gbrain search "palabra"        DISPONIBLE
Export a JSON/CSV                       datos a archivo local          OFF
Backup automatico semanal               copia de toda la data          OFF
Limpieza de datos viejos (>90 dias)     borrar datos antiguos          OFF
------------------------------------------------------------------------
```

---

## CONFIGURACION COMPLETA

Todos los parametros canonicos de WhatsApp en OpenClaw:

```
PARAMETRO                       VALOR ACTUAL          OPCIONES
------------------------------------------------------------------------
enabled                         true                  true / false
dmPolicy                        disabled              disabled / allowlist / open
groupPolicy                     allowlist             allowlist / open / disabled
sendReadReceipts                false                 true / false
reactionLevel                   off                   off / auto / manual
selfChatMode                    false                 true / false
allowFrom                       [+526624707325]       lista de numeros
groups                          1 grupo               objeto con IDs
  requireMention (por grupo)    false                 true / false
  systemPrompt (por grupo)      personalizado         texto libre
------------------------------------------------------------------------
```

---

## SISTEMA

```
    UPTIME ............... 13h 59m
    RAM .................. 3.1 GB / 7.6 GB  (41%)
    LOAD ................. 0.18 / 0.16 / 1.06
    GATEWAY .............. active   PID 194095   863 MB
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
"cambia nombre de [grupo]"     renombrar grupo
"que se dijo hoy en [grupo]"   consultar mensajes en GBrain
```

---

## COMO CREAR UN AGENTE PARA UN GRUPO

```
Paso 1   Detectar
         Manda un mensaje en el grupo o espera actividad.
         Aparecera arriba en "Grupos Detectados".

Paso 2   Pedir
         Dime: "/whatsapp add" o "agrega el grupo X"
         Te pregunto nombre, reglas y config.

Paso 3   Elegir template
         1. Guardar TODO + resumen          <- default
         2. Solo lo importante
         3. Enfocado en personas
         4. Custom (tu defines las reglas)

Paso 4   Listo
         Yo configuro, reinicio, verifico y regenero
         este archivo con el grupo nuevo incluido.
```

---

## TROUBLESHOOTING

```
PROBLEMA                              SOLUCION
------------------------------------------------------------------------
WhatsApp desconectado                 openclaw channels login --channel whatsapp
No llegan mensajes                    verificar ID del grupo en la config
Gateway caido                         systemctl --user restart openclaw-gateway
Ver logs en vivo                      journalctl --user -u openclaw-gateway -f
Cambios no se aplican                 reiniciar gateway despues de editar
No se que grupos tengo                /whatsapp groups
```

---

## ARCHIVOS CLAVE

```
~/.openclaw/openclaw.json                 config principal
~/.openclaw/credentials/whatsapp/         sesion WhatsApp Web (Baileys)
/tmp/openclaw/openclaw-YYYY-MM-DD.log     logs del dia
~/whatsapp-status.md                      ESTE ARCHIVO (auto-regenerable)
gbrain: guias/whatsapp-openclaw-setup     guia viva sincronizada
gbrain: guias/whatsapp-history/*          historial de versiones
gbrain: whatsapp/GRUPO/YYYY-MM-DD        mensajes por grupo por dia
```

---

## AUTO-REGENERACION

```
Cada vez que corras /whatsapp:

  1. VERIFICAR    lee estado real (channels, config, logs)
  2. APLICAR      si pediste cambios: modifica config, reinicia
  3. REGENERAR    reescribe este archivo con datos frescos
  4. GUARDAR      sube version actualizada a GBrain
```

Para hacer cambios, dimelo por chat:
- "activa alertas por correo en JPC"
- "cambia el nombre del grupo a Proyecto Norte"
- "agrega el grupo del asador"
- "quiero un reporte semanal de JPC"
- "desactiva el registro multimedia"

Yo lo aplico, verifico que funcione, y regenero todo.
