+++
id = "000238-pursuit"
ordinal = 238
kind = "pursuit"
timestamp = "2026-10-03T19:49:22+00:00"
summary = "pursuit prove T0064: WITNESSED — refuses when R09.md's `## Trace analysis` is put back as `## Trace notes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c5a55cc8c7de7f10ad4ce5b8c773f820b1c5c65f6d0de30354d7ccf3ba1c7329  .beagle/checks/T0064/diagnosed.sh" | sha256sum -c --quiet && bash .beagle/checks/T0064/diagnosed.sh R09'
refutes: refuses when R09.md's `## Trace analysis` is put back as `## Trace notes` (proven 2026-10-03T19:48:55+00:00)
refused after 0s of a 0s check
