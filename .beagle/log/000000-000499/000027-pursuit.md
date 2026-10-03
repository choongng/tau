+++
id = "000027-pursuit"
ordinal = 27
kind = "pursuit"
timestamp = "2026-10-03T11:00:13+00:00"
summary = "pursuit prove T0019: WITNESSED — refuses when itc_ref.py's `return (n, el, er2), cr + 1 if ir == 0:` is put back as `return (n, el2, er), cr + 1 if ir == 0:`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "0662620b8fe7f816dd1ebf2931bf6b14bb4a80a9c92e29453b48577616efb8de  .beagle/checks/T0019/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0019/check.sh'
refutes: refuses when itc_ref.py's `return (n, el, er2), cr + 1 if ir == 0:` is put back as `return (n, el2, er), cr + 1 if ir == 0:` (proven 2026-10-03T11:00:13+00:00; refused at `== 1. grader accepts the reference ITC and refuses a broken…` (== 1. grader accepts the reference ITC and refuses a broken one))
refused after 0s of a 1s check at: `== 1. grader accepts the reference ITC and refuses a broken…` (== 1. grader accepts the reference ITC and refuses a broken one)
refused with: == 1. grader accepts the reference ITC and refuses a broken one
