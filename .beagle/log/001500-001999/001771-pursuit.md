+++
id = "001771-pursuit"
ordinal = 1771
kind = "pursuit"
timestamp = "2026-10-11T02:30:08+00:00"
summary = "pursuit open T0410: pursuit_step's spawn-refused offer for a blocked task at the limit is one tau accepts"
metric_command = ""
drains = []
hooks = []
+++

criteria: When beagle refuses pursuit_step's spawn for a blocked task whose retry chain is at the limit, the result offers no infeasible close (tau's _close_infeasible refuses a task not open): it offers the parent's re-plan, or says stop and ask the user when there is no parent. An open task at the limit still gets the infeasible close then the re-plan. The rule lives where every _spawn_limit_offer caller gets it. Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "d2e9c3da64dfe1e8d191679c57a9b0ccc76d2fedd49dc64e1aa488ecbc48e004  .beagle/checks/T0410/T0410.sh" | sha256sum -c --quiet && bash .beagle/checks/T0410/T0410.sh'
budget: 40000 tokens
