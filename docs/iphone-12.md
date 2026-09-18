# iPhone 12 profile

Target hardware for this private tree. Values are UIKit logical points unless
noted. The Mac mirroring **window** is not native pixels; compare aspect, not
absolute size.

## Geometry (portrait)

| Item | Value |
|------|-------|
| Marketing name | iPhone 12 |
| Native pixels | 1170 x 2532 |
| Scale | 3x |
| Logical points | 390 x 844 |
| Aspect (tall / short) | 2.164 (844 / 390) |
| Home-screen label to icon | about 35 pt upward |

`agent-workspace/agent_helpers.py` exports `IPHONE12`, `iphone12_profile()`,
and `window_matches_iphone12()`.

Landscape swaps the pair. Notch + home indicator still consume the short
edges. Face ID lives in the notch; the harness cannot complete Face ID.

## Continuity / mirroring

iPhone Mirroring needs:

- iOS 18 or later on the phone
- macOS Sequoia (15) or later on the Mac
- Same Apple ID with 2FA
- Bluetooth + Wi-Fi, devices nearby
- Phone locked when the Mac says "iPhone in Use"

Unlocking the iPhone 12 **pauses** the session. That is a physical step.
The agent must not tap through the resume interstitial.

## Gesture feel

- Home / App Switcher / Spotlight: Cmd+1 / Cmd+2 / Cmd+3 through mirroring
  (see `home()`, `app_switcher()`, `open_app()`).
- Home-screen pages: a **fast** flick (`swipe`), not a slow drag.
- Lists: `scroll()` / `scroll_collect()` (wheel on the classic backend, fast
  flick on the background backend). A slow touch-drag barely moves Settings
  and bounces back.
- `tap_text("Weather")` on the Home Screen hits the label and does nothing.
  Use `tap_icon("Weather")`.
- In-app buttons and list rows: `tap_text` is correct.

## OCR

Vision OCR is strong on Settings rows and app chrome, weaker on stylized
icons and very small status-bar text. Unlabeled glyphs need `snapshot()`
plus a vision-capable model. Status-bar clock ticks once a minute; that can
break a naive "identical PNG" settle if the bar is included. Core
`wait_stable()` hashes the full capture; near-misses are rare.

## Out of scope on this device

- Face ID / passcode entry
- Camera / Control Center camera affordances as a sensor
- Pinch / two-finger gestures
- DRM video (renders black in the mirror)
- Multi-phone sessions
