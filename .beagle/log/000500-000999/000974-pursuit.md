+++
id = "000974-pursuit"
ordinal = 974
kind = "pursuit"
timestamp = "2026-10-05T07:50:55+00:00"
summary = "pursuit open T0239: At beagle's attempt limit tau offers a close it can make"
metric_command = ""
drains = []
hooks = []
+++

criteria: Once a task's retry chain (sibling_of back to its first route) is at beagle's spawn limit, no tau result offers new_route for it; tau offers a close it can make instead: for an open task, pursuit_step abandon='infeasible: <evidence>' closes it infeasible (or blocked) in beagle so its parent can be re-planned; Cases first never sends the driver to 'open' a holder that is already open.
decided by: sh -c 'echo "79d1b9e1609416c09dc3d8e019658e6229a5e03c5741d44f4052fa24e203b4dc  .beagle/checks/T0239/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0239/check.sh'
budget: 80000 tokens
