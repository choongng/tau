+++
id = "000563-pursuit"
ordinal = 563
kind = "pursuit"
timestamp = "2026-10-04T07:28:08+00:00"
summary = "pursuit prove T0135: WITNESSED — refuses when beagle.py's `if not retitled and _read_or_design_only(part):` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9c4f4c7f0a9e6da89db5d6be3287835ee5cd5a5ecfc7a87afcdd44240b06d469  .beagle/checks/T0135/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0135/check.sh'
refutes: refuses when beagle.py's `if not retitled and _read_or_design_only(part):` is put back as `if False:` (proven 2026-10-04T07:27:25+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_founding_read_and_design_milestone_is_retitled_known_answers)
refused after 2s of a 41s check at: FAILED tests/test_beagle_example_extension.py::test_founding_read_and_design_milestone_is_retitled_known_answers
refused with: 1 failed, 1 passed in 1.89s
