+++
id = "000047-pursuit"
ordinal = 47
kind = "pursuit"
timestamp = "2026-10-03T12:16:34+00:00"
summary = "pursuit open T0026: R02 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R02.md has a Trace analysis (what the driver and each worker actually did, by turn, with evidence quoted from the sessions) and Failure classes, each tagged tau/beagle/model/harness with an Action or Disposition line; beagle issues are added to upstream.md.
decided by: sh -c 'echo "c5a55cc8c7de7f10ad4ce5b8c773f820b1c5c65f6d0de30354d7ccf3ba1c7329  .beagle/checks/T0026/diagnosed.sh" | sha256sum -c --quiet && bash .beagle/checks/T0026/diagnosed.sh R02'
budget: 150000 tokens
