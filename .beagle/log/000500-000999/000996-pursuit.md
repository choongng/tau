+++
id = "000996-pursuit"
ordinal = 996
kind = "pursuit"
timestamp = "2026-10-05T08:11:28+00:00"
summary = "pursuit prove T0246: WITNESSED — refuses when R26.md's `exists; what R26` is put back as `has no infeasible verdict; what R26`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c51f2151584ebdb40f6ca917a6c93f91768d8f16088be56c725f181dfe6c53ab  .beagle/checks/T0246/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0246/check.sh'
refutes: refuses when R26.md's `exists; what R26` is put back as `has no infeasible verdict; what R26` (proven 2026-10-05T08:10:30+00:00; refused at R26.md still says beagle close has no infeasible verdict)
refused after 0s of a 0s check at: R26.md still says beagle close has no infeasible verdict
refused with: R26.md still says beagle close has no infeasible verdict
