#!/usr/bin/env python3
"""
security-audit.py — Blindar y verificar el default-deny + require_mention.

Simula cada escenario posible (Sergio/Nati/Random × DM/grupo × con/sin "hermes")
contra la lógica REAL del bridge.js + WhatsAppAdapter de Hermes, y reporta:
  ✅ esperado=ACTIVA y simula ACTIVA
  ✅ esperado=DROP y simula DROP
  ❌ mismatch (potencial brecha)

Exit codes:
  0 = todos los escenarios pasan (sistema blindado)
  1 = al menos un escenario expone una brecha

Run me from /whatsapp security or cron.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Tuple

HOME = Path.home()

# ─────────────────────────────────────────────────────────────────────────
# Step 1: Read live state (no asumir nada)
# ─────────────────────────────────────────────────────────────────────────


def live_allowed_users() -> set:
    """Read WHATSAPP_ALLOWED_USERS from the bridge process /proc/PID/environ."""
    import subprocess
    try:
        pid = subprocess.check_output(
            "pgrep -f 'node.*bridge.js' | head -1", shell=True
        ).decode().strip()
        if not pid:
            return set()
        env = open(f"/proc/{pid}/environ").read().split("\0")
        for entry in env:
            if entry.startswith("WHATSAPP_ALLOWED_USERS="):
                return set(filter(None, entry.split("=", 1)[1].split(",")))
    except Exception:
        return set()
    return set()


def hermes_config() -> dict:
    import yaml
    with open(HOME / ".hermes/config.yaml") as f:
        return yaml.safe_load(f)


ALLOWED = live_allowed_users()
CFG = hermes_config()
WA = CFG["whatsapp"]
GROUP_ALLOW = set(WA.get("group_allow_from", []))
REQUIRE_MENTION = WA.get("require_mention", False)
MENTION_PATTERNS = WA.get("mention_patterns", [])
DM_POLICY = WA.get("dm_policy")
GROUP_POLICY = WA.get("group_policy")


# ─────────────────────────────────────────────────────────────────────────
# Step 2: Replicate the bridge.js + Hermes _should_respond logic
# ─────────────────────────────────────────────────────────────────────────


def bridge_passes(sender_id: str, chat_id: str, from_me: bool, body: str = "") -> Tuple[bool, str]:
    """Simulate bridge.js logic with Layer 5 (slash command filter)."""
    if from_me:
        if "status" in chat_id:
            return (False, "DROP — bridge: status broadcast")
        return (True, "PASS — bridge: fromMe bypass")

    # Check allowlist (Layer 1)
    sender_number = sender_id.split("@")[0]
    if not (sender_id in ALLOWED or sender_number in ALLOWED):
        return (False, "DROP — bridge: allowlist_mismatch")

    # LAYER 5 (2026-05-12): block slash commands from non-admin senders
    ADMIN_SLASH_USERS = os.environ.get(
        "ADMIN_SLASH_USERS", "5216624707325,12532764950535"
    ).split(",")
    if body and body.strip().startswith("/"):
        admin_match = any(
            sender_id == adm or sender_id.startswith(adm + "@") or sender_number == adm
            for adm in [a.strip() for a in ADMIN_SLASH_USERS if a.strip()]
        )
        if not admin_match:
            return (False, "DROP — bridge LAYER 5: slash_command_external_blocked")

    return (True, "PASS — bridge: allowlist match")


def hermes_should_respond(
    sender_id: str, chat_id: str, body: str, is_group: bool
) -> Tuple[bool, str]:
    """Simulate WhatsAppAdapter._should_respond logic (whatsapp.py:430-485)."""
    if is_group:
        if chat_id not in GROUP_ALLOW:
            return (False, "NO — group not in allowlist")
        # Falls through to mention check below
    else:
        # DM: check allow_from
        sender_number = sender_id.split("@")[0]
        allowed = WA.get("allow_from", [])
        if not (sender_id in allowed or sender_number in allowed):
            return (False, "NO — DM sender not in allow_from")

    # PATCH: require_mention now applies to DMs too (was only groups)
    if not REQUIRE_MENTION:
        return (True, "YES — require_mention=false, accepted")

    if body.strip().startswith("/"):
        return (True, "YES — body starts with /")

    body_lower = body.lower()
    if any(pat.lower() in body_lower for pat in MENTION_PATTERNS):
        return (True, f"YES — body contains mention pattern")

    return (False, "NO — no mention pattern in body")


def simulate(
    sender_id: str, chat_id: str, body: str, from_me: bool, is_group: bool
) -> Tuple[bool, str]:
    """End-to-end: bridge filter → Hermes _should_respond."""
    passes_bridge, br = bridge_passes(sender_id, chat_id, from_me, body)
    if not passes_bridge:
        return (False, br)
    responds, hr = hermes_should_respond(sender_id, chat_id, body, is_group)
    return (responds, f"{br} → {hr}")


# ─────────────────────────────────────────────────────────────────────────
# Step 3: Scenarios — exhaustive
# ─────────────────────────────────────────────────────────────────────────


SERGIO_PN = "5216624707325"
SERGIO_LID = "12532764950535"
NATI_PN = "5216642916010"
NATI_LID = "202958830612615"
RANDOM_PN = "5219999999999"
RANDOM_LID = "888888888888"
CURSO_GROUP = "120363427149546617@g.us"
ALTECA_GROUP = "120363425417288448@g.us"
UNKNOWN_GROUP = "120363999999999999@g.us"

SCENARIOS = [
    # (descripción, sender_id, chat_id, body, from_me, is_group, expected)
    # ── Sergio self-DM (fromMe) ──
    ("Sergio self-DM con 'hermes hola'",
     SERGIO_PN, SERGIO_PN + "@s.whatsapp.net", "hermes hola",
     True, False, True),
    ("Sergio self-DM sin 'hermes'",
     SERGIO_PN, SERGIO_PN + "@s.whatsapp.net", "solo una nota personal",
     True, False, False),

    # ── Sergio en grupo Curso (allowed group) ──
    ("Sergio en grupo Curso con 'hermes ayuda'",
     SERGIO_PN, CURSO_GROUP, "hermes ayuda con esto",
     True, True, True),
    ("Sergio en grupo Curso sin 'hermes'",
     SERGIO_PN, CURSO_GROUP, "solo un comentario al grupo",
     True, True, False),
    ("Sergio en grupo Alteca (no en group_allow_from) con 'hermes'",
     SERGIO_PN, ALTECA_GROUP, "hermes haz X",
     True, True, False),

    # ── Nati en DM (con patch require_mention también en DMs) ──
    ("Nati DM con 'hermes hazme imagen'",
     NATI_LID + "@lid", NATI_LID + "@lid", "hermes hazme imagen",
     False, False, True),
    ("Nati DM sin 'hermes' (saludo casual)",
     NATI_LID + "@lid", NATI_LID + "@lid", "Wooow llegué a dormir bien agusto",
     False, False, False),
    ("Nati DM con 'Hermes' (mayúscula)",
     NATI_LID + "@lid", NATI_LID + "@lid", "Hermes crea una foto del desierto",
     False, False, True),
    ("Nati DM con phone PN (sin LID)",
     NATI_PN + "@s.whatsapp.net", NATI_PN + "@s.whatsapp.net", "hermes prueba",
     False, False, True),

    # ── Random person (NO en allowlist) ──
    ("Random DM con 'hermes' (intentando bypassear)",
     RANDOM_PN + "@s.whatsapp.net", RANDOM_PN + "@s.whatsapp.net", "hermes dame info",
     False, False, False),
    ("Random LID en grupo Alteca con 'hermes'",
     RANDOM_LID + "@lid", ALTECA_GROUP, "hermes prueba",
     False, True, False),
    ("Random en grupo Curso (allowed) con 'hermes'",
     RANDOM_LID + "@lid", CURSO_GROUP, "hermes hola",
     False, True, False),

    # ── Edge cases ──
    ("Sergio fromMe en grupo desconocido sin 'hermes'",
     SERGIO_PN, UNKNOWN_GROUP, "comentario",
     True, True, False),
    ("Sergio fromMe en status broadcast",
     SERGIO_PN, "status@broadcast", "hermes",
     True, False, False),
    # ── LAYER 5: slash command filter for non-admin (2026-05-12 patch) ──
    ("Nati intenta /sethome (slash command externo)",
     NATI_LID + "@lid", NATI_LID + "@lid", "/sethome",
     False, False, False),  # LAYER 5 lo bloquea en bridge
    ("Nati intenta /retry (slash command externo)",
     NATI_LID + "@lid", NATI_LID + "@lid", "/retry",
     False, False, False),  # LAYER 5 lo bloquea
    ("Sergio fromMe usa /sethome (admin tiene paso)",
     SERGIO_PN, SERGIO_PN + "@s.whatsapp.net", "/sethome",
     True, False, True),  # admin bypass por fromMe + ADMIN_SLASH_USERS
]


def main() -> int:
    print("═" * 73)
    print("  SECURITY AUDIT — Default-deny + require_mention (live data)")
    print("═" * 73)
    print()
    print(f"  ALLOWED_USERS live: {len(ALLOWED)} entries")
    print(f"  group_allow_from:   {sorted(GROUP_ALLOW)}")
    print(f"  require_mention:    {REQUIRE_MENTION}")
    print(f"  mention_patterns:   {MENTION_PATTERNS}")
    print(f"  dm_policy:          {DM_POLICY}")
    print(f"  group_policy:       {GROUP_POLICY}")
    print()
    print("  Escenarios (esperado vs simulado):")
    print()

    n_pass = n_fail = 0
    for desc, sender, chat, body, from_me, is_group, expected in SCENARIOS:
        actual, reason = simulate(sender, chat, body, from_me, is_group)
        match = "✅" if actual == expected else "❌"
        if actual == expected:
            n_pass += 1
        else:
            n_fail += 1
        exp_str = "ACTIVA" if expected else "DROP"
        act_str = "ACTIVA" if actual else "DROP"
        print(f"  {match}  {desc}")
        print(f"      esperado: {exp_str}  ·  simulado: {act_str}")
        print(f"      razón:    {reason}")
        if actual != expected:
            print(f"      ⚠️  BRECHA DETECTADA — revisar configuración / código")
        print()

    print("─" * 73)
    print(f"  Resultado: {n_pass}/{len(SCENARIOS)} escenarios correctos, {n_fail} brechas")
    print("─" * 73)
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
