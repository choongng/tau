+++
id = "001607-pursuit"
ordinal = 1607
kind = "pursuit"
timestamp = "2026-10-10T18:48:18+00:00"
summary = "pursuit prove T0379: WITNESSED — refuses when scorecard.py's `def loop_cut(m):` is put back as `def loop_cut(m): return False`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "905ce9d88f1343034ce22464ea663f97e4b7368bb8398c7a84b557c8c0a16cb8  .beagle/checks/T0379/T0379.sh" | sha256sum -c --quiet && bash .beagle/checks/T0379/T0379.sh'
refutes: refuses when scorecard.py's `def loop_cut(m):` is put back as `def loop_cut(m): return False` (proven 2026-10-10T18:47:21+00:00; refused at Traceback (most recent call last):)
refused after 1s of a 1s check at: Traceback (most recent call last):
refused with: AssertionError: {'driver': 0, 'workers': 0}
standing checks red: T0368
