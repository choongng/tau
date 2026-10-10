+++
id = "001475-pursuit"
ordinal = 1475
kind = "pursuit"
timestamp = "2026-10-10T03:44:57+00:00"
summary = "pursuit prove T0346: WITNESSED — refuses when R40.md's `Seen in: R34 (qwen` is put back as `Seen in: (qwen`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3eb73ff0510e5b8c5a3e8ebe06127756e751d1c971111b29d87126d1989f858e  .beagle/checks/T0346/T0346.sh" | sha256sum -c --quiet && bash .beagle/checks/T0346/T0346.sh'
refutes: refuses when R40.md's `Seen in: R34 (qwen` is put back as `Seen in: (qwen` (proven 2026-10-10T03:44:01+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: classes without 'Seen in:': ### [tau] The known-answers verdict asks for "the line that gives the result" when the reference has none, and never says to replace the case
standing checks red: T0335
