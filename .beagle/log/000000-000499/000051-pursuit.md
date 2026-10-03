+++
id = "000051-pursuit"
ordinal = 51
kind = "pursuit"
timestamp = "2026-10-03T12:24:08+00:00"
summary = "pursuit open T0030: R02 fix: scorecard reports worker-level health"
metric_command = ""
drains = []
hooks = []
+++

criteria: scorecard.py takes --meta (meta.json) and reports a workers block from meta.worker_sessions: count, turns per worker and max, how many hit the turn cap, timed out, reasoning chars total, empty/raw-tool-call reports; and ended_with_abandoned (finished while abandoned tasks have no done successor). On R02: 17 workers, ended_with_abandoned true.
decided by: sh -c 'echo "f7f52e5047785b6d7d8426418544b28363d96416166677601580db757b86fe22  .beagle/checks/T0030/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0030/check.sh'
budget: 60000 tokens
