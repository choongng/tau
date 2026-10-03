+++
id = "000115-pursuit"
ordinal = 115
kind = "pursuit"
timestamp = "2026-10-03T14:44:37+00:00"
summary = "pursuit open T0041: R04 fix: worker guard refuses beagle orientation and python one-liner writes; small guard holes (import-only check, witness in a test file, root abandon)"
metric_command = ""
drains = []
hooks = []
+++

criteria: The worker guard refuses beagle commands and reads under .beagle/ (the brief has everything), and refuses interpreter one-liner writes (python -c open(...,'w')) outside the task's scope, reusing the driver guard's detection; the brief says not to inspect .beagle/ or run beagle. _check_problem refuses a python -c check that is only imports and prints. _prove skips a witness in a test file with a message naming the code the test runs instead. _abandon_problem refuses the root task.
decided by: sh -c 'echo "c2aa3516b7b58dfc2edb6150235c06ca9d63b1c11670e97a4dcd530edb2d4605  .beagle/checks/T0041/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0041/check.sh'
budget: 100000 tokens
