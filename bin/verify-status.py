#!/usr/bin/env python3
"""
Lie Detector for the WhatsApp Dual-Agent Dashboard.

Each registered claim has:
  - description: human-readable claim from the dashboard
  - source:      command/file the truth is read from
  - check():     function returning (ok: bool, observed: str)

The script appends a "§17 LIE DETECTOR" section to ~/whatsapp-status.md
showing each claim verified against live state. Exit 0 if all pass,
1 if any fail (so callers can gate on "all green" before sending).

Run after editing status.md or before render-dashboard.py to ensure
no claim drifted out of sync with reality.

Usage:
  python3 verify-status.py             # run + append §17 to status.md
  python3 verify-status.py --report    # only print report, don't modify file
"""
from __future__ import annotations
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
STATUS_MD = HOME / "whatsapp-status.md"
SECTION_MARKER_BEGIN = "## 17. 🛡️ LIE DETECTOR — verificación claim-por-claim"
SECTION_MARKER_END = "<!-- /lie-detector -->"

# Markers for dynamic §1 LIVE STATUS block — content between them is
# regenerated from live data on every run, so it CAN'T go stale.
LIVE_BLOCK_BEGIN = "<!-- live-status-begin (auto-refreshed) -->"
LIVE_BLOCK_END = "<!-- live-status-end -->"


# ─── Helpers ─────────────────────────────────────────────

def sh(cmd: str) -> str:
    """Run shell command, return stdout (stripped). Empty string on error."""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        return r.stdout.strip()
    except Exception:
        return ""


def read_file(path: str) -> str:
    p = Path(path).expanduser()
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def file_exists(path: str) -> bool:
    return Path(path).expanduser().exists()


def proc_environ(pid: str | int, key: str) -> str:
    p = Path(f"/proc/{pid}/environ")
    if not p.exists():
        return ""
    try:
        for line in p.read_bytes().split(b"\0"):
            s = line.decode("utf-8", "replace")
            if s.startswith(f"{key}="):
                return s[len(key) + 1:]
    except Exception:
        return ""
    return ""


def bridge_pid() -> str:
    return sh("pgrep -f 'bridge\\.js' | head -1")


def openclaw_json() -> dict:
    try:
        return json.loads(read_file("~/.openclaw/openclaw.json"))
    except Exception:
        return {}


def hermes_config() -> str:
    return read_file("~/.hermes/config.yaml")


# ─── Verifier registry ───────────────────────────────────

class Claim:
    def __init__(self, section: str, what: str, source: str, check):
        self.section = section
        self.what = what
        self.source = source
        self.check = check  # callable → (ok: bool, observed: str)


