+++
id = "001553-pursuit"
ordinal = 1553
kind = "pursuit"
timestamp = "2026-10-10T15:10:35+00:00"
summary = "pursuit prove T0364: WITNESSED — refuses when beagle.py's `parts.append(_worked_example_note())` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "e32d95097254fb49a82a85cc49621883c55a3f70b8a439726d19f12084127d5a  .beagle/checks/T0364/T0364.sh" | sha256sum -c --quiet && bash .beagle/checks/T0364/T0364.sh'
refutes: refuses when beagle.py's `parts.append(_worked_example_note())` is put back as `pass` (proven 2026-10-10T15:10:34+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_known_answers_brief_has_worked_example)
refused after 1s of a 1m48s check at: FAILED tests/test_beagle_example_extension.py::test_known_answers_brief_has_worked_example
refused with: 1 failed, 1 passed, 692 deselected in 0.97s
