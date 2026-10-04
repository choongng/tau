+++
id = "000666-pursuit"
ordinal = 666
kind = "pursuit"
timestamp = "2026-10-04T12:40:47+00:00"
summary = "pursuit prove T0157: WITNESSED — refuses when R18.md's `grader: 0/42 (no implementation on disk: ~/itc …` is put back as `grader: 1/42`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9077cd2c4a1ffc345cf7cf2e17a8b5207430be600178a03d9dbd233aa62ad4ce  .beagle/checks/T0157/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0157/check.sh '"'"'#'"'"' sha256=a54ecfaefa3d219d3c981498e07f35f8cb046633cd53e1174a558c90b3479d56'
refutes: refuses when R18.md's `grader: 0/42 (no implementation on disk: ~/itc …` is put back as `grader: 1/42` (proven 2026-10-04T12:39:52+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: grader line grader: 1/42 != grade.json 0/42
