+++
id = "000901-pursuit"
ordinal = 901
kind = "pursuit"
timestamp = "2026-10-05T04:45:41+00:00"
summary = "pursuit open T0226: Cases-first and unproven-refusal follow-ups from audit 11"
metric_command = ""
drains = []
hooks = []
+++

criteria: Every branch of the 'already passes and cannot be shown to refuse' refusal puts in its first line a pursuit_step call with concrete argument values (no prose placeholders), within the breaker's quote length; Cases first's not-on-disk holder branch names the data path from the same source as the on-disk branch instead of a hard-coded filename and is tested, as is a holder found only by its pending locks; R24.md's capped-worker count agrees with the scorecard (17 of 20).
decided by: sh -c 'echo "4d0d5fc4090593ac1ae2129d19f363a233dd8571459d9ec9f3f2da2f084f1f16  .beagle/checks/T0226/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0226/check.sh'
budget: 70000 tokens
