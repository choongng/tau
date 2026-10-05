+++
id = "000869-pursuit"
ordinal = 869
kind = "pursuit"
timestamp = "2026-10-05T03:54:13+00:00"
summary = "pursuit prove T0220: WITNESSED — refuses when R24.md's `## Trace analysis` is put back as `## Trace notes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "d739c328750fa0ea6d01cb32c0f355cb69f7b244d531d46cb75b6e06a93676a8  .beagle/checks/T0220/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0220/check.sh'
refutes: refuses when R24.md's `## Trace analysis` is put back as `## Trace notes` (proven 2026-10-05T03:53:16+00:00)
refused after 0s of a 0s check
