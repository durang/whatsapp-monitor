#!/usr/bin/env python3
"""
sync-wa-groups-to-gbrain.py — Flush WhatsApp group capture → GBrain.

The Hermes bridge tee (local patch 2026-05-28 in bridge.js) appends every
message from a capture-allowlisted group to:
    ~/.hermes/whatsapp/capture/<slug>__<YYYY-MM-DD>.jsonl

This script rebuilds one GBrain page per group/day from that JSONL.
Idempotent: re-running overwrites the page from the full daily file, so it is
safe to run on a cron (mirrors bin/sync-dms-to-gbrain.py).

Canonical capture path: ONE WhatsApp link (Hermes bridge) feeds GBrain.
OpenClaw must NOT hold a second WhatsApp session (error 440 conflict).
"""
import json
import os
import glob
import subprocess

CAPTURE_DIR = os.path.expanduser("~/.hermes/whatsapp/capture")
GBRAIN = os.path.expanduser("~/.bun/bin/gbrain")


def build_page(slug: str, day: str, msgs: list) -> str:
    fm = (
        "---\n"
        f"title: WhatsApp {slug} — {day}\n"
        "type: whatsapp\n"
        f"tags: [whatsapp, {slug}, capture]\n"
        f"date: {day}\n"
        "---\n\n"
    )
    head = (
        f"# WhatsApp {slug} — {day}\n\n"
        f"_{len(msgs)} mensajes capturados (silencioso, vía bridge de Hermes). "
        "Auto-generado por sync-wa-groups-to-gbrain.py._\n\n## Registro\n"
    )
    body = []
    for m in msgs:
        ts = (m.get("ts") or "")[11:16]
        who = m.get("sender") or "?"
        mark = "(tú) " if m.get("fromMe") else ""
        text = (m.get("text") or "").replace("\n", " ").strip()
        body.append(f"- [{ts}] {mark}{who}: {text}")
    return fm + head + "\n".join(body) + "\n"


def main():
    if not os.path.isdir(CAPTURE_DIR):
        print("no capture dir yet — nothing to sync")
        return
    files = sorted(glob.glob(os.path.join(CAPTURE_DIR, "*__*.jsonl")))
    synced = 0
    for f in files:
        base = os.path.basename(f)[:-6]  # strip .jsonl
        if "__" not in base:
            continue
        slug, day = base.rsplit("__", 1)
        msgs = []
        with open(f) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    msgs.append(json.loads(line))
                except Exception:
                    pass
        if not msgs:
            continue
        page_slug = f"whatsapp/{slug}/{day}"
        content = build_page(slug, day, msgs)
        r = subprocess.run(
            [GBRAIN, "put", page_slug],
            input=content, text=True, capture_output=True,
        )
        if r.returncode == 0:
            synced += 1
            print(f"[ok] {page_slug} ({len(msgs)} msgs)")
        else:
            print(f"[err] {page_slug}: {(r.stderr or '')[:200]}")
    print(f"synced {synced}/{len(files)} page(s)")


if __name__ == "__main__":
    main()
