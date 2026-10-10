+++
id = "001378-pursuit"
ordinal = 1378
kind = "pursuit"
timestamp = "2026-10-10T00:34:09+00:00"
summary = "pursuit prove T0326: WITNESSED — refuses when R38.md's `Seen in: first seen.` is put back as ``"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b815618e0ecbedd342e419f1ae813b79a362ee4be48ede9a10336c8756d393b0  .beagle/checks/T0326/T0326.sh" | sha256sum -c --quiet && bash .beagle/checks/T0326/T0326.sh'
refutes: refuses when R38.md's `Seen in: first seen.` is put back as `` (proven 2026-10-10T00:33:13+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: classes without 'Seen in:': ### [harness] The run check required a root commit, and an unfounded run has none
