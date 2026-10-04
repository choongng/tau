+++
id = "000734-pursuit"
ordinal = 734
kind = "pursuit"
timestamp = "2026-10-04T16:19:43+00:00"
summary = "pursuit open T0171: A locked file cannot sit in a task's scope; a wrong locked test has a known-answers fix route"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_step refuses, at open and at amend, a scope that names a file locked as known answers, saying who locked it and that changes are put back; a task re-opening the known answers (named as fixing them) may hold the locked files and re-locks them at its close; and the put-back notice for a locked test that fails names that route.
decided by: sh -c 'echo "40f2f3ea70b0650b079f1ba8b4f2175863f7fa892642dab54dbcaf80762d43c0  .beagle/checks/T0171/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0171/check.sh'
budget: 50000 tokens
