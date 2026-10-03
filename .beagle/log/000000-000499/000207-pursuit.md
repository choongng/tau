+++
id = "000207-pursuit"
ordinal = 207
kind = "pursuit"
timestamp = "2026-10-03T18:27:40+00:00"
summary = "pursuit open T0061: refuse a check importing a module neither in scope nor on disk"
metric_command = ""
drains = []
hooks = []
+++

criteria: pursuit_step refuses, before any worker runs, a done_when whose python -c code imports a module of the project (its top-level package is a directory in the project or a scope path starts with it, plain or under src/) when no candidate file for it (X/Y.py, X/Y/__init__.py, also under src/) is in scope or on disk; the text names the expected path(s) and says to put that path in scope or change the import. R08: scope itc/src/interval_tree_clocks.py with check 'from itc.interval_tree_clocks import ...' is refused naming itc/interval_tree_clocks.py. Imports of stdlib or third-party modules, and of project modules that exist or are in scope, are accepted.
decided by: sh -c 'echo "16f5368aa55877cc23c3d548b62a56e25069fbae27033aa8e5be5d489e92bc0e  .beagle/checks/T0061/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0061/check.sh'
budget: 50000 tokens
