+++
id = "003381-pursuit"
ordinal = 3381
kind = "pursuit"
timestamp = "2026-10-15T22:35:17+00:00"
summary = "pursuit prove T0632: WITNESSED — refuses when beagle.py's `cut = _SOURCE_IN_INTENT.search(intent)` is put back as `cut = _SOURCE_IN_INTENT.search(target); intent …`"
metric_command = ""
drains = []
hooks = []
+++

check: .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'design_milestone_ahead or part_source or gains_src_code or sourced_layout or spec_tied_writes_cases_then_opens_with_cites_and_cases'
refutes: refuses when beagle.py's `cut = _SOURCE_IN_INTENT.search(intent)` is put back as `cut = _SOURCE_IN_INTENT.search(target); intent …` (proven 2026-10-15T22:34:17+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_founding_folds_a_sourced_layout_milestone_into_the_first_work)
refused after 9s of a 8s check at: FAILED tests/test_beagle_example_extension.py::test_founding_folds_a_sourced_layout_milestone_into_the_first_work
refused with: 2 failed, 4 passed, 741 deselected in 8.41s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0086, T0088, T0089
