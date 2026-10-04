+++
id = "000568-pursuit"
ordinal = 568
kind = "pursuit"
timestamp = "2026-10-04T07:36:44+00:00"
summary = "pursuit prove T0136: WITNESSED — refuses when beagle.py's `report = _report_before_markup(events.report, c…` is put back as `report = events.final_report(stderr)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "b3d97eeaa103d44de6f434173b5e6c0ddf7510ecdbfe586e9c013e66e779159b  .beagle/checks/T0136/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0136/check.sh'
refutes: refuses when beagle.py's `report = _report_before_markup(events.report, c…` is put back as `report = events.final_report(stderr)` (proven 2026-10-04T07:36:15+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_report_ending_in_a_raw_tool_call_keeps_the_text_before_it)
refused after 8s of a 51s check at: FAILED tests/test_beagle_example_extension.py::test_report_ending_in_a_raw_tool_call_keeps_the_text_before_it
refused with: 1 failed, 2 passed in 7.83s
