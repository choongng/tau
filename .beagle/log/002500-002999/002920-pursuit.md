+++
id = "002920-pursuit"
ordinal = 2920
kind = "pursuit"
timestamp = "2026-10-14T02:06:58+00:00"
summary = "pursuit prove T0563: WITNESSED — refuses when contract.py's `\"expects: one misreads its source, or an expect…` is put back as `\"expects: one misreads its source. \"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c7eec0f54a0cd18e88dae89e646b493eee665f2a38dffd8d2040074aec8b6f5c  .beagle/checks/T0563/T0563.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0563/T0563.v2.sh'
refutes: refuses when contract.py's `"expects: one misreads its source, or an expect…` is put back as `"expects: one misreads its source. "` (proven 2026-10-14T02:06:35+00:00; refused at 1 failed, 3 passed, 2603 deselected in 0.72s)
refused after 1s of a 1m03s check at: 1 failed, 3 passed, 2603 deselected in 0.72s
refused with: 1 failed, 3 passed, 2603 deselected in 0.72s
standing checks red: T0335, T0360, T0386, T0496
