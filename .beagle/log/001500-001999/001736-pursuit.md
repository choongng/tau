+++
id = "001736-pursuit"
ordinal = 1736
kind = "pursuit"
timestamp = "2026-10-11T01:08:53+00:00"
summary = "pursuit open T0404: The driver's bash guards see a bash -c script holding a heredoc, and touch or ln into .beagle"
metric_command = ""
drains = []
hooks = []
+++

criteria: In a founded pursuit, _driver_bash_change names a project write made inside a bash -c '...' script that holds a heredoc (with or without a leading VAR=value prefix), as it already does for bash -c 'echo x > f'; _bash_writes_dot_beagle is true for touch and ln (incl. ln -sf /dev/null) whose target is under .beagle/; a heredoc written under /tmp from the driver still runs. Tests named in the check; whole file passes; ruff clean.
decided by: sh -c 'echo "9878f821ccac470546bb4289e8ac9966493deb7be81207bc5c79c06da97a4fb6  .beagle/checks/T0404/T0404.sh" | sha256sum -c --quiet && bash .beagle/checks/T0404/T0404.sh'
budget: 60000 tokens
