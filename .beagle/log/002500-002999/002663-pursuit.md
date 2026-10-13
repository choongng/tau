+++
id = "002663-pursuit"
ordinal = 2663
kind = "pursuit"
timestamp = "2026-10-13T06:13:54+00:00"
summary = "pursuit open T0522: tau ext: an open contract milestone keeps its check when the driver passes another (R87)"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_step keeps an open Contract/Second extraction/Reconcile task on its fixed scope and check whatever done_when the driver passes, says the passed one is not used, and amends a check already substituted back to the fixed one; the open path still forces them; tau extension suite green
decided by: sh -c 'echo "d289d867ab29aa4eef8277845faf465941964dfa227b27a39262209b37de4599  .beagle/checks/T0522/T0522.sh" | sha256sum -c --quiet && bash .beagle/checks/T0522/T0522.sh'
budget: 30000 tokens
opened over T0493, T0517: 522a1919
