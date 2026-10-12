+++
id = "002239-pursuit"
ordinal = 2239
kind = "pursuit"
timestamp = "2026-10-12T12:12:10+00:00"
summary = "pursuit prove T0424: WITNESSED — refuses when R58.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b686c087471992ed3f4ac26fc70a2f56ac683bbc397225e5903185588b4e1d4c  .beagle/checks/T0424/T0424.sh" | sha256sum -c --quiet && bash .beagle/checks/T0424/T0424.sh'
refutes: refuses when R58.md is absent (proven 2026-10-12T12:11:10+00:00)
refused after 0s of a 1s check
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422