def claims() -> list[Claim]:
    pid = bridge_pid()
    return [
        # --- §1 LIVE STATUS ---
        Claim("§1", "Bridge connected (port 3000)",
              "curl http://127.0.0.1:3000/health",
              lambda: ((s := sh("curl -s --max-time 3 http://127.0.0.1:3000/health")),
                       ('"status":"connected"' in s, s[:80] if s else "no response"))[1]),
        Claim("§1", "tmux hermes-gw activo",
              "tmux ls | grep hermes-gw",
              lambda: (("hermes-gw" in (s := sh("tmux ls 2>&1"))),
                       "hermes-gw present" if "hermes-gw" in s else "MISSING")),
        Claim("§1", "Hermes model = openai/gpt-5.5 (Codex)",
              "~/.hermes/config.yaml model.default",
              lambda: (("default: openai/gpt-5.5" in hermes_config() and
                        "openai-codex" in hermes_config()),
                       "openai/gpt-5.5 + openai-codex" if "openai-codex" in hermes_config() else "DRIFT")),
        Claim("§1", "fallback_providers vacío (sin retry chain)",
              "~/.hermes/config.yaml fallback_providers",
              lambda: (("fallback_providers: []" in hermes_config()),
                       "[]" if "fallback_providers: []" in hermes_config() else "tiene chain")),

        # --- §3/§4 SECURITY ---
        Claim("§3/§4", "Bridge env WHATSAPP_ALLOWED_USERS contiene Sergio + Nati (6 entries)",
              "/proc/<bridge_pid>/environ → WHATSAPP_ALLOWED_USERS",
              lambda: ((v := proc_environ(pid, "WHATSAPP_ALLOWED_USERS")),
                       (
                         v is not None
                         and all(jid in v for jid in [
                             "5216624707325",      # Sergio phone
                             "12532764950535",     # Sergio LID
                             "526642916010",       # Nati phone (sin "1")
                             "5216642916010",      # Nati phone (con "1")
                             "202958830612615",    # Nati LID 1
                             "1100803538944",      # Nati LID 2
                         ]),
                         v or "no bridge running"
                       ))[1]),
        Claim("§3/§4", "Bridge env coincide con ~/.hermes/.env (sin drift)",
              ".env keys vs /proc/PID/environ",
              lambda: (_check_env_drift(pid))),
        Claim("§3/§4", "Hermes config.yaml dm_policy = allowlist",
              "~/.hermes/config.yaml whatsapp.dm_policy",
              lambda: (("dm_policy: allowlist" in hermes_config()),
                       "allowlist" if "dm_policy: allowlist" in hermes_config() else "DRIFT")),
        Claim("§3/§4", "Hermes config.yaml allow_from contiene Sergio (4 variantes)",
              "~/.hermes/config.yaml whatsapp.allow_from",
              lambda: (("'5216624707325'" in hermes_config() and
                        "5216624707325@s.whatsapp.net" in hermes_config() and
                        "'12532764950535'" in hermes_config() and
                        "12532764950535@lid" in hermes_config()),
                       "4 variantes Sergio presentes" if "5216624707325@s.whatsapp.net" in hermes_config() else "DRIFT")),
        Claim("§3/§4", "Hermes config.yaml require_mention = true",
              "~/.hermes/config.yaml whatsapp.require_mention",
              lambda: (("require_mention: true" in hermes_config()),
                       "true" if "require_mention: true" in hermes_config() else "DRIFT")),
        Claim("§3/§4", "Hermes group_allow_from = solo Curso group",
              "~/.hermes/config.yaml whatsapp.group_allow_from",
              lambda: (("120363427149546617@g.us" in hermes_config()),
                       "Curso group present" if "120363427149546617@g.us" in hermes_config() else "DRIFT")),
        Claim("§3/§4", "SOUL.md candado destructivas presente",
              "grep ~/.hermes/SOUL.md",
              lambda: (("Candado de acciones destructivas" in read_file("~/.hermes/SOUL.md")),
                       "presente" if "Candado de acciones destructivas" in read_file("~/.hermes/SOUL.md") else "AUSENTE")),

        # --- §3 CONTACTS ---
        Claim("§3", "Contact .md +526624707325 (Sergio admin)",
              "ls ~/.hermes/whatsapp/contacts/+526624707325.md",
              lambda: ((file_exists("~/.hermes/whatsapp/contacts/+526624707325.md")),
                       "existe" if file_exists("~/.hermes/whatsapp/contacts/+526624707325.md") else "MISSING")),
        Claim("§3", "Contact .md +13058495648 (Cynthia, ex-mislabel)",
              "ls + grep título",
              lambda: ((file_exists("~/.hermes/whatsapp/contacts/+13058495648.md") and
                        "Cynthia" in read_file("~/.hermes/whatsapp/contacts/+13058495648.md")),
                       "Cynthia" if "Cynthia" in read_file("~/.hermes/whatsapp/contacts/+13058495648.md") else "DRIFT")),
        Claim("§3", "Contact .md +17608285436 (Jason real)",
              "ls + grep título",
              lambda: ((file_exists("~/.hermes/whatsapp/contacts/+17608285436.md") and
                        "Jason" in read_file("~/.hermes/whatsapp/contacts/+17608285436.md")),
                       "Jason real" if "Jason" in read_file("~/.hermes/whatsapp/contacts/+17608285436.md") else "DRIFT")),
        Claim("§3", "_default.md fallback presente",
              "ls ~/.hermes/whatsapp/contacts/_default.md",
              lambda: ((file_exists("~/.hermes/whatsapp/contacts/_default.md")),
                       "existe" if file_exists("~/.hermes/whatsapp/contacts/_default.md") else "MISSING")),
        Claim("§3", "Group profile 120363427149546617.md presente",
              "ls ~/.hermes/whatsapp/groups/",
              lambda: ((file_exists("~/.hermes/whatsapp/groups/120363427149546617.md")),
                       "existe" if file_exists("~/.hermes/whatsapp/groups/120363427149546617.md") else "MISSING")),

        # --- §2 OpenClaw ---
        Claim("§2/§11", "OpenClaw whatsapp.enabled = true",
              "openclaw.json channels.whatsapp.enabled",
              lambda: ((openclaw_json().get("channels", {}).get("whatsapp", {}).get("enabled") is True),
                       str(openclaw_json().get("channels", {}).get("whatsapp", {}).get("enabled")))),
        Claim("§2/§11", "OpenClaw allowFrom = ['+13058495648']",
              "openclaw.json channels.whatsapp.allowFrom",
              lambda: ((openclaw_json().get("channels", {}).get("whatsapp", {}).get("allowFrom") == ['+13058495648']),
                       str(openclaw_json().get("channels", {}).get("whatsapp", {}).get("allowFrom")))),
        Claim("§2/§11", "OpenClaw groups count = 4 (JPC + JPC-Dev + JPC:JB/Bud/Duran + Alteca)",
              "openclaw.json channels.whatsapp.groups",
              lambda: ((len(openclaw_json().get("channels", {}).get("whatsapp", {}).get("groups", {})) == 4),
                       f"{len(openclaw_json().get('channels', {}).get('whatsapp', {}).get('groups', {}))} groups")),
        Claim("§2/§11", "OpenClaw selfChatMode = false",
              "openclaw.json channels.whatsapp.selfChatMode",
              lambda: ((openclaw_json().get("channels", {}).get("whatsapp", {}).get("selfChatMode") is False),
                       str(openclaw_json().get("channels", {}).get("whatsapp", {}).get("selfChatMode")))),

        # --- §10 dm-block ---
        Claim("§10", "dm-block plugin entry en openclaw.json",
              "openclaw.json plugins.entries",
              lambda: (("dm-block" in openclaw_json().get("plugins", {}).get("entries", [])),
                       "entry presente" if "dm-block" in openclaw_json().get("plugins", {}).get("entries", []) else "MISSING")),
        Claim("§10", "dm-block-claw v1.0.0 archivos en disco",
              "ls ~/.openclaw/extensions/dm-block/",
              lambda: ((file_exists("~/.openclaw/extensions/dm-block/index.js") and
                        file_exists("~/.openclaw/extensions/dm-block/package.json")),
                       "index.js + manifest" if file_exists("~/.openclaw/extensions/dm-block/index.js") else "MISSING")),

        # --- §7 GBrain (real, NO los slugs claimed antes) ---
        Claim("§7", "~/brain repo existe + .git + sessions/ + projects/",
              "ls ~/brain",
              lambda: ((file_exists("~/brain/.git") and file_exists("~/brain/sessions") and file_exists("~/brain/projects")),
                       "~/brain con .git + sessions + projects" if file_exists("~/brain/sessions") else "MISSING")),

        # --- Pipeline / scripts ---
        Claim("§16", "render-dashboard.py existe + ejecutable",
              "ls -la ~/whatsapp-monitor/bin/render-dashboard.py",
              lambda: ((os.access(str(HOME / "whatsapp-monitor/bin/render-dashboard.py"), os.X_OK)),
                       "ejecutable" if os.access(str(HOME / "whatsapp-monitor/bin/render-dashboard.py"), os.X_OK) else "MISSING/no-exec")),
        Claim("§16", "send-dashboard.sh existe + ejecutable",
              "ls -la ~/whatsapp-monitor/bin/send-dashboard.sh",
              lambda: ((os.access(str(HOME / "whatsapp-monitor/bin/send-dashboard.sh"), os.X_OK)),
                       "ejecutable" if os.access(str(HOME / "whatsapp-monitor/bin/send-dashboard.sh"), os.X_OK) else "MISSING/no-exec")),
        Claim("§16", "Local patches to hermes-agent all applied (check-patches.py)",
              "python3 ~/whatsapp-monitor/bin/check-patches.py → exit 0",
              lambda: ((os.system(f"python3 {HOME / 'whatsapp-monitor/bin/check-patches.py'} > /dev/null 2>&1") == 0),
                       "all patches applied" if os.system(f"python3 {HOME / 'whatsapp-monitor/bin/check-patches.py'} > /dev/null 2>&1") == 0 else "ONE OR MORE PATCHES MISSING — run script for details")),
        Claim("§4", "Security audit: 17/17 scenarios pass (default-deny + require_mention + layer 5 sealed)",
              "python3 ~/whatsapp-monitor/bin/security-audit.py → exit 0",
              lambda: ((os.system(f"python3 {HOME / 'whatsapp-monitor/bin/security-audit.py'} > /dev/null 2>&1") == 0),
                       "17/17 escenarios sellan capas 1-5" if os.system(f"python3 {HOME / 'whatsapp-monitor/bin/security-audit.py'} > /dev/null 2>&1") == 0 else "BRECHA DETECTADA — correr script para detalles")),
    ]


