+++
id = "002846-pursuit"
ordinal = 2846
kind = "pursuit"
timestamp = "2026-10-13T23:42:40+00:00"
summary = "pursuit prove T0555: WITNESSED — refuses when contract.py's `if listed:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a421bd15f01f75fd05c5201235ec55626a7dd755c8b0fe81c99ed90cea7824fc  .beagle/checks/T0555/T0555.sh" | sha256sum -c --quiet && bash .beagle/checks/T0555/T0555.sh'
refutes: refuses when contract.py's `if listed:` is put back as `if False:` (proven 2026-10-13T23:42:19+00:00; refused at 2 failed, 3 passed, 62 deselected in 1.91s)
refused after 2s of a 1m06s check at: 2 failed, 3 passed, 62 deselected in 1.91s
refused with: 2 failed, 3 passed, 62 deselected in 1.91s
