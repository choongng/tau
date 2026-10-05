+++
id = "001023-pursuit"
ordinal = 1023
kind = "pursuit"
timestamp = "2026-10-05T09:51:30+00:00"
summary = "pursuit prove T0249: WITNESSED — refuses when beagle.py's `Write it in parts of at most {len(text) // 2} c…` is put back as `Write it in parts of a few hundred lines:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b8ccd49b995c6a42a5027614593f5472b747c813e58a0bb204adc7aaa7d6e246  .beagle/checks/T0249/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0249/check.sh'
refutes: refuses when beagle.py's `Write it in parts of at most {len(text) // 2} c…` is put back as `Write it in parts of a few hundred lines:` (proven 2026-10-05T09:51:29+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_truncated_call_names_char_budget)
refused after 2s of a 1m28s check at: FAILED tests/test_beagle_example_extension.py::test_truncated_call_names_char_budget
refused with: 1 failed in 2.07s
