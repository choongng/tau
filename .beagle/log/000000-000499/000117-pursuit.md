+++
id = "000117-pursuit"
ordinal = 117
kind = "pursuit"
timestamp = "2026-10-03T14:55:45+00:00"
summary = "pursuit prove T0041: WITNESSED — refuses when beagle.py's `if _named(argv, \"beagle\"): return f\"run `{' '.j…` is put back as `if False: return None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c2aa3516b7b58dfc2edb6150235c06ca9d63b1c11670e97a4dcd530edb2d4605  .beagle/checks/T0041/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0041/check.sh'
refutes: refuses when beagle.py's `if _named(argv, "beagle"): return f"run `{' '.j…` is put back as `if False: return None` (proven 2026-10-03T14:55:32+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_worker_guard_refuses_beagle_commands_and_beagle_reads)
refused after 1s of a 1s check at: FAILED tests/test_beagle_example_extension.py::test_worker_guard_refuses_beagle_commands_and_beagle_reads
refused with: 1 failed, 4 passed, 229 deselected in 0.51s
