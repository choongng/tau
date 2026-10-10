+++
id = "001467-pursuit"
ordinal = 1467
kind = "pursuit"
timestamp = "2026-10-10T03:04:17+00:00"
summary = "pursuit prove T0344: WITNESSED — refuses when test_beagle_example_extension.py's `monkeypatch.setattr(_module(), \"BEAGLE_BIN\", st…` is put back as ``"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "2dd1043bba3ef6fb88147f8cedd01be5f5df005245c60e84ec24d0e647486fc2  .beagle/checks/T0344/T0344.sh" | sha256sum -c --quiet && bash .beagle/checks/T0344/T0344.sh'
refutes: refuses when test_beagle_example_extension.py's `monkeypatch.setattr(_module(), "BEAGLE_BIN", st…` is put back as `` (proven 2026-10-10T03:04:17+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_stop_gate_founded_session_gets_no_unfounded_followup)
refused after 3s of a 1m46s check at: FAILED tests/test_beagle_example_extension.py::test_stop_gate_founded_session_gets_no_unfounded_followup
refused with: 1 failed, 1 passed in 2.60s
