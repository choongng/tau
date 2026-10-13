+++
id = "002671-pursuit"
ordinal = 2671
kind = "pursuit"
timestamp = "2026-10-13T06:15:03+00:00"
summary = "pursuit prove T0522: WITNESSED — refuses when beagle.py's `scope, done_when = list(fixed[0]), fixed[1] arg…` is put back as `if record.get(\"status\") != \"open\": scope, done_…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "d289d867ab29aa4eef8277845faf465941964dfa227b27a39262209b37de4599  .beagle/checks/T0522/T0522.sh" | sha256sum -c --quiet && bash .beagle/checks/T0522/T0522.sh'
refutes: refuses when beagle.py's `scope, done_when = list(fixed[0]), fixed[1] arg…` is put back as `if record.get("status") != "open": scope, done_…` (proven 2026-10-13T06:14:02+00:00; refused at 1 failed, 1 passed, 845 deselected in 3.71s)
refused after 5s of a 2s check at: 1 failed, 1 passed, 845 deselected in 3.71s
refused with: 1 failed, 1 passed, 845 deselected in 3.71s
