+++
id = "000795-pursuit"
ordinal = 795
kind = "pursuit"
timestamp = "2026-10-05T00:37:26+00:00"
summary = "pursuit prove T0204: WITNESSED — refuses when R22.md's `## Trace analysis` is put back as `## Trace notes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9b5101bb8d8cea253e7d169d6db33b86b8f3dee174026f778d2a9af6d92acb61  .beagle/checks/T0204/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0204/check.sh'
refutes: refuses when R22.md's `## Trace analysis` is put back as `## Trace notes` (proven 2026-10-05T00:36:29+00:00)
refused after 0s of a 0s check
