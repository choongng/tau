+++
id = "001529-pursuit"
ordinal = 1529
kind = "pursuit"
timestamp = "2026-10-10T04:52:20+00:00"
summary = "pursuit prove T0355: WITNESSED — refuses when B01.md's `Built: ~/cobs holds` is put back as `Made: ~/cobs holds`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "1236215a8daa330a93cc8d06b081d89be271569e68e54dbc63d4ea9501760071  .beagle/checks/T0355/T0355.sh" | sha256sum -c --quiet && bash .beagle/checks/T0355/T0355.sh'
refutes: refuses when B01.md's `Built: ~/cobs holds` is put back as `Made: ~/cobs holds` (proven 2026-10-10T04:51:22+00:00; refused at B01.md does not say what the run built)
refused after 0s of a 0s check at: B01.md does not say what the run built
refused with: B01.md does not say what the run built
