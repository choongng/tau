+++
id = "003102-pursuit"
ordinal = 3102
kind = "pursuit"
timestamp = "2026-10-14T19:48:27+00:00"
summary = "pursuit prove T0593: WITNESSED — refuses when launch.sh's `TAU_BIN=\"$TAU_SRC/.venv/bin/tau\")` is put back as `)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "be83f5def36127fc8a1d73674333027bb3ca81feffd95748ae86e569ff5dd810  .beagle/checks/T0593/T0593.sh" | sha256sum -c --quiet && bash .beagle/checks/T0593/T0593.sh'
refutes: refuses when launch.sh's `TAU_BIN="$TAU_SRC/.venv/bin/tau")` is put back as `)` (proven 2026-10-14T19:48:27+00:00)
refused after 0s of a 0s check
