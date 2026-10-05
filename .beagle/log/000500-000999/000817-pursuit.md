+++
id = "000817-pursuit"
ordinal = 817
kind = "pursuit"
timestamp = "2026-10-05T01:20:03+00:00"
summary = "pursuit open T0208: Done-by never leaves a task open after a failed close; no worker on an empty scope with a passing check; sibling check uses scope, not titles"
metric_command = ""
drains = []
hooks = []
+++

criteria: The done-by route never leaves a task open when its close fails; no worker is dispatched on an open task whose scope is empty, or whose check is known unproven and already passes; the sibling-owned check refusal counts only a waiting task's declared scope and never a file a done task committed.
decided by: sh -c 'echo "546d67499b2c1c2d4dc7dfe070d783687e4b156638318e699e360a5088e2b194  .beagle/checks/T0208/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0208/check.sh'
budget: 130000 tokens
