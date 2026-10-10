+++
id = "001589-pursuit"
ordinal = 1589
kind = "pursuit"
timestamp = "2026-10-10T17:07:03+00:00"
summary = "pursuit prove T0371: WITNESSED — refuses when scorecard.py's `if w.get(\"cut_off_killed\"): return \"cut_off\"` is put back as ``"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "483710d17ee5bd453bcd6816255d5180671736af782b9072ee03f75ef273f570  .beagle/checks/T0371/T0371.sh" | sha256sum -c --quiet && bash .beagle/checks/T0371/T0371.sh'
refutes: refuses when scorecard.py's `if w.get("cut_off_killed"): return "cut_off"` is put back as `` (proven 2026-10-10T17:06:04+00:00; refused at Traceback (most recent call last):)
refused after 1s of a 1s check at: Traceback (most recent call last):
refused with: AssertionError: 0
standing checks red: T0073, T0077, T0081, T0082, T0085, T0088, T0089, T0057, T0058, T0059, T0065, T0066, T0067, T0068, T0072, T0074, T0083, T0084, T0086, T0087
