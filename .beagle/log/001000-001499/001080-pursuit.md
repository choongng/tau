+++
id = "001080-pursuit"
ordinal = 1080
kind = "pursuit"
timestamp = "2026-10-05T12:08:09+00:00"
summary = "pursuit prove T0259: WITNESSED — refuses when beagle.py's `if any(rel.endswith(\".py\") for rel in witness) …` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3f1f60d3904ddfa94eec7e50868efc3460c8dcfc999abd4ad0197c5a21420445  .beagle/checks/T0259/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0259/check.sh'
refutes: refuses when beagle.py's `if any(rel.endswith(".py") for rel in witness) …` is put back as `if False:` (proven 2026-10-05T12:08:09+00:00; predates the task: the task's change is only tests, and one of them refused; refused at FAILED tests/test_beagle_example_extension.py::test_done_by_import_error_o
refused after 3s of a 1m27s check at: FAILED tests/test_beagle_example_extension.py::test_done_by_import_error_only_witness_is_released
refused with: 1 failed in 2.25s
