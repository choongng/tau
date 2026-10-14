+++
id = "003135-pursuit"
ordinal = 3135
kind = "pursuit"
timestamp = "2026-10-14T21:50:10+00:00"
summary = "pursuit prove T0601: WITNESSED — refuses when beagle.py's `argv += [\"--cites\", *case_cites, \"--cases\", *ca…` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a1fad247eac13b5142c39437d295a468ad26b47e8d80f8caad6c79cdfae60666  .beagle/checks/T0601/T0601.sh" | sha256sum -c --quiet && bash .beagle/checks/T0601/T0601.sh'
refutes: refuses when beagle.py's `argv += ["--cites", *case_cites, "--cases", *ca…` is put back as `pass` (proven 2026-10-14T21:50:10+00:00)
refused after 0s of a 3m20s check
