+++
id = "000803-pursuit"
ordinal = 803
kind = "pursuit"
timestamp = "2026-10-05T00:47:25+00:00"
summary = "pursuit open T0206: Cases-test lookup skips the data file's own keys; the data lock carries the cases test"
metric_command = ""
drains = []
hooks = []
+++

criteria: A cases test that subscripts the data file's own top-level key is not refused as looking up an absent case; a known-answers close with explicit locks also locks the changed tests in scope that read the locked data and import the module; Cases first offers to lock a committed cases test instead of a new split, and never plans known answers over locked data.
decided by: sh -c 'echo "e4646eb70aaaddf988aeb7ed8c14ee0994bfa90d0131f6f25e91d173d6339d8e  .beagle/checks/T0206/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0206/check.sh'
budget: 120000 tokens
