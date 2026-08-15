# phone-harness (private)

Private ops tree for driving a real iPhone through **macOS iPhone Mirroring**.
Not a public product. Not a Windows HID stack.

Upstream core (MIT): [ShawnPana/phone-harness](https://github.com/ShawnPana/phone-harness)
at `f568cb924a19bd7008e86c6191cf3b615cff4b15`. Knock additions under `LICENSE.KNOCK`.

The transport is the Mac's iPhone Mirroring window: capture + Apple Vision OCR
for eyes, HID-level events for hands. There is no DOM. The capture is ground
truth. Higher helpers live in `agent-workspace/agent_helpers.py`.

```
  agent: open Weather
  ocr() -> "Weather" at (x, y)
  tap_icon("Weather") -> wait_stable_nav() -> ocr() confirms the forecast
```

## Host truth

| Host | What this repo does |
|------|---------------------|
| macOS Sequoia+ | Real install. Pair iPhone Mirroring. Grant Accessibility + Screen Recording. `phone-harness --doctor`. Then act. |
| Windows / Linux | Docs, skill text, and a **fail-closed** doctor. No taps, no OCR, no window capture. |

Windows Phone Link cannot substitute for iPhone Mirroring. `scrcpy` is Android
only. Do not invent a Windows control path in this tree.

Target device profile in this fork: **iPhone 12** (see `docs/iphone-12.md`).

## Layout

| Path | Role |
|------|------|
| `src/phone_harness/` | Protected upstream core (thin). Darwin-gate added in `admin.py` / `run.py`. |
| `agent-workspace/agent_helpers.py` | Agent-editable helpers (iPhone 12 profile, `tap_icon`, `snapshot`, ...) |
| `SKILL.md` | Upstream Mac skill body (`phone-harness skill` prints this) |
| `skill/SKILL.md` | Grok Build skill (Windows-first state check + Mac usage) |
| `install.md` | Upstream Mac permissions bootstrap |
| `docs/` | Usage, iPhone 12, Windows host, Mac bootstrap, upstream README |
| `scripts/doctor.ps1` | Host doctor (fail-closed off Darwin) |
| `scripts/bootstrap-mac.sh` | One-shot Mac install from this checkout |

## Windows checkout

From the checkout:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\doctor.ps1
```

Expected: FAIL on `macOS host`. That is correct. Do not pip-install pyobjc here.

Dev launcher on Windows (doctor / help / skill only):

```powershell
.\phone-harness.cmd --doctor
.\phone-harness.cmd skill
```

## Mac (the only place actions run)

Read `docs/mac-bootstrap.md` and `install.md`. Short form:

```bash
cd /path/to/phone-harness
./scripts/bootstrap-mac.sh
phone-harness --doctor
phone-harness <<'PY'
print(screen_info())
print(connection_state())
PY
```

Two steps only the operator can do:

1. Pair iPhone Mirroring with the physical iPhone 12 (same Apple ID, iOS 18+,
   nearby, Bluetooth + Wi-Fi). When the Mac says "iPhone in Use", **lock the
   phone**. Unlocking the phone pauses mirroring.
2. Grant the **terminal app** Accessibility (immediate) and Screen Recording
   (restart the terminal after). Fresh Macs may prompt for more the first time
   a tap or capture runs.

Never tap Connect / Continue from the agent. Never loop-poll for a lock.

## Usage (Mac, after doctor is green)

```bash
phone-harness <<'PY'
ensure_mirroring()
print(iphone12_profile())
print(window_matches_iphone12())
home()
# ask the operator before opening apps
# tap_icon("Weather")
# wait_stable_nav()
print([o["text"] for o in ocr()][:20])
PY
```

Day-to-day agent rules: `SKILL.md` (Mac) and `skill/SKILL.md` (Grok). Helpers:
`src/phone_harness/helpers.py` plus `agent-workspace/agent_helpers.py`.

## Safety

- Never assume the phone is unlocked or that mirroring is active. Call
  `connection_state()` (`ready` / `blocked` / `no-window` / `not-running`).
- Prefer reversible actions. Home, read, Weather / Notes only with a yes.
- Stop and ask before messages, posts, purchases, deletes, or settings changes.
- Do not linger in Messages, Photos, or Mail beyond the task.
- Face ID, camera, pinch, and DRM video are out of scope.

## License

- Upstream core and original docs: MIT, Copyright (c) 2026 shawn pana.
  Full text in `LICENSE`.
- Knock-authored files (`docs/`, `scripts/`, `skill/`, `AGENTS.md`,
  `LICENSE.KNOCK`, `NOTICE`, Windows launcher, iPhone 12 helpers): proprietary.
  See `LICENSE.KNOCK` and `NOTICE`.
