+++
id = "001599-pursuit"
ordinal = 1599
kind = "pursuit"
timestamp = "2026-10-10T18:30:29+00:00"
summary = "pursuit prove T0373: WITNESSED — refuses when R42.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "1c47cd66c0ea6894242392b7951f5d4bcfa14bcaecf6d7eb7c9f5113826c34b4  .beagle/checks/T0373/T0373.sh" | sha256sum -c --quiet && bash .beagle/checks/T0373/T0373.sh'
refutes: refuses when R42.md is absent (proven 2026-10-10T18:29:32+00:00)
refused after 0s of a 0s check
standing checks red: T0368
