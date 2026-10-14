+++
id = "002956-pursuit"
ordinal = 2956
kind = "pursuit"
timestamp = "2026-10-14T03:24:18+00:00"
summary = "pursuit prove T0570: WITNESSED — refuses when contract.py's `refused = codeless_refusal(root, settings, pref…` is put back as `refused = codeless_refusal(root, settings, pref…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "7e5fb206997e7431a3532a0f2ebd4f4cc96949b27c988abaa352825395347659  .beagle/checks/T0570/T0570.sh" | sha256sum -c --quiet && bash .beagle/checks/T0570/T0570.sh'
refutes: refuses when contract.py's `refused = codeless_refusal(root, settings, pref…` is put back as `refused = codeless_refusal(root, settings, pref…` (proven 2026-10-14T03:23:50+00:00; refused at 1 failed, 1 passed, 2608 deselected in 1.19s)
refused after 2s of a 1m00s check at: 1 failed, 1 passed, 2608 deselected in 1.19s
refused with: 1 failed, 1 passed, 2608 deselected in 1.19s
standing checks red: T0335, T0360, T0386, T0496
