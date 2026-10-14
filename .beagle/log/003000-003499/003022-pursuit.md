+++
id = "003022-pursuit"
ordinal = 3022
kind = "pursuit"
timestamp = "2026-10-14T04:32:12+00:00"
summary = "pursuit prove T0319: WITNESSED — refuses when T0319.v2.sh's `if t.endswith(\"T0245.md\") or re.search(r'^retir…` is put back as `if t.endswith(\"T0245.md\"):`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "d5bc793e11244ae9bd1bd27ca26ed421f43c671e83f8add40779fb48f190a27d  .beagle/checks/T0319/T0319.v2.sh" | sha256sum -c --quiet && bash .beagle/checks/T0319/T0319.v2.sh'
refutes: refuses when T0319.v2.sh's `if t.endswith("T0245.md") or re.search(r'^retir…` is put back as `if t.endswith("T0245.md"):` (proven 2026-10-14T04:32:12+00:00; refused at .beagle/checks/T0319/T0319.v2.sh: FAILED)
refused after 0s of a 3s check at: .beagle/checks/T0319/T0319.v2.sh: FAILED
refused with: sha256sum: WARNING: 1 computed checksum did NOT match
