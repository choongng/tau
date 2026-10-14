+++
id = "003146-pursuit"
ordinal = 3146
kind = "pursuit"
timestamp = "2026-10-14T22:43:33+00:00"
summary = "pursuit open T0609: a source task's check runs its cases (S02)"
metric_command = ""
drains = []
hooks = []
+++

criteria: For a task with a source, pursuit_step refuses a done_when that names no test file (S02's python -c of the driver's own asserts), telling the driver to use the project's test command over the case file with no expected values in it; the next-task text says the same. Upstream ask 9 (open --cases accepts a check that runs no case) is filed. The extension's suites pass.
decided by: sh -c 'echo "15f4e067ff4bc59074734e3d90bb9de45e3b458f27bb7f9e119c0c508df962a9  .beagle/checks/T0609/T0609.sh" | sha256sum -c --quiet && bash .beagle/checks/T0609/T0609.sh'
budget: 100000 tokens
opened over T0605, T0607, T0608, T0606: S02's fix, needed before R100; done before the open, so the check passes at open
