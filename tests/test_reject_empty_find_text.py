"""Empty find_text/tap_text query must not match every OCR box."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from phone_harness import helpers


class TestRejectEmptyFindText(unittest.TestCase):
    def test_find_text_rejects_empty(self):
        with self.assertRaises(ValueError):
            helpers.find_text("")
        with self.assertRaises(ValueError):
            helpers.find_text("   ")

    def test_tap_text_rejects_empty_before_ocr(self):
        with patch.object(helpers, "ocr") as ocr:
            with self.assertRaises(ValueError):
                helpers.tap_text("")
            ocr.assert_not_called()

    def test_tap_text_index_out_of_range(self):
        boxes = [{"text": "Hi", "x": 1, "y": 2, "w": 3, "h": 4, "confidence": 1.0}]
        with patch.object(helpers, "ocr", return_value=boxes):
            with self.assertRaises(RuntimeError) as cm:
                helpers.tap_text("Hi", index=3)
        self.assertIn("out of range", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
