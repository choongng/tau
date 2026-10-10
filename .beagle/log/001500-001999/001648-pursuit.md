+++
id = "001648-pursuit"
ordinal = 1648
kind = "pursuit"
timestamp = "2026-10-10T21:14:01+00:00"
summary = "pursuit prove T0384: WITNESSED — refuses when beagle.py's `else NO_CALL_CUT` is put back as `else \"Split the task or have the notes say to w…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "929e4abfa25ccf92b7c64de5c7a2400283fdc10cbc52d96e5f524e0a8a342e81  .beagle/checks/T0384/T0384.sh" | sha256sum -c --quiet && bash .beagle/checks/T0384/T0384.sh'
refutes: refuses when beagle.py's `else NO_CALL_CUT` is put back as `else "Split the task or have the notes say to w…` (proven 2026-10-10T21:14:00+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_cut_off_kill_note_names_reply_text_reasoning)
refused after 5s of a 2m03s check at: FAILED tests/test_beagle_example_extension.py::test_cut_off_kill_note_names_reply_text_reasoning
refused with: 2 failed, 714 deselected in 4.35s
