"""Agent-editable phone helpers.

Add task-specific primitives here. Core helpers from phone_harness.helpers
load this file at import time; anything defined here is available in
phone-harness scripts alongside the core helpers.

iPhone 12 notes (portrait): native 1170 x 2532 @3x, logical 390 x 844 pt.
Home-screen labels are not tap targets; the icon is ~35 pt above the label.
"""

# Portrait. Landscape swaps the pair. Window size on the Mac is not native
# pixels; compare aspect, not absolute px.
IPHONE12 = {
    "model": "iPhone 12",
    "native_px": (1170, 2532),
    "logical_pt": (390, 844),
    "scale": 3,
    "aspect": 844 / 390,
    "home_label_offset_pt": 35,
    "aspect_slop": 0.08,
}


def iphone12_profile():
    """Static iPhone 12 geometry. Safe to call on any host."""
    return dict(IPHONE12)


def tap_icon(label, index=0):
    """Tap a Home-Screen app icon by its label.

    Learned: tapping the label text itself does NOT launch the app in the
    mirrored Home Screen. The tappable icon is ~35 points above the label.
    Verified against Weather (label tap: no-op; icon tap: launches).
    """
    from phone_harness.helpers import find_text, tap
    hits = find_text(label)
    if not hits:
        raise RuntimeError(f"no Home-Screen label matching {label!r}")
    h = hits[index]
    tap(h["x"], h["y"] - IPHONE12["home_label_offset_pt"])
    return h


def go_home():
    """Home Screen via iPhone Mirroring Cmd+1."""
    from phone_harness.helpers import home
    return home()


def open_settings():
    """Open Settings via Spotlight. Ask the operator before changing values."""
    from phone_harness.helpers import open_app
    return open_app("Settings")


def find_and_tap_text(query, index=0, exact=False, as_icon=False):
    """Tap visible text, or the Home-screen icon above that label."""
    if as_icon:
        return tap_icon(query, index=index)
    from phone_harness.helpers import tap_text
    return tap_text(query, index=index, exact=exact)


def type_and_submit(text):
    """Type into the focused field and press return. Field must already be focused."""
    from phone_harness.helpers import type_text, press, wait_stable
    type_text(text)
    press("return")
    wait_stable()


def snapshot(min_confidence=0.3):
    """Screenshot + OCR + window info for a vision model or a verify step."""
    from phone_harness.helpers import screenshot, ocr, screen_info
    path = screenshot()
    boxes = ocr(min_confidence=min_confidence)
    info = screen_info()
    return {"path": path, "ocr": boxes, "screen": info}


def wait_stable_nav(timeout=8.0):
    """Longer settle for app launches and page transitions on iPhone 12."""
    from phone_harness.helpers import wait_stable
    return wait_stable(timeout=timeout, interval=0.45, settle=2)


def window_matches_iphone12(window=None):
    """True when the mirroring window aspect matches iPhone 12 portrait or landscape."""
    if window is None:
        from phone_harness.helpers import find_window
        window = find_window()
    if not window or not window.get("w") or not window.get("h"):
        return False
    aspect = max(window["w"], window["h"]) / min(window["w"], window["h"])
    return abs(aspect - IPHONE12["aspect"]) <= IPHONE12["aspect_slop"]
