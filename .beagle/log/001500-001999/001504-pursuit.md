+++
id = "001504-pursuit"
ordinal = 1504
kind = "pursuit"
timestamp = "2026-10-10T04:09:29+00:00"
summary = "pursuit open T0354: Baseline launch mode"
metric_command = ""
drains = []
hooks = []
+++

criteria: launch.sh accepts run ids B01... as baselines: tau -p --no-extensions on prompts/TASK_baseline_prompt.txt (the TASK prompt without the beagle setup and pursuit-run instructions, links kept), with the same provider, model, cap, memory and driver thinking as R runs; R runs are unchanged. The dry-run says the mode, and meta.json records mode baseline or pursuit.
decided by: sh -c 'echo "42b7cb294dc2113ee3a7f5d70b1505c186456cd0753f56d2739fdacc8a59a624  .beagle/checks/T0354/T0354.sh" | sha256sum -c --quiet && bash .beagle/checks/T0354/T0354.sh'
budget: 20000 tokens
opened over T0349, T0350, T0351: harness-only, disjoint from T0359's tau scope
