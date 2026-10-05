+++
id = "000902-pursuit"
ordinal = 902
kind = "pursuit"
timestamp = "2026-10-05T04:53:10+00:00"
summary = "pursuit prove T0226: WITNESSED — refuses when beagle.py's `if len(lead) + len(call) + len(full) + len(tail…` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "4d0d5fc4090593ac1ae2129d19f363a233dd8571459d9ec9f3f2da2f084f1f16  .beagle/checks/T0226/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0226/check.sh'
refutes: refuses when beagle.py's `if len(lead) + len(call) + len(full) + len(tail…` is put back as `if False:` (proven 2026-10-05T04:53:08+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_unproven_refusal_first_line_is_a_complete_call_within_the_quote)
refused after 3s of a 1m24s check at: FAILED tests/test_beagle_example_extension.py::test_unproven_refusal_first_line_is_a_complete_call_within_the_quote
refused with: 1 failed in 2.27s
