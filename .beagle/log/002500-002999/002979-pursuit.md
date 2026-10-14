+++
id = "002979-pursuit"
ordinal = 2979
kind = "pursuit"
timestamp = "2026-10-14T03:59:48+00:00"
summary = "pursuit prove T0575: WITNESSED — refuses when contract.py's `if found and found.group(2) in keep:` is put back as `if found:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "39cb033b8ed0c6cf9680c4b198d4c8f8abe5ff0288ffbf79c613fbd2ec5aa68d  .beagle/checks/T0575/T0575.sh" | sha256sum -c --quiet && bash .beagle/checks/T0575/T0575.sh'
refutes: refuses when contract.py's `if found and found.group(2) in keep:` is put back as `if found:` (proven 2026-10-14T03:59:31+00:00; refused at 1 failed, 2613 deselected in 0.62s)
refused after 1s of a 1m11s check at: 1 failed, 2613 deselected in 0.62s
refused with: 1 failed, 2613 deselected in 0.62s
standing checks red: T0335, T0360, T0386, T0496
