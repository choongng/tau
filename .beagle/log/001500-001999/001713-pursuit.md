+++
id = "001713-pursuit"
ordinal = 1713
kind = "pursuit"
timestamp = "2026-10-11T00:20:34+00:00"
summary = "pursuit prove T0396: WITNESSED — refuses when refusals.py's `\"count\": len(rs),` is put back as `\"count\": len(rs) + 1,`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f76d8a88fdddb8708eca07b5adf2d563ae9af5b172f2dd4bad93e6f80164a633  .beagle/checks/T0396/T0396.sh" | sha256sum -c --quiet && bash .beagle/checks/T0396/T0396.sh'
refutes: refuses when refusals.py's `"count": len(rs),` is put back as `"count": len(rs) + 1,` (proven 2026-10-11T00:19:35+00:00; refused at FAILED mine/test_refusals.py::test_main_writes_rows_and_kinds_that_agree - as...)
refused after 0s of a 2s check at: FAILED mine/test_refusals.py::test_main_writes_rows_and_kinds_that_agree - as...
refused with: 1 failed, 7 passed in 0.02s
standing checks red: T0368
