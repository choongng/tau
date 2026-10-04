+++
id = "000603-pursuit"
ordinal = 603
kind = "pursuit"
timestamp = "2026-10-04T09:04:36+00:00"
summary = "pursuit open T0144: Plan splits multi-line parts in a multi-part plan"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_plan splits every part that holds two or more non-empty lines into one part per line, in a plan of any number of parts, keeping their order, and drops a rerun-only line from any of them with a note.
decided by: sh -c 'echo "13a22e589e93ec0b5c349a6e94afbd1ae5d0c7e4d8c422e89d8e52e239969067  .beagle/checks/T0144/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0144/check.sh'
budget: 40000 tokens
