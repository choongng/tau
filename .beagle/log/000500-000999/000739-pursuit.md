+++
id = "000739-pursuit"
ordinal = 739
kind = "pursuit"
timestamp = "2026-10-04T16:42:02+00:00"
summary = "pursuit open T0174: Only a 'Known answers: fix' step may change a locked file; amend path tested"
metric_command = ""
drains = []
hooks = []
+++

criteria: Only a step whose title says it fixes the known answers (starting 'Known answers: fix') may hold, change and re-lock a locked file; an implementation task whose title merely mentions the cases or known answers is refused a scope naming a locked file, and the refusal also happens at amend and on a new route.
decided by: sh -c 'echo "8306fc1588c0256baa5cbf0a0fc88946bad1ea8b1d7839087dde8198790e669c  .beagle/checks/T0174/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0174/check.sh'
budget: 30000 tokens
