+++
id = "000646-pursuit"
ordinal = 646
kind = "pursuit"
timestamp = "2026-10-04T11:20:33+00:00"
summary = "pursuit open T0153: Report path claims checked against disk"
metric_command = ""
drains = []
hooks = []
+++

criteria: A step result and a retry note list each project path a worker report names as written that is not on disk; and a report that names no project path and is under a few hundred characters is not carried into the retry note as notes.
decided by: sh -c 'echo "db248df389b5b6b7218017b3de8bd9823d7f70700b2302c3c2f9fff4e092506e  .beagle/checks/T0153/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0153/check.sh'
budget: 50000 tokens
