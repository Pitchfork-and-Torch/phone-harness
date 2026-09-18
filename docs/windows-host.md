# Windows host

This checkout can live on a Windows PC. It cannot **drive** the iPhone there.

## Why

ShawnPana/phone-harness is a macOS-only transport:

- App: iPhone Mirroring (`com.apple.ScreenContinuity`)
- Eyes: `screencapture` or `CGWindowListCreateImage` + Vision.framework
- Hands: `CGEvent` HID tap or SkyLight `SLPSPostEventRecordTo`

None of that exists on Windows. Phone Link does not expose a tappable iPhone
framebuffer. Do not install `pyobjc` on Windows.

## What to run here

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\doctor.ps1
.\phone-harness.cmd --doctor
.\phone-harness.cmd skill
```

Doctor must FAIL on `macOS host`. That is the correct result.

## What not to run here

- `pip install -e .` (pulls Darwin-only wheels)
- Any stdin script that taps, types, or captures
- Smoke tests against a physical iPhone

## Next host

Install and pair on a Mac. See `docs/mac-bootstrap.md`. Optional later work
(not in this drop): a Windows CLI that SSHs to that Mac and runs
`phone-harness` there. Requires a reachable Mac (Tailscale or LAN SSH).
