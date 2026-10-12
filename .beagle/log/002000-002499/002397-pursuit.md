+++
id = "002397-pursuit"
ordinal = 2397
kind = "pursuit"
timestamp = "2026-10-12T14:29:59+00:00"
summary = "pursuit prove T0469: WITNESSED — refuses when beagle.py's `notes = (run.last_words if cut_off else report)…` is put back as `notes = report.strip()`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "531259c528771cb45ae7a17c314cc01dea53f2e5d71a328bff6b18119645e3d2  .beagle/checks/T0469/T0469.sh" | sha256sum -c --quiet && bash .beagle/checks/T0469/T0469.sh'
refutes: refuses when beagle.py's `notes = (run.last_words if cut_off else report)…` is put back as `notes = report.strip()` (proven 2026-10-12T14:29:59+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_cut_off_kill_note_is_not_briefed_as_reference_notes)
refused after 4s of a 2m40s check at: FAILED tests/test_beagle_example_extension.py::test_cut_off_kill_note_is_not_briefed_as_reference_notes
refused with: 1 failed, 817 deselected in 3.52s
