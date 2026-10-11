+++
id = "001838-pursuit"
ordinal = 1838
kind = "pursuit"
timestamp = "2026-10-11T23:01:15+00:00"
summary = "pursuit open T0441: Offers and refusals around new_route, attempt limits and container amend agree"
metric_command = ""
drains = []
hooks = []
+++

criteria: tau never offers a move in the same message that forbids it or that its next refusal turns down (q35 10-11 §5): a spawn refusal does not both say 'new_route=true' and 'leave new_route out'; the attempt-limit text reads true ('holds 3 attempts, below beagle's limit of 3' never appears; the number matches _at_spawn_limit); a refusal of a spawn on a pending task says to drop new_route and open/step the task, not to say more in notes; the bash guard on 'beagle pursuit amend <task>' does not send the driver to pursuit_step when pursuit_step refuses that task (a container or a task not open) but names a path that works for it; and the refusal of an infeasible close on a pending task names a move tau accepts for that task. Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "c6949f502314dc74ccd5b44655cc26e6618b639cab8273fa3c5ea5aca1980e24  .beagle/checks/T0441/T0441.sh" | sha256sum -c --quiet && bash .beagle/checks/T0441/T0441.sh'
budget: 300000 tokens
