"""scroll_screen must reject non-positive amount with a clear error.

Distinct from scroll() amount (#7) and swipe distance (#6): scroll_screen's
fraction used to no-op at 0 or reverse direction when negative.
"""

from __future__ import annotations

import importlib
import os
import sys
import types
import unittest
from unittest.mock import MagicMock, patch


def _install_mac_stubs() -> None:
    for name in ("Quartz", "Vision", "Foundation", "AppKit", "ApplicationServices"):
        if name not in sys.modules:
            sys.modules[name] = types.ModuleType(name)
    q = sys.modules["Quartz"]
    for attr in (
        "CGEventCreateKeyboardEvent", "CGEventSetFlags", "CGEventPostToPid",
        "kCGEventFlagMaskShift", "CGWindowListCopyWindowInfo",
        "kCGWindowListOptionOnScreenOnly", "kCGNullWindowID",
    ):
        if not hasattr(q, attr):
            setattr(q, attr, MagicMock())


def _load_helpers():
    _install_mac_stubs()
    os.environ["PHONE_HARNESS_BACKGROUND"] = "0"
    for mod in (
        "phone_harness.ocr",
        "phone_harness.mirror",
        "phone_harness.helpers",
        "phone_harness.background",
    ):
        sys.modules.pop(mod, None)

    ocr = types.ModuleType("phone_harness.ocr")
    sys.modules["phone_harness.ocr"] = ocr

    mirror = types.ModuleType("phone_harness.mirror")
    for name in (
        "tap", "long_press", "drag", "press", "type_text", "activate",
        "find_window", "ensure_window", "running_app", "capture",
        "is_frontmost", "scroll_wheel",
    ):
        setattr(mirror, name, MagicMock())
    sys.modules["phone_harness.mirror"] = mirror

    import phone_harness.helpers as helpers
    importlib.reload(helpers)
    return helpers


class TestScrollScreenAmount(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.helpers = _load_helpers()

    def test_zero_amount_rejected(self):
        with patch.object(self.helpers.mirror, "scroll_wheel") as sw:
            with self.assertRaises(ValueError) as cm:
                self.helpers.scroll_screen(amount=0)
            sw.assert_not_called()
        msg = str(cm.exception).lower()
        self.assertIn("amount", msg)
        self.assertIn("positive", msg)

    def test_negative_amount_rejected(self):
        with patch.object(self.helpers.mirror, "scroll_wheel") as sw:
            with self.assertRaises(ValueError) as cm:
                self.helpers.scroll_screen(direction="up", amount=-0.5)
            sw.assert_not_called()
        self.assertIn("amount", str(cm.exception).lower())

    def test_positive_amount_reaches_backend(self):
        boxes = [{"text": "A", "confidence": 0.9, "x": 1, "y": 50, "w": 10, "h": 10}]
        self.helpers.mirror.ensure_window.return_value = {
            "x": 0, "y": 0, "w": 100, "h": 200, "id": 1
        }
        with patch.object(self.helpers.time, "sleep", return_value=None):
            with patch.object(self.helpers, "_content_texts", return_value=boxes):
                self.helpers.scroll_screen(direction="up", amount=0.5)
        self.helpers.mirror.scroll_wheel.assert_called()
        dy = self.helpers.mirror.scroll_wheel.call_args[0][0]
        self.assertEqual(dy, -100)  # sign -1 * int(200*0.5)


if __name__ == "__main__":
    unittest.main()
