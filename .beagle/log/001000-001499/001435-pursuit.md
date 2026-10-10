+++
id = "001435-pursuit"
ordinal = 1435
kind = "pursuit"
timestamp = "2026-10-10T02:33:17+00:00"
summary = "pursuit prove T0333: WITNESSED — refuses when R39.md's `Seen in: R30 (qwen: W4's encoder never advanced…` is put back as `Seen in R30 (qwen: W4's encoder never advanced …`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "87bab758d1afdcfaa059714577bf737ba256a8c03006cae437a2419dcda369a2  .beagle/checks/T0333/T0333.sh" | sha256sum -c --quiet && bash .beagle/checks/T0333/T0333.sh'
refutes: refuses when R39.md's `Seen in: R30 (qwen: W4's encoder never advanced…` is put back as `Seen in R30 (qwen: W4's encoder never advanced …` (proven 2026-10-10T02:32:20+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: classes without 'Seen in:': ### [tau] A hanging check reaches the worker only as "timed out after 120 seconds … pass a larger `timeout`", because the brief's `timeout 540` outlasts the worker's 120 s bash default
standing checks red: T0335
