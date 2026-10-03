+++
id = "000075-pursuit"
ordinal = 75
kind = "pursuit"
timestamp = "2026-10-03T13:00:39+00:00"
summary = "pursuit prove T0032: WITNESSED — refuses when R03.md's `## Failure classes` is put back as `## Failure notes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c5a55cc8c7de7f10ad4ce5b8c773f820b1c5c65f6d0de30354d7ccf3ba1c7329  .beagle/checks/T0032/diagnosed.sh" | sha256sum -c --quiet && bash .beagle/checks/T0032/diagnosed.sh R03'
refutes: refuses when R03.md's `## Failure classes` is put back as `## Failure notes` (proven 2026-10-03T13:00:30+00:00)
refused after 0s of a 0s check
standing checks red: T0030
