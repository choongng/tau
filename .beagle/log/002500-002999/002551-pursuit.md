+++
id = "002551-pursuit"
ordinal = 2551
kind = "pursuit"
timestamp = "2026-10-12T20:51:22+00:00"
summary = "pursuit prove T0492: WITNESSED — refuses when eval.md's `| 54/54 | — (baseline` is put back as `| 53/54 | — (baseline`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "5c847f052748fcef8bfe737f0b24190504dc07f3b0dea20efc5bac34cd07644a  .beagle/checks/T0492/T0492.sh" | sha256sum -c --quiet && bash .beagle/checks/T0492/T0492.sh'
refutes: refuses when eval.md's `| 54/54 | — (baseline` is put back as `| 53/54 | — (baseline` (proven 2026-10-12T20:50:26+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: AssertionError: ('B06', '54/54', 'not in eval.md')
standing checks red: T0354
