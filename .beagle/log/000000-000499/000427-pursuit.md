+++
id = "000427-pursuit"
ordinal = 427
kind = "pursuit"
timestamp = "2026-10-04T01:46:00+00:00"
summary = "pursuit prove T0110: WITNESSED — refuses when beagle.py's `return _Proof(proven=False, text=\"\\n\\n\".join(re…` is put back as `return _Proof(proven=False, text=\"\\n\\n\".join(re…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "cc14422ed20cd2a6668cb2b43c66056ffb46880817034cfa35081a8064bb77d3  .beagle/checks/T0110/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0110/check.sh'
refutes: refuses when beagle.py's `return _Proof(proven=False, text="\n\n".join(re…` is put back as `return _Proof(proven=False, text="\n\n".join(re…` (proven 2026-10-04T01:45:11+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_tests_only_witness_in_test_file_names_the_imported_module_an
refused after 1s of a 29s check at: FAILED tests/test_beagle_example_extension.py::test_tests_only_witness_in_test_file_names_the_imported_module_and_is_no…
refused with: 1 failed, 1 passed in 0.78s
