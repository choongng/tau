+++
id = "001742-pursuit"
ordinal = 1742
kind = "pursuit"
timestamp = "2026-10-11T01:23:42+00:00"
summary = "pursuit open T0403: A worker's out-of-scope write refusal says what it can write instead"
metric_command = ""
drains = []
hooks = []
+++

criteria: In make_worker_scope_guard, the second and later refusal of the same out-of-scope path in one worker session says it is refused again with how many times, that no write outside the scope will be taken, and to write only under the scope or end the turn now with its report naming that path as needed. The first refusal of a path keeps today's text; a different path's first refusal is a first. Mining: 210 of 400 worker scope refusals repeated an already-refused path, in 64 of 135 sessions. Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "edfdac420835ae307d4d4e8b8f7461f0247886b4417b7421141be2a9d9240d9b  .beagle/checks/T0403/T0403.sh" | sha256sum -c --quiet && bash .beagle/checks/T0403/T0403.sh'
budget: 60000 tokens
