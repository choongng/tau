+++
id = "000261-pursuit"
ordinal = 261
kind = "pursuit"
timestamp = "2026-10-03T19:56:30+00:00"
summary = "pursuit open T0066: pursuit_plan refuses a part that only re-runs or confirms a check"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_plan (and founding milestones, if they go through the same repair) refuses, writing nothing, a part whose title and purpose only re-run, confirm or verify a check with nothing to change (R09: 'P5::Re-run the case-data test and confirm exit 0'); the refusal names the part and says a part must change something, the check runs at every close anyway, so fold it into the part before. A part that verifies by writing or adding a test or file ('Add a test that verifies join') is accepted.
decided by: sh -c 'echo "13241b4fed186f29c2b7be151bb8dd6650842358caa02561161528fbd34ceaba  .beagle/checks/T0066/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0066/check.sh'
budget: 40000 tokens
