+++
id = "002916-pursuit"
ordinal = 2916
kind = "pursuit"
timestamp = "2026-10-14T02:04:37+00:00"
summary = "pursuit prove T0559: WITNESSED — refuses when beagle.py's `return CONTRACT_STEPS if _slice_name(title) and…` is put back as `return None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "de6fd937c39bbe68a993e5a60b2cbf86c90f6e83feba757c7782693aa0842a8e  .beagle/checks/T0559/T0559.sh" | sha256sum -c --quiet && bash .beagle/checks/T0559/T0559.sh'
refutes: refuses when beagle.py's `return CONTRACT_STEPS if _slice_name(title) and…` is put back as `return None` (proven 2026-10-14T02:04:36+00:00; refused at 3 failed, 3 passed, 709 deselected in 2.00s)
refused after 3s of a 2m59s check at: 3 failed, 3 passed, 709 deselected in 2.00s
refused with: 3 failed, 3 passed, 709 deselected in 2.00s
