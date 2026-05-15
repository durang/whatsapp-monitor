#!/bin/bash
# add-contact.sh — Onboard a new contact to Hermes with a preset role.
#
# Usage:
#   add-contact.sh <PHONE> <ROLE> <NAME> [LID1] [LID2]
#
# Args:
#   PHONE  — phone number in E.164 without "+" (e.g. 5216642916010)
#   ROLE   — one of: image-only, image-and-video, admin-delegate, chat-only
#   NAME   — display name (use quotes if spaces, e.g. "Nati Pérez")
#   LID1   — (optional) Linked Device ID #1 — auto-detected from session if missing
#   LID2   — (optional) Linked Device ID #2 — same
#
# What it does:
#   1. Validates role + finds LIDs via lid-mapping-*_reverse.json
#   2. Renders the role template to ~/.hermes/whatsapp/contacts/+<PHONE>.md
#   3. Adds the 4 (or 8) JIDs to .env WHATSAPP_ALLOWED_USERS + config.yaml allow_from
#   4. If role=admin-delegate, also appends to ADMIN_SLASH_USERS
#   5. Restarts Hermes (tmux canon)
#   6. Runs security-audit.py to confirm no breach

set -eu

PHONE="${1:?Usage: add-contact.sh <PHONE> [ROLE] <NAME> [LID1] [LID2]
ROLE defaults to monitor-silent (no Hermes access — Sergio promotes later).
Valid roles: monitor-silent (default), image-only, image-and-video, chat-only, admin-delegate}"

# Smart arg parsing: if $2 is a known role, use it; else $2 is name and role=monitor-silent
case "${2:-}" in
  monitor-silent|image-only|image-and-video|chat-only|admin-delegate)
    ROLE="$2"
    NAME="${3:?Missing NAME}"
    LID1="${4:-}"
    LID2="${5:-}"
    ;;
  "")
    echo "Usage: add-contact.sh <PHONE> [ROLE] <NAME> [LID1] [LID2]" >&2
    exit 1
    ;;
  *)
    # $2 is not a known role → assume it's the name, role defaults to monitor-silent
    ROLE="monitor-silent"
    NAME="$2"
    LID1="${3:-}"
    LID2="${4:-}"
    echo "── No role specified — defaulting to 'monitor-silent' (no Hermes access). ──"
    echo "   To grant access later, run: promote-contact.sh +$1 <role>"
    echo ""
    ;;
esac

HOME_DIR="${HOME}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ROLES_DIR="$REPO_DIR/templates/roles"
CONTACTS_DIR="$HOME_DIR/.hermes/whatsapp/contacts"
ENV_FILE="$HOME_DIR/.hermes/.env"
YAML_FILE="$HOME_DIR/.hermes/config.yaml"
SESSION_DIR="$HOME_DIR/.hermes/whatsapp/session"

# ── Validate role ──
case "$ROLE" in
  monitor-silent|image-only|image-and-video|admin-delegate|chat-only) ;;
  *) echo "ERROR: unknown role '$ROLE'. Valid: monitor-silent (default)|image-only|image-and-video|chat-only|admin-delegate" >&2; exit 1 ;;
esac

TEMPLATE="$ROLES_DIR/$ROLE.md"
[ -f "$TEMPLATE" ] || { echo "ERROR: template missing: $TEMPLATE" >&2; exit 1; }

