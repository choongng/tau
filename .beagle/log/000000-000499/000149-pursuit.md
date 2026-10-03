+++
id = "000149-pursuit"
ordinal = 149
kind = "pursuit"
timestamp = "2026-10-03T16:22:15+00:00"
summary = "pursuit prove T0050: WITNESSED — refuses when R04.md's `tasks_total 11` is put back as `tasks_total 0`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "08ba37919e13580ce025aca960602b8ec7a48e1becd0ba714791efb43e28a4f9  .beagle/checks/T0050/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0050/check.sh'
refutes: refuses when R04.md's `tasks_total 11` is put back as `tasks_total 0` (proven 2026-10-03T16:21:57+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: dev-notes/itc-runs/R04.md: tasks_total 0 != json 11
