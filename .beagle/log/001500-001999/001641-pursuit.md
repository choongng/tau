+++
id = "001641-pursuit"
ordinal = 1641
kind = "pursuit"
timestamp = "2026-10-10T20:58:53+00:00"
summary = "pursuit prove T0383: WITNESSED — refuses when beagle.py's `selection = _selected_none(rc, output, check)` is put back as `selection = \"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "4829f1ca1597cc80ebc85794ce8b3e269e85b85dec9ca3efed361d923ce4b025  .beagle/checks/T0383/T0383.sh" | sha256sum -c --quiet && bash .beagle/checks/T0383/T0383.sh'
refutes: refuses when beagle.py's `selection = _selected_none(rc, output, check)` is put back as `selection = ""` (proven 2026-10-10T20:58:52+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_collected_none_note_names_a_k_that_matched_nothing)
refused after 1s of a 1m56s check at: FAILED tests/test_beagle_example_extension.py::test_collected_none_note_names_a_k_that_matched_nothing
refused with: 1 failed, 1 passed, 712 deselected in 0.95s
replaces: refuses when beagle.py's `if unselected:` is put back as `if False and unselected:` (proven 2026-10-10T20:56:54+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_open_refuses_a_check_whose_selection_deselects_every_test)
