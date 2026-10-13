+++
id = "002731-pursuit"
ordinal = 2731
kind = "pursuit"
timestamp = "2026-10-13T19:33:43+00:00"
summary = "pursuit prove T0536: WITNESSED — refuses when contract.py's `refused = codeless_refusal(root, settings, pref…` is put back as `refused = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "539b160a87933bb6093834aa6ac8f7807b574a9ce4f88478ad0f6dda26a276ef  .beagle/checks/T0536/T0536.sh" | sha256sum -c --quiet && bash .beagle/checks/T0536/T0536.sh'
refutes: refuses when contract.py's `refused = codeless_refusal(root, settings, pref…` is put back as `refused = None` (proven 2026-10-13T19:32:42+00:00; refused at 1 failed, 1 passed, 57 deselected in 1.12s)
refused after 2s of a 2s check at: 1 failed, 1 passed, 57 deselected in 1.12s
refused with: 1 failed, 1 passed, 57 deselected in 1.12s
