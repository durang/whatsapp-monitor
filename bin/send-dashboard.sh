#!/usr/bin/env bash
# Send the WhatsApp dashboard PDF to Sergio's self-DM via the Hermes bridge.
#
# Usage: send-dashboard.sh [PDF_PATH]   (default: ~/whatsapp-dashboard.pdf)
#
# Requires: bridge running on localhost:3000 (curl -s http://127.0.0.1:3000/health → connected)
# Sends via POST /send-media with mediaType=document.

set -euo pipefail

PDF="${1:-$HOME/whatsapp-dashboard.pdf}"
BRIDGE="${BRIDGE_URL:-http://127.0.0.1:3000}"
SELF_DM="${WHATSAPP_SELF_DM:-5216624707325@s.whatsapp.net}"
NOW="$(date -u +'%Y-%m-%d %H:%M UTC')"

if [[ ! -f "$PDF" ]]; then
    echo "ERROR: PDF not found: $PDF" >&2
    exit 1
fi

# Sanity: bridge alive?
HEALTH="$(curl -s --max-time 5 "$BRIDGE/health" || true)"
if [[ "$HEALTH" != *'"connected"'* ]]; then
    echo "ERROR: bridge not connected: $HEALTH" >&2
    exit 2
fi

CAPTION="WhatsApp Dual-Agent Dashboard — $NOW"
FILENAME="whatsapp-dashboard-$(date -u +'%Y%m%d-%H%M').pdf"

# Build JSON payload (jq if available, else hand-roll)
if command -v jq >/dev/null 2>&1; then
    PAYLOAD="$(jq -n \
        --arg chatId "$SELF_DM" \
        --arg filePath "$PDF" \
        --arg mediaType "document" \
        --arg caption "$CAPTION" \
        --arg fileName "$FILENAME" \
        '{chatId:$chatId, filePath:$filePath, mediaType:$mediaType, caption:$caption, fileName:$fileName}')"
else
    PAYLOAD="{\"chatId\":\"$SELF_DM\",\"filePath\":\"$PDF\",\"mediaType\":\"document\",\"caption\":\"$CAPTION\",\"fileName\":\"$FILENAME\"}"
fi

RESP="$(curl -s --max-time 30 -X POST "$BRIDGE/send-media" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")"

if [[ "$RESP" == *'"success":true'* ]]; then
    echo "OK sent → $SELF_DM"
    echo "    file: $PDF ($(stat -c %s "$PDF") bytes)"
    echo "    msgId: $(echo "$RESP" | grep -o '"messageId":"[^"]*"' || echo '(none)')"
    exit 0
else
    echo "ERROR send-media failed:"
    echo "$RESP"
    exit 3
fi
