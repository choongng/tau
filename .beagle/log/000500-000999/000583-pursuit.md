+++
id = "000583-pursuit"
ordinal = 583
kind = "pursuit"
timestamp = "2026-10-04T08:34:50+00:00"
summary = "pursuit open T0140: Unpassable known-answers check caught after the test exists"
metric_command = ""
drains = []
hooks = []
+++

criteria: A pursuit_step resend of an open task whose bound check runs a test importing a module no scope path writes is refused before any sub-agent, naming the module and the data-test done_when; when attempt 1 leaves a test importing such a module, attempt 2 does not run and the result leads with that; the not-done result says the check cannot pass and names the data-test done_when. When the escalation's own proposed done_when (the data test) is sent without new_route=true, tau takes it as the new route and says so; an escalation refusal repeats the full working call; a data-test fallback outside the task's scope is added to the scope it proposes.
decided by: sh -c 'echo "480c5858eb7ca098c4cfa12aa008e0dc241541f66d70fdb0271a285f3b19a4a1  .beagle/checks/T0140/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0140/check.sh'
budget: 90000 tokens
