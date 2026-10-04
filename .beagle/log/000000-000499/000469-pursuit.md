+++
id = "000469-pursuit"
ordinal = 469
kind = "pursuit"
timestamp = "2026-10-04T02:52:15+00:00"
summary = "pursuit prove T0119: WITNESSED — refuses when beagle.py's `bound = f\"bash -c {shlex.quote(command)}\"` is put back as `bound = command`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6ca9e58f1711f9a6e23cf8b017597d0fba6d8ace4c9b286dd99272a6b6a82410  .beagle/checks/T0119/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0119/check.sh'
refutes: refuses when beagle.py's `bound = f"bash -c {shlex.quote(command)}"` is put back as `bound = command` (proven 2026-10-04T02:51:26+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_and_chain_of_real_checks_binds_as_bash_c)
refused after 1s of a 31s check at: FAILED tests/test_beagle_example_extension.py::test_and_chain_of_real_checks_binds_as_bash_c
refused with: 1 failed, 3 passed in 0.69s
