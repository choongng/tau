+++
id = "000462-pursuit"
ordinal = 462
kind = "pursuit"
timestamp = "2026-10-04T02:37:54+00:00"
summary = "pursuit open T0118: Refuse a check that cannot run"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_step refuses to open or amend a task whose check, run once before binding, cannot run: exit 129 (git usage), exit 127 (command not found), exit 2 or 64 with a usage: line, or a SyntaxError traceback from the check's own code; the refusal quotes the first error line and the exit code and dispatches no worker. A check that fails by assertion (exit 1) still opens.
decided by: sh -c 'echo "8c3b44205cc1d8286160b4c6358fcd7532989a2905083ccd802db48ba0391eb9  .beagle/checks/T0118/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0118/check.sh'
budget: 120000 tokens
