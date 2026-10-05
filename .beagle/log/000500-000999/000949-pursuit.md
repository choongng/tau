+++
id = "000949-pursuit"
ordinal = 949
kind = "pursuit"
timestamp = "2026-10-05T07:32:28+00:00"
summary = "pursuit prove T0236: WITNESSED — refuses when upstream.md's `## R26` is put back as `## R 26`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "26427f2114014ac5a3ebfdd0f70903f1c508bc4bf98d0d485988f4aa1bc269a8  .beagle/checks/T0236/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0236/check.sh'
refutes: refuses when upstream.md's `## R26` is put back as `## R 26` (proven 2026-10-05T07:31:30+00:00)
refused after 0s of a 0s check
