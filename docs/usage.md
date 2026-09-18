# Usage

## Invoke

Mac (after `pip install -e .`):

```bash
phone-harness --doctor
phone-harness skill
phone-harness <<'PY'
ensure_mirroring()
print([o["text"] for o in ocr()][:15])
PY
```

From a checkout without install:

```bash
./phone-harness --doctor
```

Windows (fail-closed):

```powershell
.\phone-harness.cmd --doctor
powershell -ExecutionPolicy Bypass -File .\scripts\doctor.ps1
```

Helpers are pre-imported into the stdin script namespace, including names
from `agent-workspace/agent_helpers.py`.

## Common patterns

**Read the screen**

```python
ensure_mirroring()
boxes = ocr()
print([(o["text"], o["x"], o["y"], o["confidence"]) for o in boxes])
```

**Home, then open an app by icon**

```python
home()
wait_stable_nav()
tap_icon("Notes")
wait_stable_nav()
```

**Open via Spotlight (in-app name)**

```python
open_app("Settings")
```

**Tap a labeled control**

```python
tap_text("Wi-Fi")
wait_stable()
```

**Type into a focused field**

```python
tap_text("Search")
wait(0.6)
type_and_submit("hello")
```

**Verify**

```python
snap = snapshot()
print(snap["path"])
print([o["text"] for o in snap["ocr"][:20]])
```

**Scroll a list to the end**

```python
result = scroll_collect()
print(result["stop"], len(result["items"]))
```

## Coordinates

All points are **global Mac screen points**, not iPhone pixels. `ocr()`
already converts Vision boxes into that space. Never cache `(x, y)` across
calls; the window moves.

Image-pixel to screen-point (unlabeled icons):

```
sx = window_w / img_px_w
sy = window_h / img_px_h
screen_x = window_x + img_x * sx
screen_y = window_y + img_y * sy
```

`screen_info()` returns `window` and `img_px`.

## Environment

| Variable | Meaning |
|----------|---------|
| `PHONE_HARNESS_BACKGROUND=1` | Default. SkyLight taps without stealing focus. |
| `PHONE_HARNESS_BACKGROUND=0` | Classic backend. Activates the window every time. |
| `PH_AGENT_WORKSPACE` | Override path to `agent_helpers.py`'s folder. |

If the background backend fails to load (SkyLight symbols differ), helpers
fall back to `mirror.py`.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Doctor FAIL `macOS host` | You are not on a Mac. Expected on Windows. |
| pyobjc import error on Mac | `pip install` the frameworks in `pyproject.toml` |
| Capture blank / tiny PNG | Screen Recording granted but terminal not restarted |
| Window not found | Pair / open iPhone Mirroring; phone nearby |
| `blocked` / "iPhone in Use" | Operator locks the phone. Do not tap Connect. |
| Taps do nothing | Accessibility off, or window not receiving events. Try `PHONE_HARNESS_BACKGROUND=0`. |
| `tap_text` on Home does nothing | Use `tap_icon` |
| Typing garbage / missing chars | US keycodes only. Focus a text field first. Emoji will raise. |
| List does not move | Use `scroll` / `scroll_collect`, not a slow `drag` |

## Limits

One phone, one session. No multi-touch. No Face ID. DRM video is black.
OCR is text, not semantics.
