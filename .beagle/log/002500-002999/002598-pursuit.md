+++
id = "002598-pursuit"
ordinal = 2598
kind = "pursuit"
timestamp = "2026-10-13T00:31:09+00:00"
summary = "pursuit prove T0508: WITNESSED — refuses when eval.md's `| R82 | q35 | cobs | contract-first fce5dac (an…` is put back as `| R82 | q35 | cobs | contract-first fce5dac (an…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "2bfb637bdd129b2d35d3ec44b9b2896d49a83f0244b862015316c5069401dc57  .beagle/checks/T0508/T0508.sh" | sha256sum -c --quiet && bash .beagle/checks/T0508/T0508.sh'
refutes: refuses when eval.md's `| R82 | q35 | cobs | contract-first fce5dac (an…` is put back as `| R82 | q35 | cobs | contract-first fce5dac (an…` (proven 2026-10-13T00:30:11+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: ('R82', '0/44', 'not in eval.md')
