+++
id = "000053-pursuit"
ordinal = 53
kind = "pursuit"
timestamp = "2026-10-03T12:25:28+00:00"
summary = "pursuit prove T0030: WITNESSED — refuses when scorecard.py's `card[\"ended_with_abandoned\"] = ended_with_aband…` is put back as `card[\"ended_with_abandoned\"] = None`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f7f52e5047785b6d7d8426418544b28363d96416166677601580db757b86fe22  .beagle/checks/T0030/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0030/check.sh'
refutes: refuses when scorecard.py's `card["ended_with_abandoned"] = ended_with_aband…` is put back as `card["ended_with_abandoned"] = None` (proven 2026-10-03T12:25:24+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 1s check at: Traceback (most recent call last):
refused with: AssertionError: None
