+++
id = "001743-pursuit"
ordinal = 1743
kind = "pursuit"
timestamp = "2026-10-11T01:35:38+00:00"
summary = "pursuit prove T0403: WITNESSED — refuses when beagle.py's `refusals[rel] = refusals.get(rel, 0) + 1` is put back as `refusals[rel] = refusals.get(rel, 0)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "edfdac420835ae307d4d4e8b8f7461f0247886b4417b7421141be2a9d9240d9b  .beagle/checks/T0403/T0403.sh" | sha256sum -c --quiet && bash .beagle/checks/T0403/T0403.sh'
refutes: refuses when beagle.py's `refusals[rel] = refusals.get(rel, 0) + 1` is put back as `refusals[rel] = refusals.get(rel, 0)` (proven 2026-10-11T01:35:37+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_scope_refusal_of_a_path_refused_before_counts_and_sends_to_report)
refused after 3s of a 2m11s check at: FAILED tests/test_beagle_example_extension.py::test_scope_refusal_of_a_path_refused_before_counts_and_sends_to_report
refused with: 2 failed, 1 passed, 732 deselected in 2.79s
