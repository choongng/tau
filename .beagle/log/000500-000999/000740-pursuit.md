+++
id = "000740-pursuit"
ordinal = 740
kind = "pursuit"
timestamp = "2026-10-04T16:45:58+00:00"
summary = "pursuit prove T0174: WITNESSED — refuses when beagle.py's `return bool(re.search(r\"\\bfix\", head)) and \"kno…` is put back as `return \"known answer\" in head or \"cases\" in head`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "8306fc1588c0256baa5cbf0a0fc88946bad1ea8b1d7839087dde8198790e669c  .beagle/checks/T0174/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0174/check.sh'
refutes: refuses when beagle.py's `return bool(re.search(r"\bfix", head)) and "kno…` is put back as `return "known answer" in head or "cases" in head` (proven 2026-10-04T16:45:33+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_an_implementation_task_naming_the_cases_cannot_hold_a_locked
refused after 2s of a 1m02s check at: FAILED tests/test_beagle_example_extension.py::test_an_implementation_task_naming_the_cases_cannot_hold_a_locked_file
refused with: 1 failed in 1.54s