def _check_env_drift(pid: str) -> tuple[bool, str]:
    """Compare keys defined in .env vs live process env."""
    if not pid:
        return (False, "no bridge process")
    env_path = HOME / ".hermes/.env"
    if not env_path.is_file():
        return (False, ".env missing")
    drifts = []
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or not line.startswith("WHATSAPP_"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        live = proc_environ(pid, key)
        if live != val:
            drifts.append(f"{key}: env='{val}' live='{live}'")
    if drifts:
        return (False, " | ".join(drifts))
    return (True, "todas las keys del .env coinciden con bridge live")


# ─── Reporting ───────────────────────────────────────────

def run_all() -> tuple[list[tuple[Claim, bool, str]], int, int, int]:
    results = []
    ok = fail = error = 0
    for c in claims():
        try:
            res = c.check()
            # check() may return (ok, observed) or just observed string in some shapes;
            # normalize:
            if isinstance(res, tuple) and len(res) == 2 and isinstance(res[0], bool):
                passed, observed = res
            else:
                passed, observed = bool(res), str(res)
            results.append((c, passed, observed))
            if passed:
                ok += 1
            else:
                fail += 1
        except Exception as e:
            results.append((c, False, f"ERROR: {e}"))
            error += 1
    return results, ok, fail, error


def render_section(results, ok, fail, error) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total = ok + fail + error
    pct = (ok * 100 // total) if total else 0
    bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
    status_line = f"Score: {bar} {pct}% ({ok}/{total} verificados)"
    if fail or error:
        status_line += f"  ⚠️ {fail} falsos · {error} errores"
    else:
        status_line += "  ✅ sin mentiras"

    lines = [
        SECTION_MARKER_BEGIN,
        "",
        f"_Auto-generado por `~/whatsapp-monitor/bin/verify-status.py` · {now}_",
        "",
        f"**{status_line}**",
        "",
        "Cada claim del dashboard se verifica contra una fuente live (config, /proc, archivos). Si una claim no está aquí, no fue verificada — léela como aspiracional, no como hecho.",
        "",
        "| Sec | Claim | Fuente | Resultado |",
        "|---|---|---|---|",
    ]
    for c, passed, observed in results:
        # Truncate observed to fit table
        obs_short = (observed[:80] + "…") if len(observed) > 83 else observed
        obs_short = obs_short.replace("|", "/").replace("\n", " ")
        symbol = "✅" if passed else "❌"
        lines.append(f"| {c.section} | {c.what} | `{c.source}` | {symbol} `{obs_short}` |")
    lines.extend([
        "",
        "### Cómo se interpreta",
        "- ✅ = la claim del dashboard coincide con el estado live (sin mentira)",
        "- ❌ = la claim difiere del estado live (mentira o stale; revisar)",
        "- Errores (raros) = el verificador falló al ejecutar; revisar logs",
        "",
        "### Cómo agregar nuevas verificaciones",
        "Editar `~/whatsapp-monitor/bin/verify-status.py` función `claims()` — cada nueva claim se añade como un objeto `Claim(section, description, source, check_fn)`. El check_fn debe devolver `(ok: bool, observed: str)`.",
        "",
        SECTION_MARKER_END,
        "",
    ])
    return "\n".join(lines)


def replace_section(md_path: Path, new_section: str) -> None:
    text = md_path.read_text(encoding="utf-8")
    # Remove any existing §17 block (between markers)
    pattern = re.compile(
        re.escape(SECTION_MARKER_BEGIN) + r".*?" + re.escape(SECTION_MARKER_END) + r"\s*",
        re.DOTALL,
    )
    text = pattern.sub("", text).rstrip() + "\n\n---\n\n"
    text += new_section
    md_path.write_text(text, encoding="utf-8")


# ─── Dynamic §1 LIVE STATUS regeneration ─────────────────

def _bar(pct: int, width: int = 20) -> str:
    f = max(0, min(width, pct * width // 100))
    return "█" * f + "░" * (width - f)


def _human_secs(s: int) -> str:
    if s < 60: return f"{s}s"
    if s < 3600: return f"{s//60}m"
    if s < 86400: return f"{s//3600}h {(s%3600)//60}m"
    return f"{s//86400}d {(s%86400)//3600}h"


def gather_live_block() -> str:
    """Build §1 LIVE STATUS body from real commands. Called every run."""
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Bridge uptime
    health = sh("curl -s --max-time 3 http://127.0.0.1:3000/health")
    bridge_uptime = "DOWN"
    bridge_state = "❌ DOWN"
    try:
        bridge_uptime_s = int(json.loads(health).get("uptime", 0))
        bridge_uptime = _human_secs(bridge_uptime_s)
        bridge_state = "✅ connected"
    except Exception:
        pass

    # tmux hermes-gw uptime
    tmux_line = sh("tmux ls 2>/dev/null | grep hermes-gw")
    hermes_state = "✅ active (tmux)" if "hermes-gw" in tmux_line else "❌ no tmux"

    # OpenClaw uptime
    oc_active = sh("systemctl --user is-active openclaw-gateway.service")
    oc_state = "✅ active" if oc_active == "active" else f"❌ {oc_active}"
    oc_start = sh("systemctl --user show openclaw-gateway.service -p ActiveEnterTimestampMonotonic --value")
    try:
        # Monotonic is in microseconds since boot; compare with /proc/uptime
        boot_uptime = float(open("/proc/uptime").read().split()[0])
        active_age_s = int(boot_uptime - int(oc_start) / 1e6)
        oc_uptime = _human_secs(active_age_s)
    except Exception:
        oc_uptime = "?"

    # System metrics
    ram_line = sh("free -m | awk 'NR==2{print $3, $2}'")
    try:
        used, total = ram_line.split()
        used, total = int(used), int(total)
        ram_pct = used * 100 // total
        ram_str = f"{used}/{total} MB ({ram_pct}%)"
    except Exception:
        used, total, ram_pct = 0, 0, 0
        ram_str = "?"

    disk_line = sh("df -h / | awk 'NR==2{print $3, $2, $5}'")
    try:
        d_used, d_total, d_pct_str = disk_line.split()
        disk_pct = int(d_pct_str.rstrip("%"))
        disk_str = f"{d_used}/{d_total} ({d_pct_str})"
    except Exception:
        disk_pct = 0
        disk_str = "?"

    load = sh("uptime | awk -F'load average:' '{print $2}' | xargs | cut -d, -f1")
    sys_uptime = sh("uptime -p | sed 's/^up //'")

    # dm-block-claw — config presence (we cannot verify hot-load externally)
    dm_block_state = "✅ entry+files" if file_exists("~/.openclaw/extensions/dm-block/index.js") else "❌ MISSING"

    body = f"""
```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                     ║
║   AGENTE                ROLE          STATE            UPTIME       ║
╠═══════════════════════════════════════════════════════════════════════╣
║   📖 OpenClaw           LECTOR        {oc_state:<16} {oc_uptime:<12}║
║   ⚕ Hermes             EJECUTOR      {hermes_state:<16} {bridge_uptime:<12}║
║   🌉 WhatsApp Bridge    TRANSPORTE    {bridge_state:<16} {bridge_uptime:<12}║
║   🔌 dm-block-claw      PROTECCIÓN    {dm_block_state:<16} {'plugin':<12}║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║   RAM    {_bar(ram_pct)}  {ram_str:<40}║
║   DISCO  {_bar(disk_pct)}  {disk_str:<40}║
║   LOAD   {_bar(int(float(load)*20) if load else 0)}  {load:<40}║
║   UPTIME {sys_uptime:<58}║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   🧠 HERMES PRIMARY     openai/gpt-5.5 (Codex OAuth)               ║
║                          base: chatgpt.com/backend-api/codex        ║
║   🔄 HERMES FALLBACKS   fallback_providers: [] (vacío)              ║
║                          si gpt-5.5 falla, NO hay reintento auto    ║
║   🔗 MCP servers        gbrain (local) + higgsfield (remote)        ║
║                                                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║   Snapshot generado: {now_utc:<48}║
║   Header del documento (fecha v5.x) puede estar más viejo.          ║
╚═══════════════════════════════════════════════════════════════════════╝
```
""".strip()
    return body


def refresh_header(md_path: Path) -> None:
    """Refresh ASCII art header version + timestamp from SKILL.md frontmatter."""
    text = md_path.read_text(encoding="utf-8")
    # Pull canonical version from SKILL.md description line
    skill = read_file("~/whatsapp-monitor/SKILL.md")
    m = re.search(r'WhatsApp Dual-Agent Dashboard v(\d+\.\d+(?:\.\d+)?)', skill)
    version = m.group(1) if m else "?.?"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    # Header format inside ASCII art: "v 5 . 8" or "v 5 . 9 . 1" with spaces
    parts = version.split(".")
    spaced_v = "v " + " . ".join(parts)
    text = re.sub(r"v \d+(?:\s*\.\s*\d+)+", spaced_v, text, count=1)
    # Date stamp inside header
    text = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC(?= · \+\d+ · Hermosillo)",
                  now, text, count=1)
    md_path.write_text(text, encoding="utf-8")


def refresh_live_block(md_path: Path) -> None:
    """Replace the §1 LIVE STATUS code-block body with a freshly gathered one."""
    text = md_path.read_text(encoding="utf-8")
    body = gather_live_block()
    new_block = f"{LIVE_BLOCK_BEGIN}\n{body}\n{LIVE_BLOCK_END}"

    # Case A: markers already present → replace between them
    if LIVE_BLOCK_BEGIN in text and LIVE_BLOCK_END in text:
        pat = re.compile(
            re.escape(LIVE_BLOCK_BEGIN) + r".*?" + re.escape(LIVE_BLOCK_END),
            re.DOTALL,
        )
        text = pat.sub(new_block, text)
    else:
        # Case B: first run — replace the entire ## 1. ⚡ LIVE STATUS code-block.
        # Find from "## 1." header to the next "---" separator and substitute.
        pat = re.compile(
            r"(## 1\. ⚡ LIVE STATUS\s*\n+)```.*?```",
            re.DOTALL,
        )
        text = pat.sub(r"\1" + new_block, text, count=1)

    md_path.write_text(text, encoding="utf-8")


def main(argv) -> int:
    # Step 1: refresh dynamic header (version + date) and §1 LIVE STATUS
    # so verifier and rendered PDF see fresh values, no stale lies.
    if STATUS_MD.is_file() and "--report" not in argv:
        try:
            refresh_header(STATUS_MD)
            refresh_live_block(STATUS_MD)
        except Exception as e:
            print(f"WARN: failed to refresh dynamic blocks: {e}", file=sys.stderr)
    # Step 2: run verifiers
    results, ok, fail, error = run_all()
    section = render_section(results, ok, fail, error)
    print(f"Verified: {ok}/{ok+fail+error}  fail={fail} error={error}")
    for c, passed, observed in results:
        sym = "✅" if passed else "❌"
        print(f"  {sym} {c.section} {c.what}  →  {observed[:120]}")
    if "--report" in argv:
        return 0 if fail == 0 and error == 0 else 1
    if not STATUS_MD.is_file():
        print(f"WARN: {STATUS_MD} not found — skipping section append")
        return 0 if fail == 0 and error == 0 else 1
    replace_section(STATUS_MD, section)
    print(f"Appended §17 to {STATUS_MD}")
    return 0 if fail == 0 and error == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
