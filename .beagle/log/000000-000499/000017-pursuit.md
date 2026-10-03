+++
id = "000017-pursuit"
ordinal = 17
kind = "pursuit"
timestamp = "2026-10-03T09:54:58+00:00"
summary = "pursuit prove T0019: WITNESSED — refuses when itc_ref.py's `return (n, el, er2), cr + 1 if ir == 0:` is put back as `return (n, el2, er), cr + 1 if ir == 0:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "3a28c8d0249cdabe922453391482fb6628dd51634f770ff284cd8d552dcbfac4  .beagle/checks/T0019/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0019/check.sh'
refutes: refuses when itc_ref.py's `return (n, el, er2), cr + 1 if ir == 0:` is put back as `return (n, el2, er), cr + 1 if ir == 0:` (proven 2026-10-03T09:54:58+00:00; refused at `== 1. grader accepts the reference ITC and refuses a broken…` (== 1. grader accepts the reference ITC and refuses a broken one))
refused after 0s of a 1s check at: `== 1. grader accepts the reference ITC and refuses a broken…` (== 1. grader accepts the reference ITC and refuses a broken one)
refused with: == 1. grader accepts the reference ITC and refuses a broken one
