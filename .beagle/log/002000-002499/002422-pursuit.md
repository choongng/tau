+++
id = "002422-pursuit"
ordinal = 2422
kind = "pursuit"
timestamp = "2026-10-12T14:56:00+00:00"
summary = "pursuit open T0474: A worker's git commit gets the worker refusal, not beagle's commit-claims advice (R59)"
metric_command = ""
drains = []
hooks = []
+++

criteria: In a worker the worker pursuit guard is registered before the bash hooks, so a worker's git commit gets the worker refusal, not commit-claims advice (R59). Named test test_worker_git_commit_gets_the_worker_refusal_not_commit_claims_advice passes; suite and ruff pass.
decided by: sh -c 'echo "424bc5a62fed0540b5acad2a3c0c7ad73321b168e2ecd783610cdc8d918cc26b  .beagle/checks/T0474/T0474.sh" | sha256sum -c --quiet && bash .beagle/checks/T0474/T0474.sh'
budget: 150000 tokens
