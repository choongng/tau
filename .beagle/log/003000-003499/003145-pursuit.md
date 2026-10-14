+++
id = "003145-pursuit"
ordinal = 3145
kind = "pursuit"
timestamp = "2026-10-14T22:37:11+00:00"
summary = "pursuit prove T0604: WITNESSED — refuses when eval.md's `| S02 | q35 | wrenfold` is put back as `| S2 | q35 | wrenfold`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "8e7c253c39ece2e16818de58811342c96d168b4f652a2e928110c2abbac94432  .beagle/checks/T0604/T0604.sh" | sha256sum -c --quiet && bash .beagle/checks/T0604/T0604.sh'
refutes: refuses when eval.md's `| S02 | q35 | wrenfold` is put back as `| S2 | q35 | wrenfold` (proven 2026-10-14T22:37:11+00:00; refused at fb3823e531f69687396e2aab9dfed559e2fcc1c9)
refused after 0s of a 0s check at: fb3823e531f69687396e2aab9dfed559e2fcc1c9
refused with: fb3823e531f69687396e2aab9dfed559e2fcc1c9
