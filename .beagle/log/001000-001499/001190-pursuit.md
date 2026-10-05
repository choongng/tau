+++
id = "001190-pursuit"
ordinal = 1190
kind = "pursuit"
timestamp = "2026-10-05T19:00:07+00:00"
summary = "pursuit open T0283: R34 fix: locked-file scope refusals and nonexistent pytest nodes"
metric_command = ""
drains = []
hooks = []
+++

criteria: The lock refusal leads with the same call minus the locked paths; the open-task call-scope rerun path refuses locked paths the same way; a task whose scope holds the locked known-answers file is recognised as their fix regardless of its title; a done_when naming a pytest node absent from a test file the task cannot write is refused at open, naming the node and the tests that exist. Regression tests for each.
decided by: sh -c 'echo "dabd2d0efcf7da152428bc7e74210e5251dc7e505640761ebe68ef25e58a4dac  .beagle/checks/T0283/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0283/check.sh'
budget: 150000 tokens
