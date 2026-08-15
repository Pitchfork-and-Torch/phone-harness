# phone-harness (folder rules)

Private iPhone control via macOS iPhone Mirroring. Not a public product.

## Transport

- Eyes: window capture + Apple Vision OCR (`ocr.py`).
- Hands: HID events (`mirror.py`) or SkyLight background taps (`background.py`).
- Default backend is background (`PHONE_HARNESS_BACKGROUND=1`). Keyboard still
  makes the window key; mouse does not steal focus.
- There is no accessibility tree inside the mirroring window. AppleScript
  `click at` is a silent no-op.

## Host rules

- Actions run on **macOS Sequoia+ only**.
- Windows / Linux: doctor fail-closed. No taps. No pyobjc install.
- Do not build a Windows iPhone HID stack in this repo.
- `scrcpy` is a different skill (Android). Do not route iPhone work there.

## Safety (non-negotiable)

- Call `connection_state()` before acting. `blocked` / `no-window` /
  `not-running` means STOP and ask the operator to connect or lock the phone.
- Never tap Connect / Continue. Never poll-wait for a lock.
- Ask before messages, posts, purchases, deletes, account or settings changes.
- Smoke tests: Home, then Weather or Notes, only after an explicit yes.
- Unlocking the physical phone pauses mirroring ("iPhone in Use").

## Where to edit

- Task helpers: `agent-workspace/agent_helpers.py` (thin, editable).
- Core (`src/phone_harness/`): keep thin. Prefer helpers over core rewrites.
- iPhone 12 geometry: `IPHONE12` in `agent_helpers.py` + `docs/iphone-12.md`.
- Grok routing: `skill/SKILL.md`. Do not invent a catalog mega-skill.

## PII / GitHub

- This GitHub repo is **private**. Still: no home paths, no personal email,
  no phone numbers, no tokens, no Apple ID in the tree.
- Secret-scan before every commit or push.
- Leave `gh` on Pitchfork-and-Torch after GitHub work.

## Do not

- Jailbreak, WebDriverAgent, or sideload a control agent unless the operator
  explicitly changes architecture.
- Cache tap coordinates across calls. Re-query the window every time.
- Assume Face ID, pinch, camera, or DRM video can be driven.
