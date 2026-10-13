+++
id = "002607-pursuit"
ordinal = 2607
kind = "pursuit"
timestamp = "2026-10-13T00:48:55+00:00"
summary = "pursuit open T0514: beagle contract: the second extraction lists what the sources pin (operation and anchor per example, limit and invalid input), not full entries; beagle compares anchors with the contract"
metric_command = ""
drains = []
hooks = []
+++

criteria: The declared second extraction is a listing: each entry is held to its id, kind, operation, source and cite (checked against the source as before), and not to an input, expect or statement, and its operations need nothing to exercise them; contract add --file on it takes such entries; the contract itself still refuses them; the full check still names a listed passage the contract does not cite. beagle's second-extraction brief and tau's Second extraction milestone and CONTRACT_FIRST_NOTE say so. beagle CI green, tau extension suite green. (Work was begun before this open: the check was written after; prove shows it refuses.)
decided by: sh -c 'echo "73da4578b85e6a20f7a47b7ef6895b1b5f37c09ed7a0a1f9b804ddc651fe2541  .beagle/checks/T0514/T0514.sh" | sha256sum -c --quiet && bash .beagle/checks/T0514/T0514.sh'
budget: 60000 tokens
opened over T0493: the owner chose ideas 1 and 2 (contract-stage cost) first, 10-12
