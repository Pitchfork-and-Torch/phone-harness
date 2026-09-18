"""scroll must reject non-positive amount with a clear error."""

from __future__ import annotations

import importlib
import os
import sys
import types
import unittest
from unittest.mock import MagicMock, patch


def _install_mac_stubs() -> None:
    """phone_harness.ocr imports Quartz/Vision; stub them on Linux CI."""
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


class TestScrollAmount(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.helpers = _load_helpers()

    def test_zero_amount_rejected(self):
        with patch.object(self.helpers, "_win") as win:
            with self.assertRaises(ValueError) as cm:
                self.helpers.scroll(amount=0)
            win.assert_not_called()
        msg = str(cm.exception).lower()
        self.assertIn("amount", msg)
        self.assertIn("positive", msg)

    def test_negative_amount_rejected(self):
        with patch.object(self.helpers, "_win") as win:
            with self.assertRaises(ValueError) as cm:
                self.helpers.scroll(amount=-50)
            win.assert_not_called()
        self.assertIn("amount", str(cm.exception).lower())

    def test_positive_amount_reaches_backend(self):
        with patch.object(
            self.helpers, "_win", return_value={"x": 0, "y": 0, "w": 100, "h": 200}
        ):
            with patch.object(self.helpers.mirror, "scroll_wheel") as wheel:
                self.helpers.scroll(amount=120)
                wheel.assert_called_once()
                self.assertEqual(wheel.call_args[0][0], -120)


if __name__ == "__main__":
    unittest.main()
