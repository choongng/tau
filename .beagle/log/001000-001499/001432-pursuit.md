+++
id = "001432-pursuit"
ordinal = 1432
kind = "pursuit"
timestamp = "2026-10-10T02:30:21+00:00"
summary = "pursuit amend T0319"
metric_command = ""
drains = []
hooks = []
+++

the first version scanned every script under .beagle/checks, including the unbound check.sh copies that amend leaves behind; it now reads only the scripts tasks bind (done_when) and the checks they call
was: sh -c 'echo "f48b30bb76595ae0a8702ff72f94982c4082517c69c829a4c7bd91cd2c45e743  .beagle/checks/T0319/T0319.sh" | sha256sum -c --quiet && bash .beagle/checks/T0319/T0319.sh'
  f48b30bb76595ae0a8702ff72f94982c4082517c69c829a4c7bd91cd2c45e743  .beagle/checks/T0319/T0319.sh
now: sh -c 'echo "559a1b62b9bd06ff4d92ff1cfe4c9339a03575679c8f9db00f338ff5b7ef1af4  .beagle/checks/T0319/T0319.sh" | sha256sum -c --quiet && bash .beagle/checks/T0319/T0319.sh'
