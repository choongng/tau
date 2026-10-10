+++
id = "001649-pursuit"
ordinal = 1649
kind = "pursuit"
timestamp = "2026-10-10T21:16:09+00:00"
summary = "pursuit prove T0384: WITNESSED — refuses when beagle.py's `self.cut_fills.append(CUT_CALL if calls else CU…` is put back as `self.cut_fills.append(CUT_REPLY if text else CU…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "929e4abfa25ccf92b7c64de5c7a2400283fdc10cbc52d96e5f524e0a8a342e81  .beagle/checks/T0384/T0384.sh" | sha256sum -c --quiet && bash .beagle/checks/T0384/T0384.sh'
refutes: refuses when beagle.py's `self.cut_fills.append(CUT_CALL if calls else CU…` is put back as `self.cut_fills.append(CUT_REPLY if text else CU…` (proven 2026-10-10T21:16:09+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_cut_off_kill_note_says_write_in_parts_only_for_a_call_argume
refused after 5s of a 2m03s check at: FAILED tests/test_beagle_example_extension.py::test_cut_off_kill_note_says_write_in_parts_only_for_a_call_argument
refused with: 1 failed, 1 passed, 714 deselected in 4.24s
replaces: refuses when beagle.py's `else NO_CALL_CUT` is put back as `else "Split the task or have the notes say to w…` (proven 2026-10-10T21:14:00+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_cut_off_kill_note_names_reply_text_reasoning)
