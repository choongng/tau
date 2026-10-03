+++
id = "000110-pursuit"
ordinal = 110
kind = "pursuit"
timestamp = "2026-10-03T14:36:30+00:00"
summary = "pursuit open T0040: R04 fix: escalate after 3 not-done steps on one task, and stop the driver debugging worker files"
metric_command = ""
drains = []
hooks = []
+++

criteria: After 3 pursuit_step results on one task that leave it not done, a further pursuit_step on that task dispatches no worker and is refused with a fixed text naming the choices (pursuit_plan to split it, new_route with rewritten criteria, or stop and tell the user); new_route or a plan of that task resets the count. The unprovable-check memory is keyed by task, so changing the scope does not get past it. After a task's second stays-open result, a driver read/cat/grep of a file in that task's scope is refused, pointing at the step notes or a new route.
decided by: sh -c 'echo "4cd101a91edc8d41c127e75eed47463a3809a7901bf94b95376b9188562affdd  .beagle/checks/T0040/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0040/check.sh'
budget: 120000 tokens
