+++
id = "002628-pursuit"
ordinal = 2628
kind = "pursuit"
timestamp = "2026-10-13T04:17:56+00:00"
summary = "pursuit open T0518: a check whose program is not on PATH is refused at open, not read as failing (R84)"
metric_command = ""
drains = []
hooks = []
+++

criteria: a check whose first word is not a program in the project could not start: _run_check returns 127 with 'the check could not start: …', naming python3 or .venv/bin/python when they are there, so pursuit_step refuses it at open instead of reading it as failing
decided by: sh -c 'echo "3161c693e2fb9e32e39d1c03ce8593116a0248e1d2b3a4d8d164506708894936  .beagle/checks/T0518/T0518.sh" | sha256sum -c --quiet && bash .beagle/checks/T0518/T0518.sh'
budget: 40000 tokens
opened over T0493: 24d24895
