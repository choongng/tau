+++
id = "000685-pursuit"
ordinal = 685
kind = "pursuit"
timestamp = "2026-10-04T13:11:00+00:00"
summary = "pursuit prove T0161: WITNESSED — refuses when beagle.py's `stale = _stale_known_answers_duplicate(task, wh…` is put back as `stale = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c0ce73fbb299fd260361de9a125e80ba9c394737b46bac5d0f79ab4464d77e42  .beagle/checks/T0161/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0161/check.sh'
refutes: refuses when beagle.py's `stale = _stale_known_answers_duplicate(task, wh…` is put back as `stale = None` (proven 2026-10-04T13:10:33+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_abandon_of_a_known_answers_successor_as_duplicate_of_a_superseded_t…)
refused after 2s of a 1m00s check at: FAILED tests/test_beagle_example_extension.py::test_abandon_of_a_known_answers_successor_as_duplicate_of_a_superseded_t…
refused with: 1 failed in 1.41s
