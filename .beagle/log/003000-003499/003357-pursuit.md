+++
id = "003357-pursuit"
ordinal = 3357
kind = "pursuit"
timestamp = "2026-10-15T21:49:49+00:00"
summary = "pursuit prove T0650: WITNESSED — refuses when result.json is absent"
metric_command = ""
drains = []
hooks = []
+++

check: /home/choong/tautest/tau/.venv/bin/python -m pytest -q -p no:cacheprovider /home/choong/tautest/itc-harness/test_founding_bench.py
refutes: refuses when result.json is absent (proven 2026-10-15T21:48:50+00:00; refused at FAILED ../itc-harness/test_founding_bench.py::test_the_smoke_founding_recorded_a_graded_result)
refused after 1s of a 1s check at: FAILED ../itc-harness/test_founding_bench.py::test_the_smoke_founding_recorded_a_graded_result
refused with: 1 failed, 2 passed in 0.47s
standing checks red: T0335, T0360, T0386, T0496, T0508, T0526, T0529, T0530, T0537, T0546, T0548, T0574, T0086, T0088, T0089, T0226, T0502, T0505, T0507, T0509, T0519, T0524, T0525, T0536, T0541
