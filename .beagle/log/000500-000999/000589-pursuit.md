+++
id = "000589-pursuit"
ordinal = 589
kind = "pursuit"
timestamp = "2026-10-04T08:49:09+00:00"
summary = "pursuit prove T0141: WITNESSED — refuses when beagle.py's `backwards = _plan_order_problem(parts, task, go…` is put back as `backwards = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6e81bf2778b2f8f8267798dc68e5ca20dff8eec17b0af55aec17b0678b08cc07  .beagle/checks/T0141/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0141/check.sh'
refutes: refuses when beagle.py's `backwards = _plan_order_problem(parts, task, go…` is put back as `backwards = None` (proven 2026-10-04T08:48:31+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_plan_refuses_implementation_before_known_answers)
refused after 2s of a 48s check at: FAILED tests/test_beagle_example_extension.py::test_plan_refuses_implementation_before_known_answers
refused with: 1 failed in 1.51s
