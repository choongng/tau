+++
id = "000278-pursuit"
ordinal = 278
kind = "pursuit"
timestamp = "2026-10-03T20:01:29+00:00"
summary = "pursuit prove T0075: WITNESSED — refuses when scorecard.py's `return \"breaker\" if refusal_kind(text_of(m)) ==…` is put back as `return \"provider\"`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f37f602d157de2ba7ba7806c8e1abbf3f21aa1f0704053001e1d336ee332d282  .beagle/checks/T0075/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0075/check.sh'
refutes: refuses when scorecard.py's `return "breaker" if refusal_kind(text_of(m)) ==…` is put back as `return "provider"` (proven 2026-10-03T20:00:55+00:00; refused at Traceback (most recent call last):)
refused after 1s of a 1s check at: Traceback (most recent call last):
refused with: AssertionError: provider
