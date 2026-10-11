+++
id = "001709-pursuit"
ordinal = 1709
kind = "pursuit"
timestamp = "2026-10-11T00:18:48+00:00"
summary = "pursuit prove T0392: WITNESSED — refuses when beagle.py's `if rc == 124 or _pytest_collected_none(rc, chec…` is put back as `if True:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "83977452e07bb62f66fb41574df5ffb1f1533f67ef68c6d1f9843148ec149d68  .beagle/checks/T0392/T0392.sh" | sha256sum -c --quiet && bash .beagle/checks/T0392/T0392.sh'
refutes: refuses when beagle.py's `if rc == 124 or _pytest_collected_none(rc, chec…` is put back as `if True:` (proven 2026-10-11T00:18:47+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_retry_note_omits_fix_the_work_when_the_output_names_no_failure)
refused after 2s of a 2m11s check at: FAILED tests/test_beagle_example_extension.py::test_retry_note_omits_fix_the_work_when_the_output_names_no_failure
refused with: 1 failed, 2 passed, 725 deselected in 1.23s
replaces: refuses when beagle.py's `return bool(bound) and _check_problem(bound) is…` is put back as `return bool(bound) and _check_problem(bound) is…` (proven 2026-10-11T00:16:34+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_kept_bound_note_refuses_an_inverted_bound_check)
