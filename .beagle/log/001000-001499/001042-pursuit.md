+++
id = "001042-pursuit"
ordinal = 1042
kind = "pursuit"
timestamp = "2026-10-05T10:58:31+00:00"
summary = "pursuit prove T0253: WITNESSED — refuses when beagle.py's `return [t for t in ids if not _is_container(t, …` is put back as `return list(ids)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "87768062c88d28a352fe17c9124df05b49bb59e2d5a29d57d8569bdb2e96585b  .beagle/checks/T0253/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0253/check.sh'
refutes: refuses when beagle.py's `return [t for t in ids if not _is_container(t, …` is put back as `return list(ids)` (proven 2026-10-05T10:58:30+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_workable_list_never_names_a_container)
refused after 1m24s of a 1m24s check at: FAILED tests/test_beagle_example_extension.py::test_workable_list_never_names_a_container
refused with: 1 failed, 545 passed in 80.89s (0:01:20)
