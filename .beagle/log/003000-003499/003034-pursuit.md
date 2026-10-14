+++
id = "003034-pursuit"
ordinal = 3034
kind = "pursuit"
timestamp = "2026-10-14T05:02:19+00:00"
summary = "pursuit prove T0580: WITNESSED — refuses when cli.py's `childenv.child_env())` is put back as `dict(os.environ))`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f7e941ec54345407779e1769c97ec558ec88831b89cc641f6fe44cc56b859392  .beagle/checks/T0580/T0580.sh" | sha256sum -c --quiet && bash .beagle/checks/T0580/T0580.sh'
refutes: refuses when cli.py's `childenv.child_env())` is put back as `dict(os.environ))` (proven 2026-10-14T05:02:18+00:00; refused at 1 failed, 3 passed, 2623 deselected in 1.69s)
refused after 2s of a 1m58s check at: 1 failed, 3 passed, 2623 deselected in 1.69s
refused with: 1 failed, 3 passed, 2623 deselected in 1.69s
