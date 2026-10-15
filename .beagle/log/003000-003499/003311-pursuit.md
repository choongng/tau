+++
id = "003311-pursuit"
ordinal = 3311
kind = "pursuit"
timestamp = "2026-10-15T14:27:39+00:00"
summary = "pursuit prove T0640: WITNESSED — refuses when beagle.py's `return titles[:60] if len(titles) > 1 else []` is put back as `return []`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_found_first_steer_lists_a_cut_references_numbered_sections'
refutes: refuses when beagle.py's `return titles[:60] if len(titles) > 1 else []` is put back as `return []` (proven 2026-10-15T14:26:39+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_found_first_steer_lists_a_cut_references_numbered_sections)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_found_first_steer_lists_a_cut_references_numbered_sections
refused with: 1 failed, 734 deselected in 0.78s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0086, T0088, T0089, T0226, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
