+++
id = "002569-pursuit"
ordinal = 2569
kind = "pursuit"
timestamp = "2026-10-12T21:52:35+00:00"
summary = "pursuit prove T0503: WITNESSED — refuses when contract.py's `return self._shape(first, last, lines) or self.…` is put back as `return \"is not an anchor: copy one from \\`beagl…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f0b70b8052dad06d5ff02d8bcafae17a32f513bd1f9ac05b82f08bc4f173c49e  .beagle/checks/T0503/T0503.sh" | sha256sum -c --quiet && bash .beagle/checks/T0503/T0503.sh'
refutes: refuses when contract.py's `return self._shape(first, last, lines) or self.…` is put back as `return "is not an anchor: copy one from \`beagl…` (proven 2026-10-12T21:51:37+00:00; refused at FAILED tests/test_contract.py::test_contract_bare_line_number_is_refused_with_the_anchor_to_cite)
refused after 1s of a 1s check at: FAILED tests/test_contract.py::test_contract_bare_line_number_is_refused_with_the_anchor_to_cite
refused with: 1 failed, 5 passed, 39 deselected, 1 warning in 0.43s
