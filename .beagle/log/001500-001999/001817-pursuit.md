+++
id = "001817-pursuit"
ordinal = 1817
kind = "pursuit"
timestamp = "2026-10-11T22:22:31+00:00"
summary = "pursuit open T0440: Cases-test 'own algorithm' rule does not fire on data-loading helpers"
metric_command = ""
drains = []
hooks = []
+++

criteria: In beagle.py, _cases_test_problem's own-copy verdict (R40: 'checks its own copy of the algorithm') fires only when a module-level function the test defines is called on a case's input and its result is compared with the case's answer. A helper that only loads or iterates the cases data (q35 10-11: _load_cases() then 'for case in _load_cases(): assert "result" in case') does not make a test an own copy, so a data-only test that imports no project module passes this rule. The R40 own-copy test still gets the verdict. Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "779eb2910c0ef353a378b22e74bb8ba29eddc0d5e0099d5f45fa7026fa51d7c4  .beagle/checks/T0440/T0440.sh" | sha256sum -c --quiet && bash .beagle/checks/T0440/T0440.sh'
budget: 300000 tokens
