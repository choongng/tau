+++
id = "003056-pursuit"
ordinal = 3056
kind = "pursuit"
timestamp = "2026-10-14T06:11:57+00:00"
summary = "pursuit prove T0583: WITNESSED — refuses when contract.py's `if any(op == b or op.endswith(f\"-{b}\") for b in…` is put back as `if True:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "7c7058443c0d8680f66fd719f8d4f8fd0197e3a9685c2614222449d178edef93  .beagle/checks/T0583/T0583.sh" | sha256sum -c --quiet && bash .beagle/checks/T0583/T0583.sh'
refutes: refuses when contract.py's `if any(op == b or op.endswith(f"-{b}") for b in…` is put back as `if True:` (proven 2026-10-14T06:11:56+00:00; refused at 1 failed, 2 passed, 2629 deselected in 0.79s)
refused after 1s of a 2m03s check at: 1 failed, 2 passed, 2629 deselected in 0.79s
refused with: 1 failed, 2 passed, 2629 deselected in 0.79s
