+++
id = "002831-pursuit"
ordinal = 2831
kind = "pursuit"
timestamp = "2026-10-13T23:07:31+00:00"
summary = "pursuit prove T0550: WITNESSED — refuses when beagle.py's `or os.path.normpath(how[1]) in {os.path.normpat…` is put back as `or False`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "94ef83db90e1546a47c362a1aed7206e8ea39ce24e03d6f2c9fb441b2cdb25ec  .beagle/checks/T0550/T0550.sh" | sha256sum -c --quiet && bash .beagle/checks/T0550/T0550.sh'
refutes: refuses when beagle.py's `or os.path.normpath(how[1]) in {os.path.normpat…` is put back as `or False` (proven 2026-10-13T23:06:34+00:00; refused at 1 failed, 859 deselected in 1.32s)
refused after 2s of a 1s check at: 1 failed, 859 deselected in 1.32s
refused with: 1 failed, 859 deselected in 1.32s
standing checks red: T0519
