+++
id = "000048-pursuit"
ordinal = 48
kind = "pursuit"
timestamp = "2026-10-03T12:23:56+00:00"
summary = "pursuit prove T0026: WITNESSED — refuses when R02.md's `## Failure classes` is put back as `## Failure notes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c5a55cc8c7de7f10ad4ce5b8c773f820b1c5c65f6d0de30354d7ccf3ba1c7329  .beagle/checks/T0026/diagnosed.sh" | sha256sum -c --quiet && bash .beagle/checks/T0026/diagnosed.sh R02'
refutes: refuses when R02.md's `## Failure classes` is put back as `## Failure notes` (proven 2026-10-03T12:23:53+00:00)
refused after 0s of a 0s check
