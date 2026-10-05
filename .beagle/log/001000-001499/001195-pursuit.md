+++
id = "001195-pursuit"
ordinal = 1195
kind = "pursuit"
timestamp = "2026-10-05T19:25:06+00:00"
summary = "pursuit prove T0284: WITNESSED — refuses when beagle.py's `return not any(_renders_result(text, result) fo…` is put back as `return False`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "da99bc5d876d6106bca32f328394147ada805fcc103d03dd7d56d55c9a849460  .beagle/checks/T0284/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0284/check.sh'
refutes: refuses when beagle.py's `return not any(_renders_result(text, result) fo…` is put back as `return False` (proven 2026-10-05T19:25:05+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_known_answer_source_must_hold_expected_result)
refused after 3s of a 1m37s check at: FAILED tests/test_beagle_example_extension.py::test_known_answer_source_must_hold_expected_result
refused with: 1 failed in 2.60s
