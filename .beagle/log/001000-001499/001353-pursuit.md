+++
id = "001353-pursuit"
ordinal = 1353
kind = "pursuit"
timestamp = "2026-10-09T22:59:30+00:00"
summary = "pursuit open T0322: R37 class 1: step-cap refusals give a broken check one notes rerun and stop pointing at refused calls"
metric_command = ""
drains = []
hooks = []
+++

criteria: At the step cap: (1) the unchanged-route escalation says what the last check did instead of 'its check passes each time' when the last check failed; (2) a step whose check failed after steps on the same task that all passed it earns one notes-only rerun on the bound check, past the cap, offered as a whole call whose notes quote the failure, once per task; (3) the driver read guard's refusal on an escalated task and the stop gate's follow-up name the task's current escalation options rather than pursuit_step calls the step guard refuses.
decided by: sh -c 'echo "52ba3ec03f3a2d1cb49d5c0c5d68e6d4ffe0ff6ff011b679a308017cb152e7ac  .beagle/checks/T0322/T0322.sh" | sha256sum -c --quiet && bash .beagle/checks/T0322/T0322.sh'
budget: 120000 tokens
