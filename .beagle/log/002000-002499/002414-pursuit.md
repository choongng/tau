+++
id = "002414-pursuit"
ordinal = 2414
kind = "pursuit"
timestamp = "2026-10-12T14:52:15+00:00"
summary = "pursuit prove T0472: WITNESSED — refuses when beagle.py's `proof_note = _joint_cases_route(check, scope, r…` is put back as `proof_note = proof_note` and beagle.py's `joint = _joint_cases_route(f\"pytest {shlex.quot…` is put back as `joint = \"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c0b40d1031be441b4a4890c7ef9fab7dbed4b70c4eabad174b5b73fe256832c5  .beagle/checks/T0472/T0472.sh" | sha256sum -c --quiet && bash .beagle/checks/T0472/T0472.sh'
refutes: refuses when beagle.py's `proof_note = _joint_cases_route(check, scope, r…` is put back as `proof_note = proof_note` and beagle.py's `joint = _joint_cases_route(f"pytest {shlex.quot…` is put back as `joint = ""` (proven 2026-10-12T14:52:14+00:00; refused at FAILED tests/test_beagle_example_extension
refused after 3s of a 2m47s check at: FAILED tests/test_beagle_example_extension.py::test_tests_only_task_importing_unwritten_module_is_offered_the_cases_fir…
refused with: 2 failed, 820 deselected in 2.88s
