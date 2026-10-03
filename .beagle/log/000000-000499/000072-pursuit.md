+++
id = "000072-pursuit"
ordinal = 72
kind = "pursuit"
timestamp = "2026-10-03T12:59:48+00:00"
summary = "pursuit prove T0031: WITNESSED — refuses when R03.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "266946c887e0f64f177a3b25cd64b49a0ac0adb5abe5439113d5c489046a83d7  .beagle/checks/T0031/scored.sh" | sha256sum -c --quiet && bash .beagle/checks/T0031/scored.sh R03'
refutes: refuses when R03.md is absent (proven 2026-10-03T12:59:37+00:00)
refused after 0s of a 0s check
standing checks red: T0030
