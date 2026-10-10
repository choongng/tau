+++
id = "001416-pursuit"
ordinal = 1416
kind = "pursuit"
timestamp = "2026-10-10T02:20:08+00:00"
summary = "pursuit prove T0337: WITNESSED — refuses when R38.md's `upstream: see upstream.md ## R38.` is put back as `upstream: none.`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "717f80bae7b4392eca7fafee5cb44c619c6b11e95b6b0325b0918a2339e6178b  .beagle/checks/T0337/T0337.sh" | sha256sum -c --quiet && bash .beagle/checks/T0337/T0337.sh'
refutes: refuses when R38.md's `upstream: see upstream.md ## R38.` is put back as `upstream: none.` (proven 2026-10-10T02:19:09+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: R38.md still says upstream: none
