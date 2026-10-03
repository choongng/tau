+++
id = "000317-pursuit"
ordinal = 317
kind = "pursuit"
timestamp = "2026-10-03T20:23:35+00:00"
summary = "pursuit prove T0073: WITNESSED — refuses when beagle.py's `if self.stopped:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "1ffa47c5e7cc5de8211cc132b1bf20c475019ee98b32715ba6ecfe412a6b5447  .beagle/checks/T0073/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0073/check.sh'
refutes: refuses when beagle.py's `if self.stopped:` is put back as `if False:` (proven 2026-10-03T20:22:57+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_stopped_by_the_breaker_reports_the_refused_call)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_worker_stopped_by_the_breaker_reports_the_refused_call
refused with: 1 failed, 280 deselected in 0.45s
