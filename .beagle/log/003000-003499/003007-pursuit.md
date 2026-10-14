+++
id = "003007-pursuit"
ordinal = 3007
kind = "pursuit"
timestamp = "2026-10-14T04:21:53+00:00"
summary = "pursuit prove T0577: WITNESSED — refuses when contract.py's `save its text as {REFERENCES}/{name}.txt (beagl…` is put back as `save it as {REFERENCES}/{name}.txt (beagle refs…`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "e7a26ca2e4c79da3b3f0ce29d1bf5b3583a30882f7d464f9c4da3d9228d9be65  .beagle/checks/T0577/T0577.sh" | sha256sum -c --quiet && bash .beagle/checks/T0577/T0577.sh'
refutes: refuses when contract.py's `save its text as {REFERENCES}/{name}.txt (beagl…` is put back as `save it as {REFERENCES}/{name}.txt (beagle refs…` (proven 2026-10-14T04:21:33+00:00; refused at 1 failed, 2616 deselected in 0.76s)
refused after 1s of a 1m09s check at: 1 failed, 2616 deselected in 0.76s
refused with: 1 failed, 2616 deselected in 0.76s
standing checks red: T0335, T0360, T0386, T0496
