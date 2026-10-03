+++
id = "000333-pursuit"
ordinal = 333
kind = "pursuit"
timestamp = "2026-10-03T20:36:02+00:00"
summary = "pursuit open T0080: R10 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/R10.md has ## Trace analysis and ## Failure classes (each class tagged [tau]/[model]/[harness], with evidence by session line and an Action naming code where it is a tau class); upstream.md has an ## R10 section.
decided by: sh -c 'echo "c5a55cc8c7de7f10ad4ce5b8c773f820b1c5c65f6d0de30354d7ccf3ba1c7329  .beagle/checks/T0080/diagnosed.sh" | sha256sum -c --quiet && bash .beagle/checks/T0080/diagnosed.sh R10'
budget: 60000 tokens
