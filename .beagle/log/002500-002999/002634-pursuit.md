+++
id = "002634-pursuit"
ordinal = 2634
kind = "pursuit"
timestamp = "2026-10-13T04:26:10+00:00"
summary = "pursuit prove T0519: WITNESSED — refuses when beagle.py's `if seal_note.startswith(\"Sealed\"): seal_note +=…` is put back as `if False: seal_note += await _settle_after_seal…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "2e926877b21c9bc9409a9aff9fdb94e77ebde21a92549ace6afb1aa6902b515d  .beagle/checks/T0519/T0519.sh" | sha256sum -c --quiet && bash .beagle/checks/T0519/T0519.sh'
refutes: refuses when beagle.py's `if seal_note.startswith("Sealed"): seal_note +=…` is put back as `if False: seal_note += await _settle_after_seal…` (proven 2026-10-13T04:25:09+00:00; predates the task: the work was committed as 7a77a357 before the open, which is over it; this is that commit's change; refu
refused after 2s of a 2s check at: 1 failed, 3 passed, 837 deselected in 2.06s
refused with: 1 failed, 3 passed, 837 deselected in 2.06s
