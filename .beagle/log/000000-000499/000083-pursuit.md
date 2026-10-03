+++
id = "000083-pursuit"
ordinal = 83
kind = "pursuit"
timestamp = "2026-10-03T13:03:44+00:00"
summary = "pursuit prove T0035: WITNESSED — refuses when scorecard.py's `if not (dup and dup.group(1) in done):` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3b998d3911452ad8e38b0689fd8fd0fedbdd94239a2e4fbb1ba17ba5e8aaa58d  .beagle/checks/T0035/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0035/check.sh'
refutes: refuses when scorecard.py's `if not (dup and dup.group(1) in done):` is put back as `if False:` (proven 2026-10-03T13:03:35+00:00; refused at Traceback (most recent call last):)
refused after 1s of a 1s check at: Traceback (most recent call last):
refused with: AssertionError: False
standing checks red: T0030
