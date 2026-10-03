+++
id = "000379-pursuit"
ordinal = 379
kind = "pursuit"
timestamp = "2026-10-03T21:18:33+00:00"
summary = "pursuit open T0087: implementation-under-tests lead tested on the worker-problem and prove-refused branches"
metric_command = ""
drains = []
hooks = []
+++

criteria: T0068's 'The sub-agent wrote implementation into tests/ …' lead appears on each of the three not-done branches of the step result: the worker-problem branch (run.problem), the check-still-fails branch, and the prove-refused branch; a test pins each (the existing check-fails test plus two new ones). Code may route the three through one helper; behaviour otherwise unchanged.
decided by: sh -c 'echo "994302d18896d2522429f640f63685a213d53d9145ce56b2051b4f35c6c10e6d  .beagle/checks/T0087/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0087/check.sh'
budget: 15000 tokens
