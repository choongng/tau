+++
id = "000856-pursuit"
ordinal = 856
kind = "pursuit"
timestamp = "2026-10-05T02:24:58+00:00"
summary = "pursuit open T0217: Escalation names a complete working call in its first line"
metric_command = ""
drains = []
hooks = []
+++

criteria: The escalation's first line carries a complete call the model can make, so the breaker's one-line quote of a repeated call still names it; a bound check that fails on the tree now and runs files in the call's scope is kept in that call as done_when, not rejected as the bound one; the call names scope whenever the call's scope differs from the record's; the L8281-style refusal's suggested call is likewise in its first line.
decided by: sh -c 'echo "7dc16fa2e3db09df2cc484b0691f33422f339366881715d40f8cacb597359f45  .beagle/checks/T0217/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0217/check.sh'
budget: 80000 tokens
