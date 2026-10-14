+++
id = "002870-pursuit"
ordinal = 2870
kind = "pursuit"
timestamp = "2026-10-14T00:45:55+00:00"
summary = "pursuit prove T0558: WITNESSED — refuses when contract.py's `slice_inventory(*slice_kind(title, len(done)))` is put back as `slice_inventory(*slice_kind(title, 0))`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "6401105ad360796b48c045d76c7565c2ddd97ef7b32210d0061c7b4c91bf3cbb  .beagle/checks/T0558/T0558.sh" | sha256sum -c --quiet && bash .beagle/checks/T0558/T0558.sh'
refutes: refuses when contract.py's `slice_inventory(*slice_kind(title, len(done)))` is put back as `slice_inventory(*slice_kind(title, 0))` (proven 2026-10-14T00:45:32+00:00; refused at 1 failed, 75 deselected in 0.55s)
refused after 1s of a 1m04s check at: 1 failed, 75 deselected in 0.55s
refused with: 1 failed, 75 deselected in 0.55s
