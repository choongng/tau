+++
id = "002790-pursuit"
ordinal = 2790
kind = "pursuit"
timestamp = "2026-10-13T20:38:50+00:00"
summary = "pursuit prove T0544: WITNESSED — refuses when dispute-recon.md's `## Who judges it` is put back as `## Who decides`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c4753345852b016afe21b3351d886e7f7074567c8f1cfbf57fdaad379c92f645  .beagle/checks/T0544/T0544.sh" | sha256sum -c --quiet && bash .beagle/checks/T0544/T0544.sh'
refutes: refuses when dispute-recon.md's `## Who judges it` is put back as `## Who decides` (proven 2026-10-13T20:37:50+00:00; refused at missing section: ## Who judges it)
refused after 0s of a 0s check at: missing section: ## Who judges it
refused with: missing section: ## Who judges it
