+++
id = "002993-pursuit"
ordinal = 2993
kind = "pursuit"
timestamp = "2026-10-14T04:15:39+00:00"
summary = "pursuit prove T0573: WITNESSED — refuses when beagle.py's `if _bash_find(command, _contract_run_operation)…` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "1b2cfd1435eb52893c1828fc9c7eaeeee4a687b7c1561c5e5794d4d6982f7771  .beagle/checks/T0573/T0573.sh" | sha256sum -c --quiet && bash .beagle/checks/T0573/T0573.sh'
refutes: refuses when beagle.py's `if _bash_find(command, _contract_run_operation)…` is put back as `if False:` (proven 2026-10-14T04:15:38+00:00; refused at 1 failed, 723 deselected in 0.77s)
refused after 1s of a 2m36s check at: 1 failed, 723 deselected in 0.77s
refused with: 1 failed, 723 deselected in 0.77s
