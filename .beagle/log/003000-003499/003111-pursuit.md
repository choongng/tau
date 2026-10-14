+++
id = "003111-pursuit"
ordinal = 3111
kind = "pursuit"
timestamp = "2026-10-14T20:17:20+00:00"
summary = "pursuit prove T0599: WITNESSED — refuses when beagle.py's `LOCKS_NOTE = \"locks are not taken here` is put back as `CONTRACT_FIRST_NOTE = LOCKS_NOTE = \"locks are n…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "5cd7d038e00c358e1491be88bc1d8f7276d5a5a42c7a0d7e65d503533843c389  .beagle/checks/T0599/T0599.sh" | sha256sum -c --quiet && bash .beagle/checks/T0599/T0599.sh'
refutes: refuses when beagle.py's `LOCKS_NOTE = "locks are not taken here` is put back as `CONTRACT_FIRST_NOTE = LOCKS_NOTE = "locks are n…` (proven 2026-10-14T20:17:19+00:00; refused at contract-mode code left in /home/choong/tautest/tau-wt-048/examples/extensions/beagle.py)
refused after 0s of a 2m36s check at: contract-mode code left in /home/choong/tautest/tau-wt-048/examples/extensions/beagle.py
refused with: contract-mode code left in /home/choong/tautest/tau-wt-048/examples/extensions/beagle.py
