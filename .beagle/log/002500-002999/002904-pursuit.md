+++
id = "002904-pursuit"
ordinal = 2904
kind = "pursuit"
timestamp = "2026-10-14T01:42:29+00:00"
summary = "pursuit prove T0558: WITNESSED — refuses when contract.py's `slice_inventory(*slice_kind(title, len(done)))` is put back as `slice_inventory(*slice_kind(title, 0))`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "4f6530038a9890959abc763d4206f646bea8834ccbe1c9b5e989a0351b7ac8ca  .beagle/checks/T0558/T0558.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0558/T0558.v2.sh'
refutes: refuses when contract.py's `slice_inventory(*slice_kind(title, len(done)))` is put back as `slice_inventory(*slice_kind(title, 0))` (proven 2026-10-14T01:42:29+00:00; refused at 1 failed, 75 deselected in 0.57s)
refused after 1s of a 54s check at: 1 failed, 75 deselected in 0.57s
refused with: 1 failed, 75 deselected in 0.57s
