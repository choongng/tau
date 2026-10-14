+++
id = "003024-pursuit"
ordinal = 3024
kind = "pursuit"
timestamp = "2026-10-14T04:46:29+00:00"
summary = "pursuit prove T0572: WITNESSED — refuses when contract.py's `judged = [eid for eid, k in kind.items() if k i…` is put back as `judged = []`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "4b2b4baf09b6de4612508c09136fa5ecc433ecd716c8484c76dd09185a48eaff  .beagle/checks/T0572/T0572.sh" | sha256sum -c --quiet && bash .beagle/checks/T0572/T0572.sh'
refutes: refuses when contract.py's `judged = [eid for eid, k in kind.items() if k i…` is put back as `judged = []` (proven 2026-10-14T04:46:07+00:00; refused at 4 failed, 2 passed, 2617 deselected in 1.41s)
refused after 2s of a 1m05s check at: 4 failed, 2 passed, 2617 deselected in 1.41s
refused with: 4 failed, 2 passed, 2617 deselected in 1.41s
standing checks red: T0335, T0360, T0386, T0496
