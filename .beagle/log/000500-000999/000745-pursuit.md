+++
id = "000745-pursuit"
ordinal = 745
kind = "pursuit"
timestamp = "2026-10-04T16:53:20+00:00"
summary = "pursuit prove T0172: WITNESSED — refuses when beagle.py's `if _scratch_like(rel):` is put back as `if True:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "0256985607393205445e8803d75719bb5ba90c13eb995856342ed54e2303ba8e  .beagle/checks/T0172/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0172/check.sh'
refutes: refuses when beagle.py's `if _scratch_like(rel):` is put back as `if True:` (proven 2026-10-04T16:52:55+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_scope_refusal_of_project_code_does_not_point_to_tmp)
refused after 2s of a 1m02s check at: FAILED tests/test_beagle_example_extension.py::test_scope_refusal_of_project_code_does_not_point_to_tmp
refused with: 1 failed in 1.58s
