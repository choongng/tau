+++
id = "000631-pursuit"
ordinal = 631
kind = "pursuit"
timestamp = "2026-10-04T11:00:50+00:00"
summary = "pursuit open T0150: Open without scope refused; known-answers scope named"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_step refuses to open a task with no scope while the project has references/; for a task with locks (known answers) the refusal names the scope to pass (the locks plus the data test); and a worker on a known-answers task is refused a write to a source path outside its scope.
decided by: sh -c 'echo "4578d4b36fc90b6cb20cefb36f4e46f84da73d76140bc8ff490fe1e321b43885  .beagle/checks/T0150/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0150/check.sh'
budget: 60000 tokens
