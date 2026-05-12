#!/bin/bash
# promote-contact.sh — Change role of an existing contact.
#
# Usage:
#   promote-contact.sh +<PHONE> <NEW_ROLE>
#
# Example:
#   promote-contact.sh +526642916010 image-only   # Nati: silent → image-only
#
# What it does:
#   1. Backs up current .md
#   2. Renders new role template (preserves Name/Phone/LIDs)
#   3. If new role is admin-delegate, adds to ADMIN_SLASH_USERS env
#   4. Restarts Hermes
#   5. Verifies security audit

set -eu

PHONE_PLUS="${1:?Usage: promote-contact.sh +<PHONE> <NEW_ROLE>}"
NEW_ROLE="${2:?Missing NEW_ROLE — one of: monitor-silent, image-only, image-and-video, chat-only, admin-delegate}"

HOME_DIR="${HOME}"
PROFILE_PATH="$HOME_DIR/.hermes/whatsapp/contacts/$PHONE_PLUS.md"
TEMPLATE="$HOME_DIR/.hermes/whatsapp/roles/$NEW_ROLE.md"
ENV_FILE="$HOME_DIR/.hermes/.env"

# Validate
case "$NEW_ROLE" in
  monitor-silent|image-only|image-and-video|admin-delegate|chat-only) ;;
  *) echo "ERROR: unknown role '$NEW_ROLE'" >&2; exit 1 ;;
esac

[ -f "$PROFILE_PATH" ] || { echo "ERROR: contact profile not found: $PROFILE_PATH" >&2; exit 1; }
[ -f "$TEMPLATE" ] || { echo "ERROR: template missing: $TEMPLATE" >&2; exit 1; }

# Extract metadata from existing profile
NAME=$(head -1 "$PROFILE_PATH" | sed 's/^# //' | cut -d'—' -f1 | xargs)
PHONE=$(echo "$PHONE_PLUS" | tr -d '+')

echo "── Promote contact ──"
echo "  Profile: $PROFILE_PATH"
echo "  Name:    $NAME"
echo "  Phone:   +$PHONE"
echo "  New role: $NEW_ROLE"
echo ""

read -p "Proceed? [y/N] " ans
[ "$ans" = "y" ] || [ "$ans" = "Y" ] || { echo "Aborted."; exit 0; }

# Backup
BAK="$PROFILE_PATH.bak-promote-$(date -u +%Y%m%dT%H%M%S)"
cp "$PROFILE_PATH" "$BAK"
echo "✅ Backup: $BAK"

# Preserve city (from line with "Número:" in old profile, anything after parentheses)
OLD_CITY_LINE=$(grep -E "^- Número:.*\(" "$PROFILE_PATH" || true)
OLD_CITY=""
if [ -n "$OLD_CITY_LINE" ]; then
  OLD_CITY=$(echo "$OLD_CITY_LINE" | sed -E 's/.*(\([^)]+\)).*/ \1/')
fi

# Preserve custom notes (anything in "## Notas internas" block beyond first 3 lines)
CUSTOM_NOTES=$(awk '/^## Notas internas/{flag=1; next} /^## /{flag=0} flag' "$PROFILE_PATH" | tail -n +4 || true)
[ -n "$CUSTOM_NOTES" ] && CUSTOM_NOTES="
$CUSTOM_NOTES" || CUSTOM_NOTES=""

# Auto-detect LIDs again (in case they weren't preserved)
SESSION_DIR="$HOME_DIR/.hermes/whatsapp/session"
DETECTED=$(for f in "$SESSION_DIR"/lid-mapping-*_reverse.json; do
  [ -f "$f" ] || continue
  if grep -q "\"$PHONE\"\|\"${PHONE#52}\"\|\"52${PHONE#52}\"" "$f" 2>/dev/null; then
    basename "$f" | sed 's/^lid-mapping-//; s/_reverse\.json$//'
  fi
done | head -2)
LID1=$(echo "$DETECTED" | sed -n '1p')
LID2=$(echo "$DETECTED" | sed -n '2p')

# Render new template
DATE=$(date -u +%Y-%m-%d)
PHONE_DISPLAY=$(echo "+$PHONE" | sed -E 's/^\+([0-9])([0-9]{2,3})([0-9]{3})([0-9]{4})$/+\1 \2 \3 \4/')
SLUG=$(echo "$NAME" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9' | head -c 20)

# Render template with preserved customizations
python3 - <<PY
import re
template = open("$TEMPLATE").read()
template = template.replace("{{NAME}}", "$NAME")
template = template.replace("{{PHONE_DISPLAY}}", "$PHONE_DISPLAY")
template = template.replace("{{CITY_SUFFIX}}", """$OLD_CITY""")
template = template.replace("{{DATE}}", "$DATE (promoted)")
template = template.replace("{{SLUG}}", "$SLUG")
template = template.replace("{{PHONE}}", "$PHONE")
template = template.replace("{{PN_NO_PLUS}}", "$PHONE")
template = template.replace("{{LID_PRIMARY}}", "$LID1")
template = template.replace("{{CUSTOM_NOTES}}", """$CUSTOM_NOTES""")
with open("$PROFILE_PATH", "w") as f:
    f.write(template)
PY

echo "✅ Profile updated with role '$NEW_ROLE'"

# If admin-delegate, add to ADMIN_SLASH_USERS
if [ "$NEW_ROLE" = "admin-delegate" ]; then
  NEW_ENTRIES="$PHONE"
  [ -n "$LID1" ] && NEW_ENTRIES="$NEW_ENTRIES,$LID1"
  [ -n "$LID2" ] && NEW_ENTRIES="$NEW_ENTRIES,$LID2"

  if grep -q "^ADMIN_SLASH_USERS=" "$ENV_FILE"; then
    CUR=$(grep "^ADMIN_SLASH_USERS=" "$ENV_FILE" | cut -d= -f2)
    NEW="$CUR"
    for e in $(echo "$NEW_ENTRIES" | tr ',' ' '); do
      echo ",$CUR," | grep -q ",$e," || NEW="$NEW,$e"
    done
    sed -i "s|^ADMIN_SLASH_USERS=.*|ADMIN_SLASH_USERS=$NEW|" "$ENV_FILE"
  else
    echo "" >> "$ENV_FILE"
    echo "ADMIN_SLASH_USERS=5216624707325,12532764950535,$NEW_ENTRIES" >> "$ENV_FILE"
  fi
  echo "✅ ADMIN_SLASH_USERS updated"
fi

# Restart
echo ""
echo "── Restart Hermes ──"
OLD_BR=$(ps -ef | grep "node.*bridge.js" | grep -v "grep\|bash" | awk '{print $2}' | head -1)
tmux kill-session -t hermes-gw 2>/dev/null || true
sleep 2
[ -n "$OLD_BR" ] && kill -KILL "$OLD_BR" 2>/dev/null || true
sleep 4
rm -f /tmp/hermes-gw.log
tmux new-session -d -s hermes-gw "HERMES_HOME=$HOME_DIR/.hermes $HOME_DIR/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run > /tmp/hermes-gw.log 2>&1"
sleep 30

curl -s --max-time 5 http://127.0.0.1:3000/health
echo ""

python3 "$HOME_DIR/whatsapp-monitor/bin/security-audit.py" 2>&1 | tail -3
echo ""
echo "✅ Contact $NAME promoted to role '$NEW_ROLE'."
