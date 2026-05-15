#!/usr/bin/env python3
"""
Hermes sessions → GBrain DM page sync
Lee ~/.hermes/state.db, encuentra mensajes de DMs monitoreados
(Cynthia, Daniel, Nati), guarda en GBrain como whatsapp/dm/<name>/YYYY-MM-DD.

Idempotente: state file (~/.hermes-capture-state) trackea último message.id procesado.
Merge: si la página GBrain ya existe, hace append de los nuevos mensajes (no overwrite).
"""
import sqlite3
import subprocess
import sys
import os
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path

DB = os.path.expanduser('~/.hermes/state.db')
STATE_FILE = os.path.expanduser('~/.hermes-capture-state')

# Contact mapping: (LID o phone) → (gbrain_name, perfil_phone)
# Daniel/Nati en Hermes desde 2026-05-12, Cynthia desde 2026-05-15.
CONTACTS = {
    '13058495648':                      ('cynthia', '+13058495648'),
    '13058495648@s.whatsapp.net':       ('cynthia', '+13058495648'),
    '526623538272':                     ('daniel', '+526623538272'),
    '526623538272@s.whatsapp.net':      ('daniel', '+526623538272'),
    '57291223093396':                   ('daniel', '+526623538272'),
    '57291223093396@lid':               ('daniel', '+526623538272'),
    '526642916010':                     ('nati', '+526642916010'),
    '5216642916010':                    ('nati', '+526642916010'),
    '526642916010@s.whatsapp.net':      ('nati', '+526642916010'),
    '5216642916010@s.whatsapp.net':     ('nati', '+526642916010'),
    '202958830612615':                  ('nati', '+526642916010'),
    '202958830612615@lid':              ('nati', '+526642916010'),
    '1100803538944':                    ('nati', '+526642916010'),
    '1100803538944@lid':                ('nati', '+526642916010'),
}


def gbrain_get(slug: str) -> str:
    """Return page body if exists, '' otherwise."""
    r = subprocess.run(['gbrain', 'get', slug], capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        return ''
    # gbrain output incluye frontmatter — devolver el body completo tal cual
    return r.stdout


def gbrain_put(slug: str, body: str) -> bool:
    r = subprocess.run(['gbrain', 'put', slug], input=body, capture_output=True, text=True, timeout=30)
    return r.returncode == 0


def main():
    if not Path(DB).exists():
        print(f"FATAL: {DB} no existe", file=sys.stderr)
        sys.exit(1)

    last_id = 0
    if Path(STATE_FILE).exists():
        try:
            last_id = int(Path(STATE_FILE).read_text().strip() or '0')
        except ValueError:
            last_id = 0

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    in_clause = ','.join(f"'{k}'" for k in CONTACTS.keys())
    query = f"""
SELECT m.id, m.session_id, s.user_id, m.role, m.content, m.timestamp
FROM messages m
JOIN sessions s ON m.session_id = s.id
WHERE s.source = 'whatsapp'
  AND s.user_id IN ({in_clause})
  AND m.role = 'user'
  AND m.id > ?
  AND m.content IS NOT NULL
  AND length(m.content) > 0
ORDER BY m.timestamp ASC
"""
    cur.execute(query, (last_id,))
    rows = cur.fetchall()

    if not rows:
        print(f"[{datetime.now().isoformat()}] No new messages (last_id={last_id})")
        return

    groups = defaultdict(list)
    max_id = last_id
    for mid, sid, uid, role, content, ts in rows:
        name, phone = CONTACTS[uid]
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        date_str = dt.strftime('%Y-%m-%d')
        time_str = dt.strftime('%H:%M:%S UTC')
        slug = f'whatsapp/dm/{name}/{date_str}'
        groups[(slug, name, phone, date_str)].append(
            f'- **{time_str}** [msg#{mid}] ({uid}): {content.strip()}'
        )
        max_id = max(max_id, mid)

    for (slug, name, phone, date), new_msgs in groups.items():
        existing = gbrain_get(slug)
        if existing and 'whatsapp/dm/' in existing:
            # Append nuevos a la sección de mensajes
            new_section = '\n'.join(new_msgs)
            if '## Mensajes' in existing:
                body = existing.replace(
                    '## Mensajes',
                    f'## Mensajes\n\n{new_section}',
                    1,
                )
            else:
                body = existing + '\n\n' + new_section
        else:
            body = f"""# {name.capitalize()} — DM capture {date}

**Contact:** {phone}  ·  **Source:** Hermes state.db (sessions/messages)
**Captured:** silent monitor-silent profile — Hermes no responde, solo registra.

## Mensajes

{chr(10).join(new_msgs)}
"""
        ok = gbrain_put(slug, body)
        status = '✅' if ok else '❌'
        print(f'{status} {slug}: +{len(new_msgs)} msg(s)')

    Path(STATE_FILE).write_text(str(max_id))
    print(f'[{datetime.now().isoformat()}] Done. last_id={max_id} · groups={len(groups)} · total={len(rows)} msgs')


if __name__ == '__main__':
    main()
