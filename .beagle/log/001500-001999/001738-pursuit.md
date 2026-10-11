+++
id = "001738-pursuit"
ordinal = 1738
kind = "pursuit"
timestamp = "2026-10-11T01:21:37+00:00"
summary = "pursuit prove T0404: WITNESSED — refuses when beagle.py's `if any(\".beagle\" in target for target in _comma…` is put back as `if words and words[0] in (\"cp\", \"mv\") and \".bea…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9878f821ccac470546bb4289e8ac9966493deb7be81207bc5c79c06da97a4fb6  .beagle/checks/T0404/T0404.sh" | sha256sum -c --quiet && bash .beagle/checks/T0404/T0404.sh'
refutes: refuses when beagle.py's `if any(".beagle" in target for target in _comma…` is put back as `if words and words[0] in ("cp", "mv") and ".bea…` (proven 2026-10-11T01:21:36+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_bash_writes_dot_beagle_sees_touch_and_ln)
refused after 1s of a 2m10s check at: FAILED tests/test_beagle_example_extension.py::test_bash_writes_dot_beagle_sees_touch_and_ln
refused with: 1 failed, 2 passed, 729 deselected in 0.71s
replaces: refuses when beagle.py's `openers, quote = _heredoc_openers(line, quote)` is put back as `openers, quote = list(_HEREDOC.finditer(line)),…` (proven 2026-10-11T01:19:25+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_driver_bash_change_sees_a_bash_c_heredoc_write)
