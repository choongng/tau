+++
id = "002762-pursuit"
ordinal = 2762
kind = "pursuit"
timestamp = "2026-10-13T20:17:05+00:00"
summary = "pursuit prove T0539: WITNESSED — refuses when beagle.py's `\"bounds and worked examples to the contract rea…` is put back as `\"bounds and worked examples to the sources: a v…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "750b66eae20c913164e45b5cea1502fce44aac12877e6176b89dd31f51064315  .beagle/checks/T0539/T0539.sh" | sha256sum -c --quiet && bash .beagle/checks/T0539/T0539.sh'
refutes: refuses when beagle.py's `"bounds and worked examples to the contract rea…` is put back as `"bounds and worked examples to the sources: a v…` (proven 2026-10-13T20:16:08+00:00; refused at 1 failed, 854 deselected in 2.71s)
refused after 3s of a 3s check at: 1 failed, 854 deselected in 2.71s
refused with: 1 failed, 854 deselected in 2.71s
standing checks red: T0519
