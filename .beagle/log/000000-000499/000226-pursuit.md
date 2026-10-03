+++
id = "000226-pursuit"
ordinal = 226
kind = "pursuit"
timestamp = "2026-10-03T19:40:10+00:00"
summary = "pursuit open T0064: R09 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R09.md has a Trace analysis and Failure classes section (each class tagged tau/beagle/model/harness with Evidence and Action/Disposition); upstream.md has an R09 section; every tau Action is filed as a task under T0013
decided by: sh -c 'echo "c5a55cc8c7de7f10ad4ce5b8c773f820b1c5c65f6d0de30354d7ccf3ba1c7329  .beagle/checks/T0064/diagnosed.sh" | sha256sum -c --quiet && bash .beagle/checks/T0064/diagnosed.sh R09'
budget: 60000 tokens
