+++
id = "002531-pursuit"
ordinal = 2531
kind = "pursuit"
timestamp = "2026-10-12T17:19:27+00:00"
summary = "pursuit prove T0489: WITNESSED — refuses when beagle.py's `seal_note = _seal_when_ready(root) if rc == 0 e…` is put back as `seal_note = \"\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "d23826c6ae37186cb51cc17905a0c805a411e96e6c6dd4628e714128b2cdfb03  .beagle/checks/T0489/T0489.sh" | sha256sum -c --quiet && bash .beagle/checks/T0489/T0489.sh'
refutes: refuses when beagle.py's `seal_note = _seal_when_ready(root) if rc == 0 e…` is put back as `seal_note = ""` (proven 2026-10-12T17:18:31+00:00; refused at FAILED tests/test_beagle_example_extension.py::test_a_close_seals_the_contract_once_beagle_reads_it_ready[ready])
refused after 2s of a 29s check at: FAILED tests/test_beagle_example_extension.py::test_a_close_seals_the_contract_once_beagle_reads_it_ready[ready]
refused with: 2 failed, 4 passed, 826 deselected in 1.70s
