+++
id = "000166-pursuit"
ordinal = 166
kind = "pursuit"
timestamp = "2026-10-03T16:59:59+00:00"
summary = "pursuit open T0053: R07 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R07.md has a Trace analysis and Failure classes section (each class tagged tau/beagle/model with Evidence and Action/Disposition); upstream.md has an R07 section; every tau Action is filed as a task under T0013
decided by: sh -c 'echo "c5a55cc8c7de7f10ad4ce5b8c773f820b1c5c65f6d0de30354d7ccf3ba1c7329  .beagle/checks/T0053/diagnosed.sh" | sha256sum -c --quiet && bash .beagle/checks/T0053/diagnosed.sh R07'
budget: 40000 tokens
