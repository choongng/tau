+++
id = "002372-pursuit"
ordinal = 2372
kind = "pursuit"
timestamp = "2026-10-12T14:15:42+00:00"
summary = "pursuit prove T0464: WITNESSED — refuses when beagle.py's `else NO_CALL_CUT_ONLY if events.calls else NO_C…` is put back as `else NO_CALL_CUT` and beagle.py's `self.calls += len(calls)` is put back as `` and beagle.py's `\"reported\" if reported else \"ended without a re…` is put back as `\"reported\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "06a8fa96767ffc996b3cdca1d1406437e92202d32a7c3769f977f186f5e7e1ef  .beagle/checks/T0464/T0464.sh" | sha256sum -c --quiet && bash .beagle/checks/T0464/T0464.sh'
refutes: refuses when beagle.py's `else NO_CALL_CUT_ONLY if events.calls else NO_C…` is put back as `else NO_CALL_CUT` and beagle.py's `self.calls += len(calls)` is put back as `` and beagle.py's `"reported" if reported else "ended without a re…` is put back as `"reported"` (proven 2026-10-12T14:15:41+00:00;
refused after 4s of a 2m41s check at: FAILED tests/test_beagle_example_extension.py::test_cut_off_kill_note_omits_without_acting_when_the_worker_made_calls
refused with: 1 failed, 813 deselected in 4.06s
