+++
id = "000799-pursuit"
ordinal = 799
kind = "pursuit"
timestamp = "2026-10-05T00:46:59+00:00"
summary = "pursuit prove T0205: WITNESSED — refuses when beagle.py's `return _run([BEAGLE_BIN, \"pursuit\", *args], roo…` is put back as `return _run([BEAGLE_BIN, \"pursuit\", *args], roo…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "a3a3948093108957cad8dbe1341dfa46f009918ee1043b3d7513c90af2d0aea0  .beagle/checks/T0205/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0205/check.sh'
refutes: refuses when beagle.py's `return _run([BEAGLE_BIN, "pursuit", *args], roo…` is put back as `return _run([BEAGLE_BIN, "pursuit", *args], roo…` (proven 2026-10-05T00:46:39+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_pursuit_runs_beagle_under_the_memory_cap)
refused after 2s of a 1m07s check at: FAILED tests/test_beagle_example_extension.py::test_pursuit_runs_beagle_under_the_memory_cap
refused with: 1 failed in 1.28s
