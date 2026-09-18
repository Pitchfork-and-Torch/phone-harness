# Mac bootstrap

Only the operator can pair the phone and click macOS permission toggles.
The agent installs code, then waits.

## Requirements

- macOS Sequoia (15) or later
- iPhone 12 on iOS 18 or later
- Same Apple ID (2FA) on Mac and phone
- Bluetooth + Wi-Fi, devices in range
- Python 3.12+ (3.13 is fine)

## Install from this repo

```bash
# checkout already cloned
cd /path/to/phone-harness
chmod +x scripts/bootstrap-mac.sh phone-harness
./scripts/bootstrap-mac.sh
```

What the script does:

1. `python3 -m pip install` the pyobjc frameworks listed in `pyproject.toml`
2. `python3 -m pip install -e . --no-deps` so `phone-harness` is on PATH
3. `phone-harness --doctor`

Canonical home on a Mac can stay this git checkout. Upstream docs mention
`~/.phone-harness`; either is fine if `pip install -e .` points at it.

## Permissions (operator)

Open the panes:

```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
open "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"
```

1. Accessibility: enable the terminal app (Terminal, iTerm, or the Grok
   Build host). Takes effect immediately.
2. Screen Recording: enable the same app, then **quit and reopen** it.
   Capture stays blank until that restart.
3. A clean Mac may prompt for more the first time a tap or capture runs.
   Approve those. `--doctor` only knows the two panes above.

## Pair iPhone Mirroring (operator)

1. Open **iPhone Mirroring** on the Mac once.
2. Approve the pair on the iPhone 12.
3. If the window says **iPhone in Use**, lock the phone. Leave it locked
   while the agent works.
4. Do not unlock the phone mid-task. That pauses the session.

The harness never taps Connect. After you confirm it is connected, the
agent retries `connection_state()` once.

## Register the skill on the Mac (optional)

```bash
mkdir -p ~/.grok/skills/phone-harness
# Prefer the Grok body (Windows-aware). On a Mac-only agent, SKILL.md is fine.
cp skill/SKILL.md ~/.grok/skills/phone-harness/SKILL.md
# Claude Code / Codex copies if those agents run on the Mac:
mkdir -p ~/.claude/skills/phone-harness
cp SKILL.md ~/.claude/skills/phone-harness/SKILL.md
```

## Verify

```bash
phone-harness --doctor
phone-harness <<'PY'
print(connection_state())
print(screen_info())
print(window_matches_iphone12())
PY
```

If `connection_state()` is not `ready`, stop. Do not smoke-test.

Safe smoke (only after the operator says yes): `home()`, then
`tap_icon("Weather")` or `open_app("Notes")`, `ocr()` a few strings,
`home()` again.
