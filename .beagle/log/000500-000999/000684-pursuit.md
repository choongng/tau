+++
id = "000684-pursuit"
ordinal = 684
kind = "pursuit"
timestamp = "2026-10-04T13:05:07+00:00"
summary = "pursuit open T0161: No abandon of known answers as duplicate of a superseded task; Cases first names cases on disk"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_step refuses to abandon a known-answers task as a duplicate of a task that is neither done nor open (naming the live successor to work instead); and when the known-answers files are on disk uncommitted, the Cases first refusal names them and the route that closes on them instead of ordering a new split.
decided by: sh -c 'echo "c0ce73fbb299fd260361de9a125e80ba9c394737b46bac5d0f79ab4464d77e42  .beagle/checks/T0161/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0161/check.sh'
budget: 50000 tokens
