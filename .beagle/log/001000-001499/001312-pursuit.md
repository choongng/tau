+++
id = "001312-pursuit"
ordinal = 1312
kind = "pursuit"
timestamp = "2026-10-09T21:46:40+00:00"
summary = "pursuit prove T0312: WITNESSED — refuses when beagle.py's `whole = whole_tree and os.path.normpath(rel or …` is put back as `whole = False`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "52abacf178e8e15b208c41d7c157ff09aede915d0f66e2fcb02c126f2ce099a8  .beagle/checks/T0312/T0312.sh" | sha256sum -c --quiet && bash .beagle/checks/T0312/T0312.sh'
refutes: refuses when beagle.py's `whole = whole_tree and os.path.normpath(rel or …` is put back as `whole = False` (proven 2026-10-09T21:46:39+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_cases_first_refuses_whole_tree_scope_on_known_answers_task)
refused after 3s of a 1m40s check at: FAILED tests/test_beagle_example_extension.py::test_cases_first_refuses_whole_tree_scope_on_known_answers_task
refused with: 1 failed in 2.37s
