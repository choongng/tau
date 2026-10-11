+++
id = "001844-pursuit"
ordinal = 1844
kind = "pursuit"
timestamp = "2026-10-11T23:13:09+00:00"
summary = "pursuit prove T0437: WITNESSED — refuses when beagle.py's `sources = [rel for rel in sources if os.path.no…` is put back as `pass`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "9871846cb348a4ab3804bdd269daa87f6be769497e4c80d1a2785c504bd1f672  .beagle/checks/T0437/T0437.sh" | sha256sum -c --quiet && bash .beagle/checks/T0437/T0437.sh'
refutes: refuses when beagle.py's `sources = [rel for rel in sources if os.path.no…` is put back as `pass` (proven 2026-10-11T23:13:07+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_absence_fallback_never_takes_away_a_file_the_check_names)
refused after 9s of a 5m17s check at: FAILED tests/test_beagle_example_extension.py::test_absence_fallback_never_takes_away_a_file_the_check_names
refused with: 2 failed, 1 passed, 771 deselected in 7.96s
