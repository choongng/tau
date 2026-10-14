+++
id = "003134-pursuit"
ordinal = 3134
kind = "pursuit"
timestamp = "2026-10-14T21:46:47+00:00"
summary = "pursuit prove T0599: WITNESSED — refuses when beagle.py's `LOCKS_NOTE = \"locks are not taken here` is put back as `CONTRACT_FIRST_NOTE = LOCKS_NOTE = \"locks are n…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "360b0a6910580c3a87db8e0ade9bff0eff8ee59b7a545a4f4784ebce2f9527e2  .beagle/checks/T0599/T0599.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0599/T0599.v2.sh'
refutes: refuses when beagle.py's `LOCKS_NOTE = "locks are not taken here` is put back as `CONTRACT_FIRST_NOTE = LOCKS_NOTE = "locks are n…` (proven 2026-10-14T21:46:47+00:00; refused at contract-mode code left in /home/choong/tautest/tau-wt-048/examples/extensions/beagle.py)
refused after 0s of a 2m38s check at: contract-mode code left in /home/choong/tautest/tau-wt-048/examples/extensions/beagle.py
refused with: contract-mode code left in /home/choong/tautest/tau-wt-048/examples/extensions/beagle.py
