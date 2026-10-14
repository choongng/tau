+++
id = "002947-pursuit"
ordinal = 2947
kind = "pursuit"
timestamp = "2026-10-14T03:20:26+00:00"
summary = "pursuit prove T0571: WITNESSED — refuses when beagle.py's `why = _commit_only(root, [*sealed, CONTRACT_DRA…` is put back as `why = _commit_only(root, [*sealed], [subject, *…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "e4a5f0c9d966fe17edf402a97ffaed551e1cd4cdfed045fb532238cfa4772a4a  .beagle/checks/T0571/T0571.sh" | sha256sum -c --quiet && bash .beagle/checks/T0571/T0571.sh'
refutes: refuses when beagle.py's `why = _commit_only(root, [*sealed, CONTRACT_DRA…` is put back as `why = _commit_only(root, [*sealed], [subject, *…` (proven 2026-10-14T03:20:25+00:00; refused at 1 failed, 718 deselected in 3.58s)
refused after 4s of a 2m54s check at: 1 failed, 718 deselected in 3.58s
refused with: 1 failed, 718 deselected in 3.58s
