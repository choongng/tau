+++
id = "002925-pursuit"
ordinal = 2925
kind = "pursuit"
timestamp = "2026-10-14T02:25:01+00:00"
summary = "pursuit prove T0560: WITNESSED — refuses when beagle.py's `if verdict == \"wrong\" and not _judged_values(sa…` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a7cf0c09049971c0f1207c006b1d3d29c81c2660fb74b01889130dfdfffa7e42  .beagle/checks/T0560/T0560.sh" | sha256sum -c --quiet && bash .beagle/checks/T0560/T0560.sh'
refutes: refuses when beagle.py's `if verdict == "wrong" and not _judged_values(sa…` is put back as `if False:` (proven 2026-10-14T02:25:00+00:00; refused at 1 failed, 3 passed, 714 deselected in 2.38s)
refused after 3s of a 2m44s check at: 1 failed, 3 passed, 714 deselected in 2.38s
refused with: 1 failed, 3 passed, 714 deselected in 2.38s
