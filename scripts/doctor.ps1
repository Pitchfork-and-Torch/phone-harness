# Fail-closed host doctor. No phone actions.
# On Windows / Linux: report the Darwin requirement and exit 1.
# On macOS: delegate to phone-harness --doctor when available.

[CmdletBinding()]
param()

$ErrorActionPreference = "Continue"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$fail = $false

function Write-Check {
    param([bool]$Ok, [string]$Label, [string]$Hint = "")
    $mark = if ($Ok) { "PASS" } else { "FAIL" }
    if (-not $Ok) { $script:fail = $true }
    $line = "  [$mark] $Label"
    if (-not $Ok -and $Hint) { $line += " - $Hint" }
    Write-Output $line
}

Write-Output "phone-harness doctor"
Write-Output ""

$isDarwin = $IsMacOS
if (-not $isDarwin -and $env:OS -eq "Windows_NT") { $isDarwin = $false }

Write-Check -Ok $isDarwin -Label "macOS host (iPhone Mirroring transport)" -Hint "this host is not Darwin; pyobjc / Vision / CGEvent / iPhone Mirroring are Darwin-only"

$src = Join-Path $root "src\phone_harness\helpers.py"
Write-Check -Ok (Test-Path $src) -Label "checkout has src/phone_harness" -Hint "clone this repo first"

$cmd = Get-Command phone-harness -ErrorAction SilentlyContinue
if ($isDarwin) {
    Write-Check -Ok ([bool]$cmd) -Label "phone-harness on PATH" -Hint "run scripts/bootstrap-mac.sh"
} else {
    Write-Output "  [SKIP] phone-harness on PATH - n/a off Darwin"
}

if (-not $isDarwin) {
    Write-Output ""
    Write-Output "Windows/Linux cannot drive the phone."
    Write-Output "Next: install on macOS Sequoia+ (docs/mac-bootstrap.md)."
    Write-Output ""
    Write-Output "fix the FAILs above, then re-run"
    exit 1
}

$py = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Check -Ok $false -Label "python3" -Hint "install Python 3.12+"
    Write-Output ""
    Write-Output "fix the FAILs above, then re-run"
    exit 1
}

$env:PYTHONPATH = (Join-Path $root "src")
& python3 -m phone_harness.run --doctor
exit $LASTEXITCODE
