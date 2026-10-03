+++
id = "000101-pursuit"
ordinal = 101
kind = "pursuit"
timestamp = "2026-10-03T14:20:54+00:00"
summary = "pursuit open T0038: R04 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R04.md holds a trace of the driver session (what happened, by line), failure classes each tagged [tau]/[beagle]/[model] with evidence and an action, and a Disposition line; beagle-side findings are in upstream.md.
decided by: sh -c 'echo "c5a55cc8c7de7f10ad4ce5b8c773f820b1c5c65f6d0de30354d7ccf3ba1c7329  .beagle/checks/T0038/diagnosed.sh" | sha256sum -c --quiet && bash .beagle/checks/T0038/diagnosed.sh R04'
budget: 80000 tokens
