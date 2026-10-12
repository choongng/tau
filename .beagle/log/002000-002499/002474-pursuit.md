+++
id = "002474-pursuit"
ordinal = 2474
kind = "pursuit"
timestamp = "2026-10-12T16:21:39+00:00"
summary = "pursuit prove T0483: WITNESSED — refuses when contract.py's `if second:` is put back as `if False:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6badde3e281f576dc9e42cc49ef13311e9c16d127675c260a00facc61109a021  .beagle/checks/T0483/T0483.sh" | sha256sum -c --quiet && bash .beagle/checks/T0483/T0483.sh'
refutes: refuses when contract.py's `if second:` is put back as `if False:` (proven 2026-10-12T16:20:40+00:00; refused at FAILED tests/test_contract.py::test_brief_keeps_a_second_extraction_from_reading_the_first)
refused after 0s of a 2s check at: FAILED tests/test_contract.py::test_brief_keeps_a_second_extraction_from_reading_the_first
refused with: 1 failed, 3 passed, 30 deselected in 0.20s
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422, T0423, T0424, T0425, T0426, T0336
