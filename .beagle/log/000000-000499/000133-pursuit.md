+++
id = "000133-pursuit"
ordinal = 133
kind = "pursuit"
timestamp = "2026-10-03T15:58:26+00:00"
summary = "pursuit open T0046: R06 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R06.md has a Trace analysis and Failure classes, each class with Evidence and an Action or Disposition; upstream items appended to upstream.md.
decided by: sh -c 'echo "c5a55cc8c7de7f10ad4ce5b8c773f820b1c5c65f6d0de30354d7ccf3ba1c7329  .beagle/checks/T0046/diagnosed.sh" | sha256sum -c --quiet && bash .beagle/checks/T0046/diagnosed.sh R06'
budget: 120000 tokens
