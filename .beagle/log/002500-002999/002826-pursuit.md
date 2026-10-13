+++
id = "002826-pursuit"
ordinal = 2826
kind = "pursuit"
timestamp = "2026-10-13T21:59:21+00:00"
summary = "pursuit prove T0552: WITNESSED — refuses when incremental-contract.md's `## Build tasks` is put back as `## Tasks`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "04b4bf61461c5c6c03a4d597d2b74b593a1d7ef54a8fde86d8bc0586cec1834b  .beagle/checks/T0552/T0552.sh" | sha256sum -c --quiet && bash .beagle/checks/T0552/T0552.sh'
refutes: refuses when incremental-contract.md's `## Build tasks` is put back as `## Tasks` (proven 2026-10-13T21:58:24+00:00; refused at missing section: ## Build tasks)
refused after 0s of a 0s check at: missing section: ## Build tasks
refused with: missing section: ## Build tasks
standing checks red: T0519
