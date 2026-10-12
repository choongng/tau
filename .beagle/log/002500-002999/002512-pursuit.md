+++
id = "002512-pursuit"
ordinal = 2512
kind = "pursuit"
timestamp = "2026-10-12T17:07:02+00:00"
summary = "pursuit open T0496: R36/R38 name tests the twin removal deleted (T0335 red)"
metric_command = ""
drains = []
hooks = []
+++

criteria: R36.md and R38.md Tests: lines name only tests that exist in tau or tau-subagents; the names 88f99810 deleted with the thinking-off twin move to a 'Removed in 88f99810' line saying why, so the history stays readable. T0335's and T0360's resolvers both pass.
decided by: sh -c 'echo "81193430a8689f0bf9737788a776ad38a6606e48cd6f4f78e2b18880a68a050d  .beagle/checks/T0496/T0496.sh" | sha256sum -c --quiet && bash .beagle/checks/T0496/T0496.sh'
budget: 15000 tokens
opened over T0489: standing drift: T0335 and T0360 are red on every prove until it is fixed, so it goes ahead of T0489, whose proves would otherwise report them
