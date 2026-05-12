#!/usr/bin/env python3
"""
check-patches.py — Verify local patches to hermes-agent are still applied.

Local patches can be lost when Hermes is updated (`git pull` in
~/.hermes/hermes-agent/). Run this script to detect missing patches.

Each patch is defined by:
  - file_path (absolute)
  - marker: a unique string only present when the patch IS applied
  - description: human-readable label

Exit codes:
  0 = all patches applied
  1 = at least one missing
  2 = file not found / cannot verify

Designed to be called from verify-status.py so the lie-detector dashboard
shows patch health alongside everything else.
"""
import os
import sys
from typing import List, Tuple

HOME = os.path.expanduser("~")


# Patches list — extend here when adding new local patches
PATCHES: List[dict] = [
    {
        "id": "send_image_kwargs",
        "description": "send_image accepts **kwargs (extends upstream PR #3571)",
        "file": f"{HOME}/.hermes/hermes-agent/gateway/platforms/whatsapp.py",
        "marker": "Local patch 2026-05-12 (pending upstream PR): upstream commit 33c89e52e",
        "fix_hint": "Re-add `**kwargs,` to send_image signature. See ~/whatsapp-monitor/SKILL.md section 'Local patches'.",
    },
    {
        "id": "require_mention_dms",
        "description": "require_mention also applies to DMs (not only groups)",
        "file": f"{HOME}/.hermes/hermes-agent/gateway/platforms/whatsapp.py",
        "marker": "Local patch 2026-05-12 (pending upstream PR): apply require_mention",
        "fix_hint": "Re-add the DM mention check block in WhatsAppAdapter._should_respond. See SKILL.md.",
    },
    {
        "id": "interim_messages_per_platform_default",
        "description": "interim_assistant_messages registered in _GLOBAL_DEFAULTS",
        "file": f"{HOME}/.hermes/hermes-agent/gateway/display_config.py",
        "marker": "Local patch 2026-05-12 (pending upstream PR): make interim_assistant_messages",
        "fix_hint": "Re-add 'interim_assistant_messages': True to _GLOBAL_DEFAULTS dict.",
    },
    {
        "id": "interim_messages_resolve",
        "description": "gateway/run.py uses resolve_display_setting for interim_assistant_messages",
        "file": f"{HOME}/.hermes/hermes-agent/gateway/run.py",
        "marker": "Local patch 2026-05-12 (pending upstream PR): use resolve_display_setting",
        "fix_hint": "Re-add resolve_display_setting call in interim_assistant_messages_enabled block.",
    },
]


def check(patch: dict) -> Tuple[str, str]:
    """Return (status, detail) where status is 'OK', 'MISSING', or 'NOFILE'."""
    path = patch["file"]
    if not os.path.exists(path):
        return ("NOFILE", f"{path} does not exist")
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if patch["marker"] in content:
            return ("OK", "marker present")
        return ("MISSING", f"marker '{patch['marker'][:60]}...' not found")
    except Exception as e:
        return ("NOFILE", f"read error: {e}")


def main() -> int:
    results = []
    max_id_len = max(len(p["id"]) for p in PATCHES)
    print(f"# Patch health check  ({len(PATCHES)} patches tracked)")
    print()
    n_ok = n_missing = n_nofile = 0
    for p in PATCHES:
        status, detail = check(p)
        if status == "OK":
            n_ok += 1
            icon = "✅"
        elif status == "MISSING":
            n_missing += 1
            icon = "❌"
        else:
            n_nofile += 1
            icon = "⚠️"
        print(f"  {icon}  {p['id'].ljust(max_id_len)}  {status:<8}  {p['description']}")
        if status != "OK":
            print(f"      file: {p['file']}")
            print(f"      detail: {detail}")
            print(f"      fix: {p['fix_hint']}")
        results.append((p["id"], status))
    print()
    print(f"# Summary: {n_ok} OK, {n_missing} MISSING, {n_nofile} NOFILE")

    if n_nofile > 0:
        return 2
    if n_missing > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
