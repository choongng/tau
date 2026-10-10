+++
id = "001622-pursuit"
ordinal = 1622
kind = "pursuit"
timestamp = "2026-10-10T19:07:31+00:00"
summary = "pursuit prove T0376: WITNESSED — refuses when beagle.py's `if own_import and await _data_check_passes_comm…` is put back as `if False and await _data_check_passes_committed(`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "1c93246820f76a0322c6db6fa0b2cca55c29e2fe3870b8474a5214ab9090d8cd  .beagle/checks/T0376/T0376.sh" | sha256sum -c --quiet && bash .beagle/checks/T0376/T0376.sh'
refutes: refuses when beagle.py's `if own_import and await _data_check_passes_comm…` is put back as `if False and await _data_check_passes_committed(` (proven 2026-10-10T19:07:31+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_open_task_whose_check_imports_unwritten_module_runs_with_dro
refused after 4s of a 1m55s check at: FAILED tests/test_beagle_example_extension.py::test_open_task_whose_check_imports_unwritten_module_runs_with_drop_impor…
refused with: 1 failed, 1 passed, 708 deselected in 3.59s
