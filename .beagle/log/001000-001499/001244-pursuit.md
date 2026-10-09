+++
id = "001244-pursuit"
ordinal = 1244
kind = "pursuit"
timestamp = "2026-10-09T18:44:53+00:00"
summary = "pursuit prove T0295: WITNESSED — refuses when scored.sh is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "1d1eb64f0efbf4921df6f5c8476857d584d98653caab9c34d6a365fabc71f229  .beagle/checks/T0295/T0295.sh" | sha256sum -c --quiet && bash .beagle/checks/T0295/T0295.sh'
refutes: refuses when scored.sh is absent (proven 2026-10-09T18:43:56+00:00; refused at grep: .beagle/checks/runs/v6/scored.sh: No such file or directory)
refused after 2s of a 4s check at: grep: .beagle/checks/runs/v6/scored.sh: No such file or directory
refused with: grep: .beagle/checks/runs/v6/scored.sh: No such file or directory
standing checks red: T0023
