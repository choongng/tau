+++
id = "001277-pursuit"
ordinal = 1277
kind = "pursuit"
timestamp = "2026-10-09T21:08:37+00:00"
summary = "pursuit prove T0307: WITNESSED — refuses when R36.md's `Seen in: first seen as a reasoning loop (R36, g…` is put back as `first seen as a reasoning loop (R36, gemma, the…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "d8e811a70f2225e2885d40cc367f7398c49efa831ef27f66bf3d0c0b588b67b6  .beagle/checks/T0307/T0307.sh" | sha256sum -c --quiet && bash .beagle/checks/T0307/T0307.sh'
refutes: refuses when R36.md's `Seen in: first seen as a reasoning loop (R36, g…` is put back as `first seen as a reasoning loop (R36, gemma, the…` (proven 2026-10-09T21:08:37+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: classes without 'Seen in:': ### [tau] A driver reasoning loop spends the whole output budget, and the 7th cut-off ends the run