# ── Validate phone ──
[[ "$PHONE" =~ ^[0-9]+$ ]] || { echo "ERROR: PHONE must be digits-only (no +). Got: $PHONE" >&2; exit 1; }
[ ${#PHONE} -ge 10 ] || { echo "ERROR: PHONE too short" >&2; exit 1; }

# ── Auto-detect LIDs if not provided ──
auto_lids() {
  local query="${1#52}"  # try Mexico phone variants
  for f in "$SESSION_DIR"/lid-mapping-*_reverse.json; do
    [ -f "$f" ] || continue
    if grep -q "\"$1\"\|\"$query\"\|\"52$query\"\|\"521$query\"" "$f" 2>/dev/null; then
      basename "$f" | sed 's/^lid-mapping-//; s/_reverse\.json$//'
    fi
  done
}

if [ -z "$LID1" ] && [ -z "$LID2" ]; then
  DETECTED=$(auto_lids "$PHONE" | head -2)
  LID1=$(echo "$DETECTED" | sed -n '1p')
  LID2=$(echo "$DETECTED" | sed -n '2p')
fi

echo "── Contact to add ──"
echo "  Name:  $NAME"
echo "  Phone: $PHONE"
echo "  Role:  $ROLE"
echo "  LID 1: ${LID1:-<none detected>}"
echo "  LID 2: ${LID2:-<none detected>}"
echo "  Template: $TEMPLATE"
echo ""

# Confirm
read -p "Proceed? [y/N] " ans
[ "$ans" = "y" ] || [ "$ans" = "Y" ] || { echo "Aborted."; exit 0; }

# ── 1. Render template ──
PROFILE_PATH="$CONTACTS_DIR/+$PHONE.md"
[ -f "$PROFILE_PATH" ] && { echo "ERROR: profile already exists: $PROFILE_PATH (use remove-contact.sh first)" >&2; exit 1; }

DATE=$(date -u +%Y-%m-%d)
PHONE_PLUS=$(echo "$PHONE" | sed 's/^/+/' | sed -E 's/^\+([0-9])([0-9]{2,3})([0-9]{3})([0-9]{4})$/+\1 \2 \3 \4/')
SLUG=$(echo "$NAME" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9' | head -c 20)

# Render template — first do {{SECURITY_BLINDADA}} (multiline replace via python),
# then string placeholders via sed.
SEC_BLOCK_PATH="$REPO_DIR/templates/security-blindada.md"
python3 -c "
import sys
with open('$TEMPLATE') as f: t = f.read()
with open('$SEC_BLOCK_PATH') as f: s = f.read()
if '{{SECURITY_BLINDADA}}' in t:
    t = t.replace('{{SECURITY_BLINDADA}}', s.strip())
else:
    # Auto-inject after first '## ' if template lacks placeholder
    lines = t.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('## '):
            lines.insert(i, '')
            lines.insert(i+1, s.strip())
            lines.insert(i+2, '')
            break
    t = '\n'.join(lines)
sys.stdout.write(t)
" > "$PROFILE_PATH.tmp"

sed -e "s|{{NAME}}|$NAME|g" \
    -e "s|{{PHONE_DISPLAY}}|$PHONE_PLUS|g" \
    -e "s|{{CITY_SUFFIX}}||g" \
    -e "s|{{DATE}}|$DATE|g" \
    -e "s|{{SLUG}}|$SLUG|g" \
    -e "s|{{PHONE}}|$PHONE|g" \
    -e "s|{{PN_NO_PLUS}}|$PHONE|g" \
    -e "s|{{LID_PRIMARY}}|$LID1|g" \
    -e "s|{{CUSTOM_NOTES}}||g" \
    "$PROFILE_PATH.tmp" > "$PROFILE_PATH"

rm "$PROFILE_PATH.tmp"

echo "✅ Profile written: $PROFILE_PATH"

# ── 2. Update .env WHATSAPP_ALLOWED_USERS ──
ENV_BAK="$ENV_FILE.bak-addcontact-$(date -u +%Y%m%dT%H%M%S)"
cp "$ENV_FILE" "$ENV_BAK"

# Build list of new entries (skip if already present)
NEW_ENTRIES="$PHONE"
[ -n "$LID1" ] && NEW_ENTRIES="$NEW_ENTRIES,$LID1"
[ -n "$LID2" ] && NEW_ENTRIES="$NEW_ENTRIES,$LID2"

CURRENT=$(grep "^WHATSAPP_ALLOWED_USERS=" "$ENV_FILE" | cut -d= -f2)
UPDATED="$CURRENT"
for entry in $(echo "$NEW_ENTRIES" | tr ',' ' '); do
  if ! echo ",$CURRENT," | grep -q ",$entry,"; then
    UPDATED="$UPDATED,$entry"
  fi
done

sed -i "s|^WHATSAPP_ALLOWED_USERS=.*|WHATSAPP_ALLOWED_USERS=$UPDATED|" "$ENV_FILE"
echo "✅ .env updated (backup: $ENV_BAK)"

# ── 2b. If admin-delegate, also append to ADMIN_SLASH_USERS ──
if [ "$ROLE" = "admin-delegate" ]; then
  if grep -q "^ADMIN_SLASH_USERS=" "$ENV_FILE"; then
    CUR_ADMIN=$(grep "^ADMIN_SLASH_USERS=" "$ENV_FILE" | cut -d= -f2)
    NEW_ADMIN="$CUR_ADMIN"
    for entry in $(echo "$NEW_ENTRIES" | tr ',' ' '); do
      if ! echo ",$CUR_ADMIN," | grep -q ",$entry,"; then
        NEW_ADMIN="$NEW_ADMIN,$entry"
      fi
    done
    sed -i "s|^ADMIN_SLASH_USERS=.*|ADMIN_SLASH_USERS=$NEW_ADMIN|" "$ENV_FILE"
  else
    echo "" >> "$ENV_FILE"
    echo "# admin-delegate role: $NAME granted slash command access" >> "$ENV_FILE"
    echo "ADMIN_SLASH_USERS=5216624707325,12532764950535,$NEW_ENTRIES" >> "$ENV_FILE"
  fi
  echo "✅ ADMIN_SLASH_USERS updated (admin-delegate role)"
fi

# ── 3. Update config.yaml allow_from ──
YAML_BAK="$YAML_FILE.bak-addcontact-$(date -u +%Y%m%dT%H%M%S)"
cp "$YAML_FILE" "$YAML_BAK"

python3 - <<PY
import yaml
with open("$YAML_FILE") as f: cfg = yaml.safe_load(f)
allow = cfg["whatsapp"]["allow_from"]
new = []
new.append("$PHONE")
new.append("$PHONE@s.whatsapp.net")
if "$LID1":
    new.append("$LID1")
    new.append("$LID1@lid")
if "$LID2":
    new.append("$LID2")
    new.append("$LID2@lid")
for e in new:
    if e and e not in allow:
        allow.append(e)
cfg["whatsapp"]["allow_from"] = allow
with open("$YAML_FILE", "w") as f:
    yaml.safe_dump(cfg, f, sort_keys=False)
print(f"  allow_from now has {len(allow)} entries")
PY
echo "✅ config.yaml updated (backup: $YAML_BAK)"

# ── 4. Restart Hermes (tmux canon) ──
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

# ── 5. Verify ──
echo ""
echo "── Verification ──"
curl -s --max-time 5 http://127.0.0.1:3000/health
echo ""
NEW_BPID=$(ps -ef | grep "node.*bridge.js" | grep -v "grep\|bash" | awk '{print $2}' | head -1)
echo "Live allowlist (bridge PID $NEW_BPID):"
tr '\0' '\n' < /proc/$NEW_BPID/environ 2>/dev/null | grep "^WHATSAPP_ALLOWED_USERS=" | sed 's/^/  /'
echo ""

# Run security audit
echo "Running security audit..."
python3 "$HOME_DIR/whatsapp-monitor/bin/security-audit.py" 2>&1 | tail -3
AUDIT_EXIT=$?

if [ $AUDIT_EXIT -eq 0 ]; then
  echo ""
  echo "✅ Contact '$NAME' onboarded successfully as role '$ROLE'."
  echo "   Profile: $PROFILE_PATH"
  echo "   Send instructions: tell $NAME to message you with 'hermes [request]'"
else
  echo ""
  echo "⚠️  Security audit reported issues — review with:"
  echo "   python3 ~/whatsapp-monitor/bin/security-audit.py"
fi
