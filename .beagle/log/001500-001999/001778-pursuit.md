+++
id = "001778-pursuit"
ordinal = 1778
kind = "pursuit"
timestamp = "2026-10-11T02:46:38+00:00"
summary = "pursuit open T0412: The bool-exit refusal is tested on every route and says what it cannot know"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_step refuses a python -c done_when whose exit status is a bool expression on the amend route and the new-route route, as it does on the open (tests send such a done_when through each). The refusal no longer asserts the check passes bad work: it says the exit is 1 when the expression is true and 0 when false, so the check is right only if the expression means a failure was found, and asks for the explicit form either way; it is true for both sys.exit(bool(failures)) and R44's SystemExit(not bad and ...). Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "38edd181666586017b4297980d9bb836fedf6551ca3c16eaeedcd380b23dc9f8  .beagle/checks/T0412/T0412.sh" | sha256sum -c --quiet && bash .beagle/checks/T0412/T0412.sh'
budget: 40000 tokens
