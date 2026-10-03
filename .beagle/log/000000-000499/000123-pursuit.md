+++
id = "000123-pursuit"
ordinal = 123
kind = "pursuit"
timestamp = "2026-10-03T15:28:04+00:00"
summary = "pursuit open T0043: R05 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R05.md has a Trace analysis and Failure classes, each class with Evidence and an Action or Disposition; upstream items appended to upstream.md.
decided by: sh -c 'echo "c5a55cc8c7de7f10ad4ce5b8c773f820b1c5c65f6d0de30354d7ccf3ba1c7329  .beagle/checks/T0043/diagnosed.sh" | sha256sum -c --quiet && bash .beagle/checks/T0043/diagnosed.sh R05'
budget: 20000 tokens
