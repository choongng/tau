+++
id = "001871-pursuit"
ordinal = 1871
kind = "pursuit"
timestamp = "2026-10-12T00:52:23+00:00"
summary = "pursuit prove T0444: WITNESSED — refuses when beagle.py's `if any(_case_at(first, p) != _case_at(second, p…` is put back as `if routing or True:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "ca99d49d06f201087cd656b71de0e18ae834ecf58f964c52171b58f089579d4a  .beagle/checks/T0444/T0444.sh" | sha256sum -c --quiet && bash .beagle/checks/T0444/T0444.sh'
refutes: refuses when beagle.py's `if any(_case_at(first, p) != _case_at(second, p…` is put back as `if routing or True:` (proven 2026-10-12T00:52:22+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_cases_test_problem_refuses_cases_the_test_cannot_tell_apart)
refused after 3s of a 2m42s check at: FAILED tests/test_beagle_example_extension.py::test_cases_test_problem_refuses_cases_the_test_cannot_tell_apart
refused with: 1 failed, 2 passed, 782 deselected in 3.18s
