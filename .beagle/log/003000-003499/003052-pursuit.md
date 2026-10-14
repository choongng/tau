+++
id = "003052-pursuit"
ordinal = 3052
kind = "pursuit"
timestamp = "2026-10-14T06:06:59+00:00"
summary = "pursuit prove T0585: WITNESSED — refuses when r98-time-recon.md's `Decision:` is put back as `Decided:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "fe9c8c781edfe8af4e9d96e26f0b2587eb04a2ecc44b2b0e5dc51fd5ff0ad77e  .beagle/checks/T0585/T0585.sh" | sha256sum -c --quiet && bash .beagle/checks/T0585/T0585.sh'
refutes: refuses when r98-time-recon.md's `Decision:` is put back as `Decided:` (proven 2026-10-14T06:06:58+00:00)
refused after 0s of a 0s check
