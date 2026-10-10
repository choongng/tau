+++
id = "001457-pursuit"
ordinal = 1457
kind = "pursuit"
timestamp = "2026-10-10T02:44:50+00:00"
summary = "pursuit open T0341: pursuit_step is bounded by one step budget across its attempts"
metric_command = ""
drains = []
hooks = []
+++

criteria: One pursuit_step call is bounded by one step budget across its attempts: a second worker run gets only what remains of it, and is skipped when less than a floor remains, the step then returning the first run's result with a line saying the step's time is spent and to call pursuit_step again. Regression tests in tests/test_beagle_example_extension.py.
decided by: sh -c 'echo "62990b18bed06b0ee70ad89a3b792a165a058fc46115be1c5fb0bd37fea54389  .beagle/checks/T0341/T0341.sh" | sha256sum -c --quiet && bash .beagle/checks/T0341/T0341.sh'
budget: 50000 tokens
