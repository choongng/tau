+++
id = "002629-pursuit"
ordinal = 2629
kind = "pursuit"
timestamp = "2026-10-13T04:19:04+00:00"
summary = "pursuit prove T0518: WITNESSED — refuses when beagle.py's `missing = _missing_program(argv[0], root) if mi…` is put back as `missing = \"\" if missing:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3161c693e2fb9e32e39d1c03ce8593116a0248e1d2b3a4d8d164506708894936  .beagle/checks/T0518/T0518.sh" | sha256sum -c --quiet && bash .beagle/checks/T0518/T0518.sh'
refutes: refuses when beagle.py's `missing = _missing_program(argv[0], root) if mi…` is put back as `missing = "" if missing:` (proven 2026-10-13T04:18:06+00:00; predates the task: the work was written on branch check-program while R85 ran, and 24d24895 is that merge; the task is opened over it to record it,
refused after 2s of a 1s check at: 1 failed, 838 deselected in 1.35s
refused with: 1 failed, 838 deselected in 1.35s
