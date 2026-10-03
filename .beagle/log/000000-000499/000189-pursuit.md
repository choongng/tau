+++
id = "000189-pursuit"
ordinal = 189
kind = "pursuit"
timestamp = "2026-10-03T18:17:08+00:00"
summary = "pursuit open T0057: free waits on stalled/abandoned heirs; name depend --drop"
metric_command = ""
drains = []
hooks = []
+++

criteria: Abandoning task N through pursuit_step also drops any wait W->M whose waiting_heirs[M] is N (R08: T0007 waited on T0006 routed to T0011; abandoning T0011 left it). When pursuit_step finds nothing ready, every wait whose target or that target's heir is abandoned or a stalled container is named with its exact 'beagle pursuit depend W M --drop --reason' command, and the wait text says stalled rather than pending for a stalled container. Tests use R08's tree shape.
decided by: sh -c 'echo "bb4f181212580737f46459271a20d3a5346691ba4d7890be3c67b28105791b57  .beagle/checks/T0057/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0057/check.sh'
budget: 80000 tokens
