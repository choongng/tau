+++
id = "001827-pursuit"
ordinal = 1827
kind = "pursuit"
timestamp = "2026-10-11T22:44:12+00:00"
summary = "pursuit open T0442: Worker wall-clock fits the model's speed, and a killed worker's progress reaches the next"
metric_command = ""
drains = []
hooks = []
+++

criteria: A worker's wall clock is commensurate with the session model's decode speed: when tau knows the model's max_tokens and has a measured output rate (tokens per second from earlier worker turns in this session), the default worker wall is at least the time for three maximal turns at that rate (the 900 s default stays as the floor and stays the default when no rate is measured); a model-supplied timeout is clamped to that wall, not to 900. A worker killed at the wall leaves its progress for the next attempt on the same task: the last thinking or text it produced (trimmed) and its uncommitted changed files are in the next attempt's notes or brief (q38fn 10-11: 5 of 9 workers killed at 900 s at ~20 tok/s with max_tokens 16384). Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "b586a5500fd6a4f2e67a880eb7c20ebd6c96d2fc02cdfd7d47015d05c8d00de6  .beagle/checks/T0442/T0442.sh" | sha256sum -c --quiet && bash .beagle/checks/T0442/T0442.sh'
budget: 300000 tokens
