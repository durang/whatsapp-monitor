#!/usr/bin/env bash
# sync-templates.sh — Idempotent sync of role templates from canonical source to deployed location.
#
# Canonical:  ~/whatsapp-monitor/templates/roles/*.md   (git-tracked, won't be lost)
# Deployed:   ~/.hermes/whatsapp/roles/*.md             (used at runtime by add/promote scripts)
#
# Run automatically by add-contact.sh / promote-contact.sh before reading any template.
# Safe to run manually anytime — only updates if source is newer.
#
# Exit 0 = success.  Output lines starting with "+ " = files copied.

set -euo pipefail

SOURCE="$HOME/whatsapp-monitor/templates/roles"
TARGET="$HOME/.hermes/whatsapp/roles"

[ -d "$SOURCE" ] || { echo "ERROR: source missing: $SOURCE" >&2; exit 1; }
mkdir -p "$TARGET"

CHANGED=0
for f in "$SOURCE"/*.md; do
  [ -f "$f" ] || continue
  name=$(basename "$f")
  dest="$TARGET/$name"
  if [ ! -f "$dest" ] || ! cmp -s "$f" "$dest"; then
    cp -p "$f" "$dest"
    chmod 600 "$dest"
    echo "+ $name"
    CHANGED=$((CHANGED+1))
  fi
done

if [ "$CHANGED" -eq 0 ]; then
  echo "✓ templates al día ($SOURCE → $TARGET)"
else
  echo "✓ $CHANGED templates sincronizados"
fi
