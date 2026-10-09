+++
id = "001330-pursuit"
ordinal = 1330
kind = "pursuit"
timestamp = "2026-10-09T22:13:46+00:00"
summary = "pursuit prove T0316: NOT-DISCRIMINATING — `sh -c 'echo \"e75161af561d822c2d0af168b5b48d4a8c97bf21fa3b0c4cadba8e07e81cecda  .beagle/checks/T0316/T0316.sh\" | sha256sum -c --quiet && bash .beagle/checks/T0316/T0316.sh'`"
metric_command = ""
drains = []
hooks = []
+++

criteria: R36.md's Tests: lines name tests/test_beagle_example_extension.py, the file that exists, and no longer name tests/test_beagle_extension.py.
measured: still passes with the defect put back in R36.md (exit 0), measured 2026-10-09T22:13:46+00:00
