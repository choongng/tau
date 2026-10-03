+++
id = "000180-pursuit"
ordinal = 180
kind = "pursuit"
timestamp = "2026-10-03T18:16:49+00:00"
summary = "pursuit prove T0056: WITNESSED — refuses when R08.md's `## Failure classes` is put back as `## Classes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c5a55cc8c7de7f10ad4ce5b8c773f820b1c5c65f6d0de30354d7ccf3ba1c7329  .beagle/checks/T0056/diagnosed.sh" | sha256sum -c --quiet && bash .beagle/checks/T0056/diagnosed.sh R08'
refutes: refuses when R08.md's `## Failure classes` is put back as `## Classes` (proven 2026-10-03T18:16:26+00:00)
refused after 0s of a 0s check
