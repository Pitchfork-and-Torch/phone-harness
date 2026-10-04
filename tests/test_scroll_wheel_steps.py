"""scroll_wheel must reject non-positive steps (avoid ZeroDivisionError)."""

from __future__ import annotations

import importlib
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


def _install_mac_stubs() -> None:
    for name in ("Quartz", "Vision", "Foundation", "AppKit", "ApplicationServices"):
        if name not in sys.modules:
            sys.modules[name] = types.ModuleType(name)
    q = sys.modules["Quartz"]
    for attr in (
        "CGEventCreateKeyboardEvent", "CGEventSetFlags", "CGEventPost",
        "CGEventCreateScrollWheelEvent", "CGEventSetLocation", "CGPointMake",
        "kCGEventFlagMaskShift", "kCGEventFlagMaskCommand",
        "kCGEventFlagMaskAlternate", "kCGEventFlagMaskControl",
        "kCGEventMouseMoved", "kCGEventLeftMouseDown", "kCGEventLeftMouseUp",
        "kCGEventLeftMouseDragged", "kCGHIDEventTap", "kCGScrollEventUnitPixel",
        "CGWindowListCopyWindowInfo", "kCGWindowListOptionOnScreenOnly",
        "kCGNullWindowID",
    ):
        if not hasattr(q, attr):
            setattr(q, attr, MagicMock() if not attr.startswith("kCG") else 0)
    app = sys.modules["AppKit"]
    if not hasattr(app, "NSRunningApplication"):
        app.NSRunningApplication = MagicMock()
    if not hasattr(app, "NSWorkspace"):
        app.NSWorkspace = MagicMock()


def _load_mirror():
    _install_mac_stubs()
    for mod in ("phone_harness.mirror", "phone_harness.background"):
        sys.modules.pop(mod, None)
    import phone_harness.mirror as mirror
    importlib.reload(mirror)
    return mirror


class TestScrollWheelSteps(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mirror = _load_mirror()

    def test_zero_steps_rejected(self):
        with patch.object(self.mirror, "_focus") as focus:
            with self.assertRaises(ValueError) as cm:
                self.mirror.scroll_wheel(300, 0, 0, steps=0)
            focus.assert_not_called()
        msg = str(cm.exception).lower()
        self.assertIn("steps", msg)
        self.assertNotIn("division", msg)

    def test_negative_steps_rejected(self):
        with patch.object(self.mirror, "_focus") as focus:
            with self.assertRaises(ValueError) as cm:
                self.mirror.scroll_wheel(300, 0, 0, steps=-3)
            focus.assert_not_called()
        self.assertIn("steps", str(cm.exception).lower())

    def test_positive_steps_reaches_focus(self):
        with patch.object(self.mirror, "_focus") as focus:
            with patch.object(self.mirror, "_post_mouse"):
                self.mirror.scroll_wheel(100, 1, 2, steps=2)
            focus.assert_called()

    def test_background_source_guards_steps(self):
        # background imports SkyLight at module load (macOS-only). Assert the
        # same steps guard is present in source so Linux CI still covers it.
        src = (Path(__file__).resolve().parents[1] / "src/phone_harness/background.py").read_text()
        self.assertIn("scroll_wheel steps must be positive", src)
        self.assertIn("if steps is None or steps <= 0:", src)


if __name__ == "__main__":
    unittest.main()
