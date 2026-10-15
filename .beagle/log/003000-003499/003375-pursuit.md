+++
id = "003375-pursuit"
ordinal = 3375
kind = "pursuit"
timestamp = "2026-10-15T22:27:38+00:00"
summary = "pursuit prove T0655: WITNESSED — refuses when beagle.py's `part, source = _source_in_part(part, root)` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'milestone_source or placeholder or milestone_part'
refutes: refuses when beagle.py's `part, source = _source_in_part(part, root)` is put back as `pass` (proven 2026-10-15T22:26:39+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_a_link_or_reference_written_in_a_milestone_part_becomes_its_source)
refused after 3s of a 3s check at: FAILED tests/test_beagle_example_extension.py::test_a_link_or_reference_written_in_a_milestone_part_becomes_its_source
refused with: 1 failed, 6 passed, 737 deselected in 2.82s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0086, T0088, T0089, T0226, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
