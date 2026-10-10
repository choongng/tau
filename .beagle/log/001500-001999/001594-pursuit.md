+++
id = "001594-pursuit"
ordinal = 1594
kind = "pursuit"
timestamp = "2026-10-10T17:16:08+00:00"
summary = "pursuit open T0372: R41 fix: a step whose worker was cut off reasoning retries thinking-off"
metric_command = ""
drains = []
hooks = []
+++

criteria: beagle.py's _WorkerEvents counts reasoning-only cut-offs (a message_end with stop 'length', thinking present, no text and no tool call). A worker killed at WORKER_CUT_OFFS where any cut-off was reasoning-only gets a kill note saying its reasoning filled the output limit before any reply or call, and the next _run_worker for the same task under the same root passes --thinking off once (then the configured level again), with the worker's note saying it runs thinking-off because of that. Kills by call cut-offs alone, runs already thinking-off, and WORKER_THINKING_OMIT runs are unchanged. Tests test_reasoning_only_cut_off_named_in_worker_note, test_next_attempt_runs_thinking_off_after_reasoning_cut_offs; whole file passes, ruff clean.
decided by: sh -c 'echo "4bc5d9bc406bf3df181b3bdd872ecd7d7ad411e1e01d3cca10f11777e682bee8  .beagle/checks/T0372/T0372.sh" | sha256sum -c --quiet && bash .beagle/checks/T0372/T0372.sh'
budget: 80000 tokens
