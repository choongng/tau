+++
id = "002608-pursuit"
ordinal = 2608
kind = "pursuit"
timestamp = "2026-10-13T00:50:02+00:00"
summary = "pursuit prove T0514: WITNESSED — refuses when contract.py's `if listing: # The second extraction: what is pi…` is put back as `if kind`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "73da4578b85e6a20f7a47b7ef6895b1b5f37c09ed7a0a1f9b804ddc651fe2541  .beagle/checks/T0514/T0514.sh" | sha256sum -c --quiet && bash .beagle/checks/T0514/T0514.sh'
refutes: refuses when contract.py's `if listing: # The second extraction: what is pi…` is put back as `if kind` (proven 2026-10-13T00:49:04+00:00; refused at - contract/contract.second.json does not exist yet)
refused after 0s of a 3s check at: - contract/contract.second.json does not exist yet
refused with: - contract/contract.second.json does not exist yet
