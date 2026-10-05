+++
id = "001149-pursuit"
ordinal = 1149
kind = "pursuit"
timestamp = "2026-10-05T16:11:30+00:00"
summary = "pursuit prove T0274: WITNESSED — refuses when beagle.py's `brief += _last_close_note((str(root), task))` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "655b5da655bebfca944ce58b9023800585ac6c3e4ed773261108fa4b79d9ca04  .beagle/checks/T0274/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0274/check.sh'
refutes: refuses when beagle.py's `brief += _last_close_note((str(root), task))` is put back as `pass` (proven 2026-10-05T16:11:30+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_rerun_after_stays_open_close_brief_carries_reason)
refused after 2s of a 1m39s check at: FAILED tests/test_beagle_example_extension.py::test_rerun_after_stays_open_close_brief_carries_reason
refused with: 1 failed in 2.19s
