+++
id = "000656-pursuit"
ordinal = 656
kind = "pursuit"
timestamp = "2026-10-04T11:34:28+00:00"
summary = "pursuit prove T0155: WITNESSED — refuses when beagle.py's `retitled = any(_names_known_answers(part) for p…` is put back as `retitled = False`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "0676dbe2192e9e677a290ca24586c989b5a6d458279d94e82f57e7632081f09a  .beagle/checks/T0155/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0155/check.sh'
refutes: refuses when beagle.py's `retitled = any(_names_known_answers(part) for p…` is put back as `retitled = False` (proven 2026-10-04T11:33:57+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_founding_does_not_retitle_when_a_known_answers_milestone_exists)
refused after 2s of a 54s check at: FAILED tests/test_beagle_example_extension.py::test_founding_does_not_retitle_when_a_known_answers_milestone_exists
refused with: 1 failed, 1 passed in 1.41s
