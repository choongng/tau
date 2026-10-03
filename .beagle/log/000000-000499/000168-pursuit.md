+++
id = "000168-pursuit"
ordinal = 168
kind = "pursuit"
timestamp = "2026-10-03T17:01:02+00:00"
summary = "pursuit prove T0053: WITNESSED — refuses when R07.md's `## Trace analysis` is put back as `## Notes`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "c5a55cc8c7de7f10ad4ce5b8c773f820b1c5c65f6d0de30354d7ccf3ba1c7329  .beagle/checks/T0053/diagnosed.sh" | sha256sum -c --quiet && bash .beagle/checks/T0053/diagnosed.sh R07'
refutes: refuses when R07.md's `## Trace analysis` is put back as `## Notes` (proven 2026-10-03T17:00:38+00:00)
refused after 0s of a 0s check
replaces: still passes with the defect put back in R07.md (exit 0), measured 2026-10-03T17:00:34+00:00
