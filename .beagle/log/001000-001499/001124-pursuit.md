+++
id = "001124-pursuit"
ordinal = 1124
kind = "pursuit"
timestamp = "2026-10-05T14:25:10+00:00"
summary = "pursuit open T0269: Cut-off advice keeps generator scripts out of scope; helpers left in scope reported; heredoc store reads guarded"
metric_command = ""
drains = []
hooks = []
+++

criteria: The cut-off (truncated write) advice that offers a script says to run it inline (python3 - <<'EOF') or from a scratch path outside the project, never saved in scope; the step result after a worker run names a new untracked .py in scope that no test imports and the check does not name as a helper left in scope; the worker .beagle/ guard also reads heredoc bodies fed to python/python3 - and refuses a store read there.
decided by: sh -c 'echo "16fbc9bd0e64d7648ed0f285d34e6cce90a05e3f3d564bf310e3e1786e89a553  .beagle/checks/T0269/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0269/check.sh'
budget: 60000 tokens
