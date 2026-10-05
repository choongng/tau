+++
id = "001133-pursuit"
ordinal = 1133
kind = "pursuit"
timestamp = "2026-10-05T15:40:14+00:00"
summary = "pursuit prove T0272: WITNESSED — refuses when R32.md's `## Trace analysis` is put back as `## Trace notes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "03771a398341c04c50a9c4d2867caa267d3984270a0e651ded8c8b0a1a9f1f25  .beagle/checks/T0272/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0272/check.sh'
refutes: refuses when R32.md's `## Trace analysis` is put back as `## Trace notes` (proven 2026-10-05T15:39:17+00:00)
refused after 0s of a 0s check
