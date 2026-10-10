+++
id = "001446-pursuit"
ordinal = 1446
kind = "pursuit"
timestamp = "2026-10-10T02:38:34+00:00"
summary = "pursuit prove T0343: WITNESSED — refuses when scorecard.py's `if w[\"stopped_by_refusals\"]: return \"refusals\"` is put back as `if False: return \"refusals\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "31598f802db9cff7992c852730e7c1ab9e54baa42038c8fe4c2b371ad013fcab  .beagle/checks/T0343/T0343.sh" | sha256sum -c --quiet && bash .beagle/checks/T0343/T0343.sh'
refutes: refuses when scorecard.py's `if w["stopped_by_refusals"]: return "refusals"` is put back as `if False: return "refusals"` (proven 2026-10-10T02:37:38+00:00; refused at Traceback (most recent call last):)
refused after 1s of a 1s check at: Traceback (most recent call last):
refused with: AssertionError: R39: timed_out/wall/refusals/cap [6, 5, 0, 1] != [6, 1, 4, 1]
standing checks red: T0335, T0324, T0330
