+++
id = "000024-pursuit"
ordinal = 24
kind = "pursuit"
timestamp = "2026-10-03T10:59:50+00:00"
summary = "pursuit prove T0021: WITNESSED — refuses when R01.md's `## Failure classes` is put back as `## Failure list`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c5a55cc8c7de7f10ad4ce5b8c773f820b1c5c65f6d0de30354d7ccf3ba1c7329  .beagle/checks/T0021/diagnosed.sh" | sha256sum -c --quiet && bash .beagle/checks/T0021/diagnosed.sh R01'
refutes: refuses when R01.md's `## Failure classes` is put back as `## Failure list` (proven 2026-10-03T10:59:50+00:00)
refused after 0s of a 0s check
standing checks red: T0019
