+++
id = "002132-pursuit"
ordinal = 2132
kind = "pursuit"
timestamp = "2026-10-12T09:17:26+00:00"
summary = "pursuit prove T0456: WITNESSED — refuses when beagle.py's `rest = [entry for entry in scope if not _holds_…` is put back as `rest = list(scope)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "2a984a64a85225afd666a8f3d1b53197a8a6e4cc058ca013f22f0fd37b188450  .beagle/checks/T0456/T0456.sh" | sha256sum -c --quiet && bash .beagle/checks/T0456/T0456.sh'
refutes: refuses when beagle.py's `rest = [entry for entry in scope if not _holds_…` is put back as `rest = list(scope)` (proven 2026-10-12T09:17:25+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_locked_test_refusal_for_a_lint_check_offers_a_scope_without_the_jud…)
refused after 3s of a 2m44s check at: FAILED tests/test_beagle_example_extension.py::test_locked_test_refusal_for_a_lint_check_offers_a_scope_without_the_jud…
refused with: 1 failed, 803 deselected in 2.99s
