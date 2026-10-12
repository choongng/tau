+++
id = "002541-pursuit"
ordinal = 2541
kind = "pursuit"
timestamp = "2026-10-12T17:37:36+00:00"
summary = "pursuit prove T0491: WITNESSED — refuses when wrenfold_ref.py's `return value < (1 << bits) and not (tag == 0 an…` is put back as `return value < (1 << bits)`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "774c9c5a24e6eb665829dc1b352687ecfc4642106f28288eeb5160a76b543661  .beagle/checks/T0491/T0491.sh" | sha256sum -c --quiet && bash .beagle/checks/T0491/T0491.sh'
refutes: refuses when wrenfold_ref.py's `return value < (1 << bits) and not (tag == 0 an…` is put back as `return value < (1 << bits)` (proven 2026-10-12T17:36:38+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 1s check at: Traceback (most recent call last):
refused with: AssertionError: (1, 49, 54, {'boundary', 'count', 'roundtrip'})
