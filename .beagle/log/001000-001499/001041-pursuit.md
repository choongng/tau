+++
id = "001041-pursuit"
ordinal = 1041
kind = "pursuit"
timestamp = "2026-10-05T10:47:21+00:00"
summary = "pursuit open T0253: Fix route, title clash and container answer cannot deadlock"
metric_command = ""
drains = []
hooks = []
+++

criteria: The known-answers fix route reuses an existing pending fix leaf instead of offering a clashing part, or gives a unique title; the title clash ignores ancestors/containers of the split task and never tells the driver to work a container; every tau result's first-line call names a workable leaf.
decided by: sh -c 'echo "87768062c88d28a352fe17c9124df05b49bb59e2d5a29d57d8569bdb2e96585b  .beagle/checks/T0253/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0253/check.sh'
budget: 55000 tokens
