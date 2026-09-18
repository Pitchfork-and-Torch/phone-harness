#!/bin/sh
# One-shot Mac install from this checkout. Does not pair the phone.
# Does not grant Accessibility or Screen Recording (operator must click those).
set -eu

ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ "$(uname -s)" != "Darwin" ]; then
  echo "bootstrap-mac.sh must run on macOS Sequoia+." >&2
  echo "This host is $(uname -s). See docs/windows-host.md." >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found. Install Python 3.12+." >&2
  exit 1
fi

echo "Installing pyobjc frameworks..."
python3 -m pip install --user \
  pyobjc-framework-Quartz \
  pyobjc-framework-Vision \
  pyobjc-framework-AppKit \
  pyobjc-framework-ApplicationServices

echo "Installing editable phone-harness (no dep resolve)..."
python3 -m pip install --user -e . --no-deps

chmod +x "$ROOT/phone-harness" "$ROOT/scripts/bootstrap-mac.sh"

echo "Running doctor..."
if command -v phone-harness >/dev/null 2>&1; then
  phone-harness --doctor
else
  PYTHONPATH="$ROOT/src" python3 -m phone_harness.run --doctor
fi

echo ""
echo "If doctor is not all-clear: pair iPhone Mirroring and grant"
echo "Accessibility + Screen Recording (see docs/mac-bootstrap.md)."
