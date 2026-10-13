+++
id = "002773-pursuit"
ordinal = 2773
kind = "pursuit"
timestamp = "2026-10-13T20:27:36+00:00"
summary = "pursuit prove T0541: WITNESSED — refuses when contract.py's `shared, odd = codeless_outliers(root, settings,…` is put back as `shared, odd = \"\", {}`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "afc053d9f2f60479eaff83f4bfadf136c9f087172871d91b68d61d6de7a30aa7  .beagle/checks/T0541/T0541.sh" | sha256sum -c --quiet && bash .beagle/checks/T0541/T0541.sh'
refutes: refuses when contract.py's `shared, odd = codeless_outliers(root, settings,…` is put back as `shared, odd = "", {}` (proven 2026-10-13T20:26:38+00:00; refused at 1 failed, 61 deselected in 0.36s)
refused after 1s of a 1s check at: 1 failed, 61 deselected in 0.36s
refused with: 1 failed, 61 deselected in 0.36s
standing checks red: T0519
