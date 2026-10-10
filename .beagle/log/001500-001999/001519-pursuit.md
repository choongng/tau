+++
id = "001519-pursuit"
ordinal = 1519
kind = "pursuit"
timestamp = "2026-10-10T04:38:34+00:00"
summary = "pursuit prove T0349: WITNESSED — refuses when beagle.py's `if probe[0] == 0 and not await` is put back as `if probe[0] == 1 and not await`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "cc85ddb9f85be7ba69f5d65819a14ad2c381b7fb738260b4759925aebdf1cc45  .beagle/checks/T0349/T0349.sh" | sha256sum -c --quiet && bash .beagle/checks/T0349/T0349.sh'
refutes: refuses when beagle.py's `if probe[0] == 0 and not await` is put back as `if probe[0] == 1 and not await` (proven 2026-10-10T04:38:34+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_absent_test_kept_when_data_test_already_passes)
refused after 2s of a 1m50s check at: FAILED tests/test_beagle_example_extension.py::test_absent_test_kept_when_data_test_already_passes
refused with: 2 failed, 682 deselected in 1.55s
