+++
id = "001384-pursuit"
ordinal = 1384
kind = "pursuit"
timestamp = "2026-10-10T00:34:50+00:00"
summary = "pursuit open T0330: Output-limit nudge: thinking-off and in-a-row bound in a sub-agent session"
metric_command = ""
drains = []
hooks = []
+++

criteria: R38 class 3: in a tau-subagents agent session the nudged request still thought for the whole 8192 tokens, and four nudges ran in a row past MAX_OUTPUT_LIMIT_CONTINUATIONS=2. Find why (queued follow-up beside the nudge? provider not the guarded one?) and fix in session.py with a regression test.
decided by: sh -c 'echo "34f787de5b7d7db91b753a70fd8d7d9153880e1d5b4e019439a61c957950fd28  .beagle/checks/T0330/T0330.sh" | sha256sum -c --quiet && bash .beagle/checks/T0330/T0330.sh'
budget: 60000 tokens
