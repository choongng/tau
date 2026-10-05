+++
id = "000910-pursuit"
ordinal = 910
kind = "pursuit"
timestamp = "2026-10-05T06:06:28+00:00"
summary = "pursuit prove T0228: WITNESSED — refuses when R25.md's `## Trace analysis` is put back as `## Trace notes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "346f1507d981a265eab3beb9e688bdb44f11d579269309db78df437080794a5e  .beagle/checks/T0228/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0228/check.sh'
refutes: refuses when R25.md's `## Trace analysis` is put back as `## Trace notes` (proven 2026-10-05T06:05:30+00:00)
refused after 0s of a 0s check
