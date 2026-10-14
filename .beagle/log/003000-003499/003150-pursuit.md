+++
id = "003150-pursuit"
ordinal = 3150
kind = "pursuit"
timestamp = "2026-10-14T22:50:25+00:00"
summary = "pursuit prove T0609: WITNESSED — refuses when beagle.py's `if not cases_scope:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "15f4e067ff4bc59074734e3d90bb9de45e3b458f27bb7f9e119c0c508df962a9  .beagle/checks/T0609/T0609.sh" | sha256sum -c --quiet && bash .beagle/checks/T0609/T0609.sh'
refutes: refuses when beagle.py's `if not cases_scope:` is put back as `if False:` (proven 2026-10-14T22:50:25+00:00)
refused after 2s of a 3m24s check
