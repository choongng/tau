+++
id = "001088-pursuit"
ordinal = 1088
kind = "pursuit"
timestamp = "2026-10-05T13:17:36+00:00"
summary = "pursuit prove T0263: WITNESSED — refuses when R30.md's `## Trace analysis` is put back as `## Trace notes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "03e4b17e32d86d7a591664134c4d570f010068754185c96f81a13b313acafb4a  .beagle/checks/T0263/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0263/check.sh'
refutes: refuses when R30.md's `## Trace analysis` is put back as `## Trace notes` (proven 2026-10-05T13:16:39+00:00)
refused after 0s of a 0s check
