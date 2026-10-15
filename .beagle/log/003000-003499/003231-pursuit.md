+++
id = "003231-pursuit"
ordinal = 3231
kind = "pursuit"
timestamp = "2026-10-15T04:39:55+00:00"
summary = "pursuit prove T0624: WITNESSED — refuses when beagle.py's `a link in the \" \"user's request states:` is put back as `states:`"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py -k test_found_offers_the_requests_link_as_a_milestone_source
refutes: refuses when beagle.py's `a link in the " "user's request states:` is put back as `states:` (proven 2026-10-15T04:38:58+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_found_offers_the_requests_link_as_a_milestone_source)
refused after 3s of a 3s check at: FAILED tests/test_beagle_example_extension.py::test_found_offers_the_requests_link_as_a_milestone_source
refused with: 1 failed, 721 deselected in 2.46s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
