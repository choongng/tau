+++
id = "000636-pursuit"
ordinal = 636
kind = "pursuit"
timestamp = "2026-10-04T11:05:53+00:00"
summary = "pursuit open T0151: Amend keeps a known-answers check on its data"
metric_command = ""
drains = []
hooks = []
+++

criteria: An amended done_when is refused when it already passes, when it runs pytest --collect-only, or, for a task with pending locks, when it reads no locked file; a not-done result whose check failed on a missing locked file names that file as the work rather than inviting a corrected check; the shell-operator refusal on an amend says the bound check stands when it is one valid command.
decided by: sh -c 'echo "7c809ee8d1f6132f53b7b905d020a5969c8d3e6e04adcae8696737b0ec4da341  .beagle/checks/T0151/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0151/check.sh'
budget: 60000 tokens
