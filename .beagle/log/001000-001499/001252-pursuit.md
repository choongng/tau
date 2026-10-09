+++
id = "001252-pursuit"
ordinal = 1252
kind = "pursuit"
timestamp = "2026-10-09T19:05:02+00:00"
summary = "pursuit open T0292: R35 fix: an escalation's offered route must change the call"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a new_route supersedes a task and keeps its done_when and scope, the not-done count and demand carry to the successor instead of being forgotten; an escalation whose only available check is the kept bound one does not offer new_route as the call that works, but offers pursuit_plan splitting the files one per part (or stopping); a new_route whose done_when, scope and criteria equal the bound task's is refused once the not-done count has reached the escalation threshold, saying a route that changes nothing gets the same result. Keyed on structure (check/scope equality, counts), no prompt-specific words. Regression tests for each.
decided by: sh -c 'echo "54ad0d23b1876a5e81062d007eff02a7f2d4358e10c006cca6c253e32e421850  .beagle/checks/T0292/T0292.sh" | sha256sum -c --quiet && bash .beagle/checks/T0292/T0292.sh'
budget: 150000 tokens
