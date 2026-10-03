+++
id = "000074-pursuit"
ordinal = 74
kind = "pursuit"
timestamp = "2026-10-03T13:00:23+00:00"
summary = "pursuit open T0032: R03 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R03.md has a Trace analysis and Failure classes, each tagged with an Action or Disposition line.
decided by: sh -c 'echo "c5a55cc8c7de7f10ad4ce5b8c773f820b1c5c65f6d0de30354d7ccf3ba1c7329  .beagle/checks/T0032/diagnosed.sh" | sha256sum -c --quiet && bash .beagle/checks/T0032/diagnosed.sh R03'
budget: 40000 tokens
