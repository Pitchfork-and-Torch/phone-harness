---
name: phone-harness
description: >
  Control the operator's real iPhone through macOS iPhone Mirroring (capture,
  Vision OCR with tap coordinates, HID tap/swipe/type). Use when the task
  genuinely needs the physical iPhone: iOS-only apps, phone-number or 2FA
  flows, on-device visual checks. Differentiator: iPhone + iPhone Mirroring
  on a Mac - not scrcpy (Android) and not a Windows Phone Link stack.
metadata:
  short-description: "Drive a real iPhone via Mac iPhone Mirroring"
  tags: ["iphone", "ios", "mirroring", "ocr", "private"]
  priority: 40
  example-user-utterances:
    - "use the phone harness"
    - "tap this on my iPhone"
    - "OCR the iPhone screen"
    - "open Settings on the phone"
    - "iPhone Mirroring"
  composes-with: ["scrcpy"]
  private: true
---

# phone-harness

Thin harness: perception + low-level actions + agent-written helpers.
Transport is the Mac **iPhone Mirroring** window. Nothing else.

## State check (always first)

```powershell
powershell -ExecutionPolicy Bypass -File scripts/doctor.ps1
```

Or: `phone-harness --doctor` / `phone-harness.cmd --doctor`.

| Doctor | What you do |
|--------|-------------|
| FAIL `macOS host` | Stop. This machine cannot tap the phone. Report that. Point at `docs/mac-bootstrap.md`. Do not invent a Windows control path. |
| FAIL permissions / window / capture | Relay the first FAIL. Operator pairs mirroring or grants Accessibility / Screen Recording. Do not tap Connect. |
| PASS + `connection_state()` is `ready` | You may read the screen. Ask before any smoke open or irreversible act. |
| `blocked` / `no-window` / `not-running` | Stop. Ask the operator to open iPhone Mirroring and, if it says iPhone in Use, **lock the phone**. Retry once after they confirm. |

`scrcpy` is Android. Do not use it for this iPhone.

## When not to use

If the same job can be done on the Mac or the web (site, API, desktop app),
do it there. This skill is for iOS-only surfaces, the device phone number,
2FA that must happen on the handset, or "how does this look on the phone."

## Mac usage

Helpers are pre-imported. Coordinates are global Mac screen points.

```bash
phone-harness <<'PY'
ensure_mirroring()
print(connection_state())
print(screen_info())
print([o["text"] for o in ocr()][:20])
PY
```

- Read: `ocr()`, `find_text()`, `screenshot()`, `snapshot()`
- Tap: `tap(x, y)`, `tap_text("Label")`, Home-screen `tap_icon("Weather")`
- Nav: `home()` / `go_home()`, `app_switcher()`, `open_app("Notes")`, `open_settings()`
- Gesture: `swipe("up")`, `scroll()`, `scroll_collect()`, `long_press(x, y)`
- Type: focus a field first, then `type_text(...)` or `type_and_submit(...)`
- Settle: `wait_stable()` or `wait_stable_nav()` after every navigation
- iPhone 12: `iphone12_profile()`, `window_matches_iphone12()`

Always `ensure_mirroring()` (or check `connection_state()`) before acting.
Re-query OCR after every action. Never cache coordinates.

Core functions live in `src/phone_harness/helpers.py`. Add task-specific
helpers in `agent-workspace/agent_helpers.py`.

For the full Mac gotcha list (focus, video stream, Home-screen labels,
US keycodes), read root `SKILL.md`. For pairing and permissions, read
`install.md` and `docs/mac-bootstrap.md`.

## Consent

Real phone. Stop and ask before sending a message, posting, purchasing,
deleting, or changing settings. Do not linger in Messages, Photos, or Mail.
Smoke test is Home, then Weather or Notes, **only if the operator says yes**.

## Connection is the operator's job

Never tap Connect / Continue. Never loop-poll. Unlocking the physical
phone pauses mirroring. Face ID cannot be driven.
