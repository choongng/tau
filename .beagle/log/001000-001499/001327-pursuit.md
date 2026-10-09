+++
id = "001327-pursuit"
ordinal = 1327
kind = "pursuit"
timestamp = "2026-10-09T22:13:42+00:00"
summary = "pursuit open T0316: Audit 11: R36.md's regression-test names point at the real test file"
metric_command = ""
drains = []
hooks = []
+++

criteria: R36.md's Tests: lines name tests/test_beagle_example_extension.py, the file that exists, and no longer name tests/test_beagle_extension.py.
decided by: sh -c 'echo "e75161af561d822c2d0af168b5b48d4a8c97bf21fa3b0c4cadba8e07e81cecda  .beagle/checks/T0316/T0316.sh" | sha256sum -c --quiet && bash .beagle/checks/T0316/T0316.sh'
budget: 10000 tokens
