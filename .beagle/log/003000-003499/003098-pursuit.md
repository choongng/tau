+++
id = "003098-pursuit"
ordinal = 3098
kind = "pursuit"
timestamp = "2026-10-14T19:47:55+00:00"
summary = "pursuit open T0593: harness: workers run the dev tau (TAU_BIN defaults to 'tau' on PATH = ~/.local/bin/tau, editable ~/tautest/tau); launch.sh should set TAU_BIN to the harness tau and record it in meta.json"
metric_command = ""
drains = []
hooks = []
+++

criteria: launch.sh sets TAU_BIN to $TAU_SRC/.venv/bin/tau in a pursuit run's env, so workers the extension dispatches run the harness tau; meta.json records tau_bin; launch.sh parses (bash -n)
decided by: sh -c 'echo "be83f5def36127fc8a1d73674333027bb3ca81feffd95748ae86e569ff5dd810  .beagle/checks/T0593/T0593.sh" | sha256sum -c --quiet && bash .beagle/checks/T0593/T0593.sh'
budget: 20000 tokens
opened over T0598: harness work, disjoint from T0599 which a worker holds; the smoke T0604 waits on it
