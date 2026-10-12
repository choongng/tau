+++
id = "001926-pursuit"
ordinal = 1926
kind = "pursuit"
timestamp = "2026-10-12T04:27:13+00:00"
summary = "pursuit prove T0449: WITNESSED — refuses when beagle.py's `named = \", \".join(computed[:4]) + (\", …\" if len…` is put back as `named = \", \".join(own[:4]) + (\", …\" if len(own)…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "52859f9c2eff7ec8a70ac814dc32b4b109e8d14b2f5a0e6abbb96e58ae155c10  .beagle/checks/T0449/T0449.sh" | sha256sum -c --quiet && bash .beagle/checks/T0449/T0449.sh'
refutes: refuses when beagle.py's `named = ", ".join(computed[:4]) + (", …" if len…` is put back as `named = ", ".join(own[:4]) + (", …" if len(own)…` (proven 2026-10-12T04:27:12+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_own_copy_refusal_names_only_the_computing_functions)
refused after 3s of a 2m37s check at: FAILED tests/test_beagle_example_extension.py::test_own_copy_refusal_names_only_the_computing_functions
refused with: 1 failed, 795 deselected in 2.94s
