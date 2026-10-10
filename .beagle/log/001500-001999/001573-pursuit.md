+++
id = "001573-pursuit"
ordinal = 1573
kind = "pursuit"
timestamp = "2026-10-10T16:26:12+00:00"
summary = "pursuit prove T0358: WITNESSED — refuses when baselines.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "adf2670b532d595059a9cac79594a9a2a0bc39e96d04de44fa60c8337d0e8328  .beagle/checks/T0358/T0358.sh" | sha256sum -c --quiet && bash .beagle/checks/T0358/T0358.sh'
refutes: refuses when baselines.md is absent (proven 2026-10-10T16:26:11+00:00; refused at no dev-notes/itc-runs/baselines.md)
refused after 0s of a 0s check at: no dev-notes/itc-runs/baselines.md
refused with: no dev-notes/itc-runs/baselines.md
