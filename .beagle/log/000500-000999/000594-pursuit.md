+++
id = "000594-pursuit"
ordinal = 594
kind = "pursuit"
timestamp = "2026-10-04T08:56:50+00:00"
summary = "pursuit prove T0142: WITNESSED — refuses when beagle.py's `report, shown = run.report, _capped_report(run)` is put back as `report, shown = run.report, run.shown_report`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "fbeac5d140a38b4899d41c863615cce1b73a17896d648e5893ae420448e16db2  .beagle/checks/T0142/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0142/check.sh'
refutes: refuses when beagle.py's `report, shown = run.report, _capped_report(run)` is put back as `report, shown = run.report, run.shown_report` (proven 2026-10-04T08:56:13+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_not_done_result_caps_last_report)
refused after 2s of a 49s check at: FAILED tests/test_beagle_example_extension.py::test_not_done_result_caps_last_report
refused with: 1 failed, 1 passed in 1.58s
