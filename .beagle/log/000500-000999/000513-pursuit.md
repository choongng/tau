+++
id = "000513-pursuit"
ordinal = 513
kind = "pursuit"
timestamp = "2026-10-04T04:19:59+00:00"
summary = "pursuit open T0125: Locked tests restored even when the lock store is rewritten"
metric_command = ""
drains = []
hooks = []
+++

criteria: A locked test changed together with its copy under .beagle/locked (as by a worker's ruff format .) is still restored at close, from the commit that locked it (recorded with its sha256), and the store is rewritten from that commit too. The worker guard refuses ruff format, and ruff check --fix, over . or with no path, naming the paths to give instead.
decided by: sh -c 'echo "970fd38cbf0ded4961d6c81f723a140fab5c82b2dd5c81970a3a3bae78d7062b  .beagle/checks/T0125/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0125/check.sh'
budget: 100000 tokens
