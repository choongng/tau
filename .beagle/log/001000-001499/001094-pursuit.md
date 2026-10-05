+++
id = "001094-pursuit"
ordinal = 1094
kind = "pursuit"
timestamp = "2026-10-05T13:17:56+00:00"
summary = "pursuit open T0264: A check killed at the cap on uncommitted scope code opens as a hang to find"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a check is killed (memory cap or timeout) and its targets import uncommitted files in the task's or a predecessor's scope, pursuit_step opens the task anyway and the brief says the scoped code does not finish (killed at the limit after N s) and to find the loop or growth; new_route does not run a killed check a second time; _run_check scales its timeout from the last recorded clean run (at least 60 s); the driver edit guard, when the ready task last failed to open on a kill, names the pursuit_step call that now opens it.
decided by: sh -c 'echo "2b691256ff61c05cb47e7e0c05db22430b6fc2ab8efb850f1931d37af35393b1  .beagle/checks/T0264/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0264/check.sh'
budget: 100000 tokens
