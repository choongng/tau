+++
id = "002141-pursuit"
ordinal = 2141
kind = "pursuit"
timestamp = "2026-10-12T09:21:11+00:00"
summary = "pursuit open T0458: Under lean, no driver text promises locks (R55)"
metric_command = ""
drains = []
hooks = []
+++

criteria: Under BEAGLE_TAU_LEAN no driver text promises locks; texts unchanged with lean off, and fixed at extension load so no prefix changes mid-session (R55). Named test test_lean_switch_drops_lock_promises_from_driver_texts passes; suite and ruff pass.
decided by: sh -c 'echo "6ccc0a33f7d284742a65e140e75e7448b6b4329507ef7c9109542a616b8dae8c  .beagle/checks/T0458/T0458.sh" | sha256sum -c --quiet && bash .beagle/checks/T0458/T0458.sh'
budget: 150000 tokens
