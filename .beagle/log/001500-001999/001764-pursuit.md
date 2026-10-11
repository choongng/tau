+++
id = "001764-pursuit"
ordinal = 1764
kind = "pursuit"
timestamp = "2026-10-11T02:16:20+00:00"
summary = "pursuit prove T0408: WITNESSED — refuses when beagle.py's `if existing and holder is not None and _at_spaw…` is put back as `if existing and holder is not None and _at_spaw…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c22dba1730bbd956814a4f17dd2feb3a18bbca57002842bf1d13d29c14725006  .beagle/checks/T0408/T0408.sh" | sha256sum -c --quiet && bash .beagle/checks/T0408/T0408.sh'
refutes: refuses when beagle.py's `if existing and holder is not None and _at_spaw…` is put back as `if existing and holder is not None and _at_spaw…` (proven 2026-10-11T02:16:19+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_cases_first_offers_the_infeasible_close_for_a_holder_at_the_
refused after 3s of a 2m12s check at: FAILED tests/test_beagle_example_extension.py::test_cases_first_offers_the_infeasible_close_for_a_holder_at_the_spawn_l…
refused with: 1 failed, 1 passed, 743 deselected in 2.62s
