+++
id = "003046-pursuit"
ordinal = 3046
kind = "pursuit"
timestamp = "2026-10-14T06:00:41+00:00"
summary = "pursuit prove T0582: WITNESSED — refuses when contract.py's `if _slug(bare(op)) not in bounded]` is put back as `if False]`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "db33143e31029074c4ccc257d2b8d9099f688837f2ed1a6cb83e0aae3dfea64c  .beagle/checks/T0582/T0582.sh" | sha256sum -c --quiet && bash .beagle/checks/T0582/T0582.sh'
refutes: refuses when contract.py's `if _slug(bare(op)) not in bounded]` is put back as `if False]` (proven 2026-10-14T06:00:40+00:00; refused at 2 failed, 2627 deselected in 0.72s)
refused after 1s of a 3m58s check at: 2 failed, 2627 deselected in 0.72s
refused with: 2 failed, 2627 deselected in 0.72s
