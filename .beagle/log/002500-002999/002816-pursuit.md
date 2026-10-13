+++
id = "002816-pursuit"
ordinal = 2816
kind = "pursuit"
timestamp = "2026-10-13T21:47:29+00:00"
summary = "pursuit prove T0549: WITNESSED — refuses when discriminate-recon.md's `## Recommendation` is put back as `## Proposal`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c29d6f4ba5c6ad6c92d0cfa9b18cc93f90840a3f2e0a9142c0168b577954519e  .beagle/checks/T0549/T0549.sh" | sha256sum -c --quiet && bash .beagle/checks/T0549/T0549.sh'
refutes: refuses when discriminate-recon.md's `## Recommendation` is put back as `## Proposal` (proven 2026-10-13T21:46:32+00:00; refused at missing section: ## Recommendation)
refused after 0s of a 0s check at: missing section: ## Recommendation
refused with: missing section: ## Recommendation
standing checks red: T0519
