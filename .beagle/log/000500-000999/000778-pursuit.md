+++
id = "000778-pursuit"
ordinal = 778
kind = "pursuit"
timestamp = "2026-10-04T23:11:27+00:00"
summary = "pursuit prove T0200: WITNESSED — refuses when beagle.py's `return [rel for rel in _check_data_reads(comman…` is put back as `return []`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "fd33b528309957f934a8d6a456d13ec354a49007ac45be2dc1180d7afafc770a  .beagle/checks/T0200/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0200/check.sh'
refutes: refuses when beagle.py's `return [rel for rel in _check_data_reads(comman…` is put back as `return []` (proven 2026-10-04T23:11:04+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_proof_note_for_a_data_test_scoped_without_its_data_names_the_data_f…)
refused after 2s of a 1m04s check at: FAILED tests/test_beagle_example_extension.py::test_proof_note_for_a_data_test_scoped_without_its_data_names_the_data_f…
refused with: 1 failed, 2 passed in 1.80s
