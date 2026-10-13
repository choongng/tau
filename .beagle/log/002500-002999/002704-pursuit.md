+++
id = "002704-pursuit"
ordinal = 2704
kind = "pursuit"
timestamp = "2026-10-13T15:09:01+00:00"
summary = "pursuit prove T0528: WITNESSED — refuses when beagle.py's `remaining = deadline + events.cut_ms / 1000 - l…` is put back as `remaining = deadline - loop.time()`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "1cc39b78739024be96b7afc69b0ef64a1f8d20be706e5bd2ffc3dd46df237a68  .beagle/checks/T0528/T0528.sh" | sha256sum -c --quiet && bash .beagle/checks/T0528/T0528.sh'
refutes: refuses when beagle.py's `remaining = deadline + events.cut_ms / 1000 - l…` is put back as `remaining = deadline - loop.time()` (proven 2026-10-13T15:08:02+00:00; refused at 1 failed, 11 passed, 840 deselected in 13.05s)
refused after 13s of a 15s check at: 1 failed, 11 passed, 840 deselected in 13.05s
refused with: 1 failed, 11 passed, 840 deselected in 13.05s
standing checks red: T0519
