+++
id = "000660-pursuit"
ordinal = 660
kind = "pursuit"
timestamp = "2026-10-04T11:43:36+00:00"
summary = "pursuit prove T0156: NOT-DISCRIMINATING — `sh -c 'echo \"58a69bca34a7c2d6b2a65ed70ff2edb53faf616b49402b66cd7665ed3429b98b  .beagle/checks/T0156/check.sh\" | sha256sum -c --quiet && bash .beagle/checks/T0156/check.sh'`"
metric_command = ""
drains = []
hooks = []
+++

criteria: A test copies R15's full cases file (all 32 cases from ~/itc.r15/tests/cases.json) and the reference lines it quotes as fixtures, and asserts every case counts as quoting the reference.
measured: still passes with the defect put back in test_beagle_example_extension.py (exit 0), measured 2026-10-04T11:43:36+00:00
