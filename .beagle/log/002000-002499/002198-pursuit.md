+++
id = "002198-pursuit"
ordinal = 2198
kind = "pursuit"
timestamp = "2026-10-12T09:50:02+00:00"
summary = "pursuit prove T0462: WITNESSED — refuses when beagle.py's `locks = \"\" if _lean() else \", with locks` is put back as `locks = \"\" if not _lean() else \", with locks`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "e6cfc2eef4e0170e2248307686e9682a3ae8600474ed3aa28fd79c089c3b1a8f  .beagle/checks/T0462/T0462.sh" | sha256sum -c --quiet && bash .beagle/checks/T0462/T0462.sh'
refutes: refuses when beagle.py's `locks = "" if _lean() else ", with locks` is put back as `locks = "" if not _lean() else ", with locks` (proven 2026-10-12T09:50:01+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_lean_uncommitted_note_and_oracle_hints_recommend_no_locks)
refused after 3s of a 2m48s check at: FAILED tests/test_beagle_example_extension.py::test_lean_uncommitted_note_and_oracle_hints_recommend_no_locks
refused with: 1 failed, 810 deselected in 2.79s
