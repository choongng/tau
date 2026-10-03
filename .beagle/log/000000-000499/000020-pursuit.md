+++
id = "000020-pursuit"
ordinal = 20
kind = "pursuit"
timestamp = "2026-10-03T10:56:01+00:00"
summary = "pursuit prove T0020: WITNESSED — refuses when grade.json is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "266946c887e0f64f177a3b25cd64b49a0ac0adb5abe5439113d5c489046a83d7  .beagle/checks/T0020/scored.sh" | sha256sum -c --quiet && bash .beagle/checks/T0020/scored.sh R01'
refutes: refuses when grade.json is absent (proven 2026-10-03T10:56:00+00:00)
refused after 0s of a 0s check
standing checks red: T0019
