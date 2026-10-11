+++
id = "001733-pursuit"
ordinal = 1733
kind = "pursuit"
timestamp = "2026-10-11T01:08:33+00:00"
summary = "pursuit prove T0399: WITNESSED — refuses when findings.py's `if len(rows) < OFFERED_MIN:` is put back as `if len(rows) <= OFFERED_MIN:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "eafefcc5dd630cebe1defab8842656db26a48e1db1cad4b90bbdc57658969d2c  .beagle/checks/T0399/T0399b.sh" | sha256sum -c --quiet && bash .beagle/checks/T0399/T0399b.sh'
refutes: refuses when findings.py's `if len(rows) < OFFERED_MIN:` is put back as `if len(rows) <= OFFERED_MIN:` (proven 2026-10-11T01:07:33+00:00; refused at FAILED mine/test_findings.py::test_rules_pick_pairs_seen_twice_and_stretches_over_their_minimum)
refused after 0s of a 3s check at: FAILED mine/test_findings.py::test_rules_pick_pairs_seen_twice_and_stretches_over_their_minimum
refused with: 2 failed, 3 passed in 0.02s
standing checks red: T0368
