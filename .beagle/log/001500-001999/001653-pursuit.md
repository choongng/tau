+++
id = "001653-pursuit"
ordinal = 1653
kind = "pursuit"
timestamp = "2026-10-10T21:28:29+00:00"
summary = "pursuit prove T0385: WITNESSED — refuses when beagle.py's `if quotable(quoted(at)) and quotable(quoted(aft…` is put back as `if True:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "4db23c9124eb4d53bafd0d7cd788a277efc5643874ba1a5f3c4954328ba94b25  .beagle/checks/T0385/T0385.sh" | sha256sum -c --quiet && bash .beagle/checks/T0385/T0385.sh'
refutes: refuses when beagle.py's `if quotable(quoted(at)) and quotable(quoted(aft…` is put back as `if True:` (proven 2026-10-10T21:28:28+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_source_hold_offers_only_quotes_that_pass_the_rule)
refused after 2s of a 2m02s check at: FAILED tests/test_beagle_example_extension.py::test_source_hold_offers_only_quotes_that_pass_the_rule
refused with: 1 failed, 1 passed, 716 deselected in 1.38s
