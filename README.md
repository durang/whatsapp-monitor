# WhatsApp Monitor for OpenClaw

A self-regenerating WhatsApp monitoring agent that silently observes your groups, records every message to a knowledge base, and gives you a real-time command center — all from your terminal.

Built as a skill for [OpenClaw](https://github.com/nicepkg/openclaw), the open-source AI agent gateway.

---

## What it actually does

You link your WhatsApp number. You pick which groups to monitor. The agent joins as an invisible observer — no blue ticks, no reactions, no responses. It reads everything, stores it in [GBrain](https://github.com/nicepkg/gbrain) (a personal knowledge brain), and generates daily summaries with decisions, tasks, deadlines, and agreements extracted automatically.

You control everything from a single command: `/whatsapp`.

```
 __        ___         _       _
 \ \      / / |__   __ _| |_ ___/ \   _ __  _ __
  \ \ /\ / /| '_ \ / _` | __/ __| |  | '_ \| '_ \
   \ V  V / | | | | (_| | |_\__ \ |__| |_) | |_) |
    \_/\_/  |_| |_|\__,_|\__|___/\____| .__/| .__/
                                       |_|   |_|
    M O N I T O R    v2.1    ·    C O M M A N D    C E N T E R
```

---

## Features

### Monitoring

- **Silent observation** — reads every message in selected groups without sending read receipts, reactions, or responses. Nobody knows the agent is there.
- **Per-group permissions** — each group gets its own config: read-only, can respond, muted, filtered. Full control over what the agent does in each group.
- **DM control** — enable or disable direct messages per number. Default: disabled (nobody can message the bot).
- **Multi-group** — monitor as many groups as you want, each with different rules.
- **Real-time status** — connection health, last message received, gateway uptime, memory usage.

### Storage & Intelligence

- **Full message archive** — every message stored in GBrain with format `[HH:MM] Name: message`, organized by group and date.
- **Daily summaries** — automatic end-of-day digest: decisions made, tasks assigned, deadlines mentioned, agreements reached, meetings scheduled, problems flagged.
- **Multimedia logging** — images, audio, video, and documents are registered when received.
- **Semantic search** — search across all stored messages with `gbrain search "keyword"`.
- **Version history** — every config change creates a snapshot in GBrain.

### Toggleable Features (per group)

Each group can have any combination of these features enabled:

| Feature | What it does |
|---|---|
| Save everything | Store every message to GBrain |
| Daily summary | Auto-generated digest of decisions, tasks, dates |
| Multimedia logging | Log when images/audio/video arrive |
| Email alerts | Send email when critical topics are mentioned |
| Telegram forwarding | Forward important messages to your Telegram bot |
| Keyword alerts | Trigger alerts on specific words ("urgent", "deadline") |
| People filter | Prioritize messages from specific group members |
| Date extractor | Detect and list all deadlines and events mentioned |
| Amount detector | Track budgets, prices, and financial figures |
| Task extractor | Identify assigned tasks and create a list |
| Topic tagger | Auto-classify messages by topic |
| Anti-noise filter | Skip stickers, lone emojis, "ok", "haha" |
| Weekly report | Sunday summary of the entire week |
| Auto-translation | Translate messages between languages when saving |
| Link extractor | Collect and organize all shared URLs |
| Agreement detector | Identify verbal commitments and promises |
| Per-person history | Activity profile for each group member |

### Command Center

Running `/whatsapp` generates a complete dashboard:

```
    CONEXION ............. CONNECTED         HEALTHY    (in: 5m ago)
    GATEWAY .............. ACTIVE            863 MB RAM  (uptime: 30m)
    DMs .................. DISABLED          nobody can message the bot
    READ RECEIPTS ........ OFF               invisible, no blue ticks
    REACTIONS ............ OFF               no emojis
    MODE ................. OBSERVER          reads only, never responds
```

Plus:
- Full permission matrix per group (14 permissions)
- Active and available features with real examples
- Detected-but-unmonitored groups from logs
- GBrain storage status
- Complete OpenClaw WhatsApp config reference
- System health (uptime, RAM, load, gateway PID)
- Troubleshooting guide
- Agent creation walkthrough

### Self-Regenerating

The dashboard regenerates itself every time you run `/whatsapp`:

1. **Verify** — reads live state from OpenClaw (channels, config, logs)
2. **Apply** — if you requested changes, modifies config and restarts gateway
3. **Regenerate** — rewrites the status file with fresh data
4. **Save** — uploads updated version to GBrain

Changes are made through natural language:

```
"add the trading group"
"enable email alerts on JPC"
"rename the group to Project North"
"disable multimedia logging"
"what was said today in JPC?"
```

---

## Architecture

```
WhatsApp Web (Baileys)
    │
    ▼
OpenClaw Gateway (systemd service)
    │
    ├── reads messages from monitored groups
    ├── applies per-group systemPrompt rules
    │
    ▼
GBrain (knowledge base)
    │
    ├── whatsapp/GROUP/YYYY-MM-DD  (daily message logs)
    ├── guias/whatsapp-openclaw-setup  (live config guide)
    └── guias/whatsapp-history/*  (version snapshots)
    │
    ▼
/whatsapp skill (Claude Code or OpenClaw)
    │
    ├── generates ~/whatsapp-status.md  (visual dashboard)
    ├── verifies live state on every run
    └── applies changes and regenerates
```

---

## Per-Group Permission Matrix

Each monitored group has 14 configurable permissions:

```
Read messages ................... configurable
Respond in group ................ configurable
Respond to @mentions ............ configurable
Send read receipts .............. configurable
Send reactions .................. configurable
Pin messages .................... configurable
Delete messages ................. configurable
Calls / video calls ............. configurable
Add/remove members .............. configurable
Muted (skip processing) ........ configurable
Send files ...................... configurable
Read group info ................. configurable
Track online presence ........... configurable
Require @mention to process ..... configurable
```

Default: read-only silent observer (only "Read messages" and "Read group info" enabled).

---

## SystemPrompt per Group

Each group gets its own AI behavior through a systemPrompt. Templates included:

**1. Save everything + summary** (default)
Records every message. Generates daily summary with decisions, tasks, deadlines.

**2. Only important**
Filters for decisions, tasks, dates, agreements. Ignores casual conversation.

**3. Focused on people**
Records everything from specific people. Only important stuff from others.

**4. Custom**
Write your own rules in natural language. The AI understands context.

SystemPrompts support auto-improvement: the agent detects recurring patterns (people, topics) and updates its own context section.

---

## Installation

### Requirements

- [OpenClaw](https://github.com/nicepkg/openclaw) with `@openclaw/whatsapp` plugin
- [GBrain](https://github.com/nicepkg/gbrain) for storage
- A WhatsApp number linked via QR scan

### Setup

1. Copy `SKILL.md` to your skills directory:

```bash
# For Claude Code
mkdir -p ~/.claude/skills/whatsapp
cp SKILL.md ~/.claude/skills/whatsapp/SKILL.md

# For OpenClaw
mkdir -p ~/.openclaw/skills/whatsapp
cp SKILL.md ~/.openclaw/skills/whatsapp/SKILL.md
```

2. Link WhatsApp:

```bash
openclaw channels login --channel whatsapp
# Scan the QR code with your phone
```

3. Add a group to monitor:

```bash
# From Claude Code or OpenClaw chat:
/whatsapp add
```

4. Run the dashboard:

```bash
/whatsapp
```

---

## Configuration Reference

All canonical WhatsApp parameters in OpenClaw:

| Parameter | Options | Default |
|---|---|---|
| `enabled` | true / false | true |
| `dmPolicy` | disabled / allowlist / open | disabled |
| `groupPolicy` | allowlist / open / disabled | allowlist |
| `sendReadReceipts` | true / false | false |
| `reactionLevel` | off / auto / manual | off |
| `selfChatMode` | true / false | false |
| `allowFrom` | list of phone numbers | owner only |
| `groups.{id}.requireMention` | true / false | false |
| `groups.{id}.systemPrompt` | free text | save-everything template |

---

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | The skill definition (install in Claude Code or OpenClaw) |
| `whatsapp-status.md` | Auto-generated dashboard (example output) |

---

## Available Commands

| Command | What it does |
|---|---|
| `/whatsapp` | Full dashboard — verify, regenerate, show status |
| `/whatsapp add` | Add a group to monitoring (guided) |
| `/whatsapp remove` | Remove a group from monitoring |
| `/whatsapp groups` | Quick groups table |
| `/whatsapp guide` | Show guide from GBrain |
| `/whatsapp dm add <number>` | Enable DMs from a number |
| `/whatsapp dm remove <number>` | Disable DMs from a number |

---

## License

MIT

---

Built with [OpenClaw](https://github.com/nicepkg/openclaw) and [GBrain](https://github.com/nicepkg/gbrain).
