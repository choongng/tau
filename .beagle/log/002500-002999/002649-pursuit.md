+++
id = "002649-pursuit"
ordinal = 2649
kind = "pursuit"
timestamp = "2026-10-13T06:00:44+00:00"
summary = "pursuit prove T0520: WITNESSED — refuses when beagle.py's `_CONTRACT_READ_VERBS = frozenset({\"status\", \"ch…` is put back as `_CONTRACT_READ_VERBS = frozenset({\"status\", \"ch…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "fb6c9aa55682b326033162d5f10cbad3127fb823a833fd3003ca47aa3d452145  .beagle/checks/T0520/T0520.sh" | sha256sum -c --quiet && bash .beagle/checks/T0520/T0520.sh'
refutes: refuses when beagle.py's `_CONTRACT_READ_VERBS = frozenset({"status", "ch…` is put back as `_CONTRACT_READ_VERBS = frozenset({"status", "ch…` (proven 2026-10-13T05:59:44+00:00; refused at 3 failed, 14 passed, 829 deselected in 3.45s)
refused after 4s of a 2s check at: 3 failed, 14 passed, 829 deselected in 3.45s
refused with: 3 failed, 14 passed, 829 deselected in 3.45s
