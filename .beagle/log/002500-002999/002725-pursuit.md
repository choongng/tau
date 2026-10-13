+++
id = "002725-pursuit"
ordinal = 2725
kind = "pursuit"
timestamp = "2026-10-13T19:23:59+00:00"
summary = "pursuit prove T0535: WITNESSED — refuses when beagle.py's `DEFAULT_WORKER_MAX_TURNS = 60` is put back as `DEFAULT_WORKER_MAX_TURNS = 30`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "28130f17713462b774f0c9dc547b5056b3ef621248bbff4e450b24552573dbcd  .beagle/checks/T0535/T0535.sh" | sha256sum -c --quiet && bash .beagle/checks/T0535/T0535.sh'
refutes: refuses when beagle.py's `DEFAULT_WORKER_MAX_TURNS = 60` is put back as `DEFAULT_WORKER_MAX_TURNS = 30` (proven 2026-10-13T19:22:59+00:00)
refused after 0s of a 3s check
