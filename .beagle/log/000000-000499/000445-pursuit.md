+++
id = "000445-pursuit"
ordinal = 445
kind = "pursuit"
timestamp = "2026-10-04T02:02:11+00:00"
summary = "pursuit open T0113: cases first: refuse opening a new source module before a known-answers test imports it"
metric_command = ""
drains = []
hooks = []
+++

criteria: (a) When the project has a references/ directory, pursuit_step refuses to open a task whose scope names a new (absent at HEAD) non-test Python source module while no locked test file imports that module by name; the refusal says 'Cases first', says how to add the known-answers milestone and names the module a locked test imports when there is one. A scope naming the module a locked cases test imports is opened. Without references/ the gate is off. (b) _check_problem refuses a python3 -c json.load done_when whose only assertions are key/in checks, saying a key check passes on any content. Named tests pass, extension test file passes, ruff clean.
decided by: sh -c 'echo "7d0d0bdfd4a9c18f858dff6091149e7ffafe91d37bf18eca479de414adec449f  .beagle/checks/T0113/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0113/check.sh'
budget: 150000 tokens
