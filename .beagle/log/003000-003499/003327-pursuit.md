+++
id = "003327-pursuit"
ordinal = 3327
kind = "pursuit"
timestamp = "2026-10-15T16:21:14+00:00"
summary = "pursuit prove T0643: WITNESSED — refuses when beagle.py's `page = source.partition(\"#\")[0]` is put back as `page = source`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k 'test_pursuit_step_reads_a_url_source_with_a_fragment_from_the_page_on_disk'
refutes: refuses when beagle.py's `page = source.partition("#")[0]` is put back as `page = source` (proven 2026-10-15T16:20:16+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_step_reads_a_url_source_with_a_fragment_from_the_page_on_di…)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_step_reads_a_url_source_with_a_fragment_from_the_page_on_di…
refused with: 1 failed, 737 deselected in 0.90s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0086, T0088, T0089, T0226, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
