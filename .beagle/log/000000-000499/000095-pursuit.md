+++
id = "000095-pursuit"
ordinal = 95
kind = "pursuit"
timestamp = "2026-10-03T13:17:34+00:00"
summary = "pursuit prove T0034: WITNESSED — refuses when beagle.py's `f\"{_reference_extract(text)}\\n>>>\"` is put back as `f\"\\n>>>\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "94f973c11df717164bb12f304b86eecd51602b7d9642e1d5781985f3eff0063e  .beagle/checks/T0034/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0034/check.sh'
refutes: refuses when beagle.py's `f"{_reference_extract(text)}\n>>>"` is put back as `f"\n>>>"` (proven 2026-10-03T13:17:25+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_found_first_steer_carries_reference_extracts)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_found_first_steer_carries_reference_extracts
refused with: 1 failed, 2 passed, 217 deselected in 0.49s
