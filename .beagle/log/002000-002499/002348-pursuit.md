+++
id = "002348-pursuit"
ordinal = 2348
kind = "pursuit"
timestamp = "2026-10-12T14:09:22+00:00"
summary = "pursuit prove T0426: WITNESSED — refuses when R60.md is absent"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "eef1f0b30e25f8093c4e1d7f50ba185c100c7795cc0e3258812c35e1e3fa26b5  .beagle/checks/T0426/T0426.sh" | sha256sum -c --quiet && bash .beagle/checks/T0426/T0426.sh'
refutes: refuses when R60.md is absent (proven 2026-10-12T14:08:24+00:00)
refused after 0s of a 0s check
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422, T0336
