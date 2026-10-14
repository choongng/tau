+++
id = "002983-pursuit"
ordinal = 2983
kind = "pursuit"
timestamp = "2026-10-14T04:02:50+00:00"
summary = "pursuit prove T0578: WITNESSED — refuses when beagle.py's `\"Read only the lines you cite, by line range (o…` is put back as `\"A cases file needs only the lines it cites: re…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "5e2bf708dc444ba08294523cd890292acd9c0bc7df66b8ce1ca4fb7e09c42154  .beagle/checks/T0578/T0578.sh" | sha256sum -c --quiet && bash .beagle/checks/T0578/T0578.sh'
refutes: refuses when beagle.py's `"Read only the lines you cite, by line range (o…` is put back as `"A cases file needs only the lines it cites: re…` (proven 2026-10-14T04:02:49+00:00; refused at 1 failed, 722 deselected in 0.77s)
refused after 1s of a 2m43s check at: 1 failed, 722 deselected in 0.77s
refused with: 1 failed, 722 deselected in 0.77s
