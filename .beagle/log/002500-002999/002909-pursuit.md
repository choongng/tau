+++
id = "002909-pursuit"
ordinal = 2909
kind = "pursuit"
timestamp = "2026-10-14T01:53:50+00:00"
summary = "pursuit prove T0564: WITNESSED — refuses when pursuit.py's `if number == steps[-1]:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "536762806de7cff2cb95d361c9340fcca80e6b9c3e46a9320d47a206d57682fa  .beagle/checks/T0564/T0564.v3.sh" | sha256sum -c --quiet && bash .beagle/checks/T0564/T0564.v3.sh'
refutes: refuses when pursuit.py's `if number == steps[-1]:` is put back as `if False:` (proven 2026-10-14T01:53:48+00:00; refused at 2 failed, 8 passed, 2593 deselected in 1.78s)
refused after 2s of a 1m53s check at: 2 failed, 8 passed, 2593 deselected in 1.78s
refused with: 2 failed, 8 passed, 2593 deselected in 1.78s
