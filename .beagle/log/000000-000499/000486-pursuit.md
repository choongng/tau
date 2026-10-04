+++
id = "000486-pursuit"
ordinal = 486
kind = "pursuit"
timestamp = "2026-10-04T03:26:27+00:00"
summary = "pursuit prove T0122: WITNESSED — refuses when R14.md's `## Trace analysis` is put back as `## Trace notes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9fbfa60244bfd79635f7fe81227f85ddf0ebbc0e31d9759e64346fc503824ad8  .beagle/checks/T0122/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0122/check.sh'
refutes: refuses when R14.md's `## Trace analysis` is put back as `## Trace notes` (proven 2026-10-04T03:25:37+00:00)
refused after 0s of a 0s check
