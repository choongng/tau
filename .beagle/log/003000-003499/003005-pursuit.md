+++
id = "003005-pursuit"
ordinal = 3005
kind = "pursuit"
timestamp = "2026-10-14T04:20:40+00:00"
summary = "pursuit prove T0245: WITNESSED — refuses when R26.md's `upstream: beagle's `close --outcome infeasible|…` is put back as `upstream: beagle's spawn refusal at the attempt…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c51f2151584ebdb40f6ca917a6c93f91768d8f16088be56c725f181dfe6c53ab  .beagle/checks/T0245/T0245.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0245/T0245.v2.sh'
refutes: refuses when R26.md's `upstream: beagle's `close --outcome infeasible|…` is put back as `upstream: beagle's spawn refusal at the attempt…` (proven 2026-10-14T04:20:40+00:00; refused at R26.md still says beagle close has no infeasible verdict)
refused after 0s of a 0s check at: R26.md still says beagle close has no infeasible verdict
refused with: R26.md still says beagle close has no infeasible verdict
