+++
id = "001291-pursuit"
ordinal = 1291
kind = "pursuit"
timestamp = "2026-10-09T21:18:35+00:00"
summary = "pursuit open T0310: R36 fix: a new_route with rewritten criteria keeps the old criteria and moves the new text to notes"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_step with new_route=true and criteria differing from the task's recorded criteria is no longer refused for the criteria: the task keeps its recorded criteria, the call's criteria text is folded into the step's notes, and the result begins 'Criteria kept from <task>; yours went into the notes'. The call then goes on to the done_when check and T0292's same-route check, so a call that changes nothing else (same bound check, same scope, at the escalation count) gets the 'a new route that changes nothing gets the same result' refusal rather than a criteria refusal. Keyed on the call versus the task record; no prompt words.
decided by: sh -c 'echo "b698edfbc5359aed63e12c35be58853b6a89448e0c136987f4ab29025765127c  .beagle/checks/T0310/T0310.sh" | sha256sum -c --quiet && bash .beagle/checks/T0310/T0310.sh'
budget: 120000 tokens
