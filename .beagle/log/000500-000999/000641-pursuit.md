+++
id = "000641-pursuit"
ordinal = 641
kind = "pursuit"
timestamp = "2026-10-04T11:12:04+00:00"
summary = "pursuit open T0152: Close refuses a missing lock; prove takes data away"
metric_command = ""
drains = []
hooks = []
+++

criteria: A done close is refused (not-done, nothing committed) when any lock entry of the task is not a file on disk; and for a task with locks, the fallback witness in _prove takes away the locked data files rather than source files.
decided by: sh -c 'echo "08fd4778ce686b59d2ed9388162510f39da00a56401ab4af7f6e3f25132b762b  .beagle/checks/T0152/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0152/check.sh'
budget: 50000 tokens
