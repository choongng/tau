+++
id = "002719-pursuit"
ordinal = 2719
kind = "pursuit"
timestamp = "2026-10-13T19:14:22+00:00"
summary = "pursuit open T0535: tau ext: worker turn cap 30 -> 60"
metric_command = ""
drains = []
hooks = []
+++

criteria: DEFAULT_WORKER_MAX_TURNS is 60; the worker argv test expects 60 by default; the brief's turn note scales from it
decided by: sh -c 'echo "28130f17713462b774f0c9dc547b5056b3ef621248bbff4e450b24552573dbcd  .beagle/checks/T0535/T0535.sh" | sha256sum -c --quiet && bash .beagle/checks/T0535/T0535.sh'
budget: 60000 tokens
