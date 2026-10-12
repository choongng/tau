+++
id = "002202-pursuit"
ordinal = 2202
kind = "pursuit"
timestamp = "2026-10-12T11:06:05+00:00"
summary = "pursuit prove T0423: WITNESSED — refuses when R57.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f57e98e96349c67c3a950f3f0e718337ca1b7cc8f646fa8ee6b6d6c0b82fce6c  .beagle/checks/T0423/T0423.sh" | sha256sum -c --quiet && bash .beagle/checks/T0423/T0423.sh'
refutes: refuses when R57.md is absent (proven 2026-10-12T11:05:06+00:00)
refused after 0s of a 0s check
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422
