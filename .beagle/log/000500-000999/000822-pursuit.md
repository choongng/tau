+++
id = "000822-pursuit"
ordinal = 822
kind = "pursuit"
timestamp = "2026-10-05T01:32:34+00:00"
summary = "pursuit open T0209: Root plans refuse parts duplicating live tasks; escalation text drops run history"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_plan refuses a root part whose title equals (case-folded) a live task's title, naming it; a milestone added after founding can be abandoned as a duplicate of a live task, and no refusal suggests a bash command the guard refuses; model-facing text names no past run (no R04-style run ids).
decided by: sh -c 'echo "fe009b9167866d32acae8d688f8651f7dc71fed228562beb2821d019ad11f2a8  .beagle/checks/T0209/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0209/check.sh'
budget: 100000 tokens
