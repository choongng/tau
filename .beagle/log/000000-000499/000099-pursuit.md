+++
id = "000099-pursuit"
ordinal = 99
kind = "pursuit"
timestamp = "2026-10-03T14:20:45+00:00"
summary = "pursuit prove T0037: WITNESSED — refuses when R04.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "78f588778dd8afbfcad14f30a9e028cf43167afc74f644cdb1764504f6549eb6  .beagle/checks/T0037/scored.sh" | sha256sum -c --quiet && bash .beagle/checks/T0037/scored.sh R04'
refutes: refuses when R04.md is absent (proven 2026-10-03T14:20:35+00:00)
refused after 0s of a 0s check
