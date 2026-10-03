+++
id = "000022-pursuit"
ordinal = 22
kind = "pursuit"
timestamp = "2026-10-03T10:56:08+00:00"
summary = "pursuit open T0021: R01 diagnose"
metric_command = ""
drains = []
hooks = []
+++

criteria: R01.md gains a Trace analysis (timeline of the driver and both workers: what each turn tried, where time went, why no task was stepped in 58 min) and Failure classes, each '### [tau|beagle|model|harness] <name>' with evidence (session line/timestamps) and an 'Action:' or 'Disposition:' line proposing a concrete fix site in tau (src path + mechanism) or why none. Beagle-side items also appended to upstream.md.
decided by: sh -c 'echo "c5a55cc8c7de7f10ad4ce5b8c773f820b1c5c65f6d0de30354d7ccf3ba1c7329  .beagle/checks/T0021/diagnosed.sh" | sha256sum -c --quiet && bash .beagle/checks/T0021/diagnosed.sh R01'
budget: 150000 tokens
