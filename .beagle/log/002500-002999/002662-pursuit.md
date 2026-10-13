+++
id = "002662-pursuit"
ordinal = 2662
kind = "pursuit"
timestamp = "2026-10-13T06:13:52+00:00"
summary = "pursuit prove T0523: WITNESSED — refuses when README.md's `2562 tests, and seventeen blocking gates` is put back as `2561 tests, and seventeen blocking gates`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "efc6f520edd04445c565c2dc45e5ca675b97288d90361ab066918767ea230641  .beagle/checks/T0523/T0523.sh" | sha256sum -c --quiet && bash .beagle/checks/T0523/T0523.sh'
refutes: refuses when README.md's `2562 tests, and seventeen blocking gates` is put back as `2561 tests, and seventeen blocking gates` (proven 2026-10-13T06:13:49+00:00; refused at ci: FAILED — see above)
refused after 1m41s of a 1m51s check at: ci: FAILED — see above
refused with: ci/check.sh exited 1
