+++
id = "000960-pursuit"
ordinal = 960
kind = "pursuit"
timestamp = "2026-10-05T07:33:13+00:00"
summary = "pursuit open T0241: Compaction leaves headroom"
metric_command = ""
drains = []
hooks = []
+++

criteria: After an automatic compaction the estimated context (system prompt, tools, summary and kept tail, by the estimator the threshold uses) is at most half the auto-compact threshold, keeping at least the last exchange; tested with a kept tail the current cut would leave over that.
decided by: sh -c 'echo "b7803d8738f5d0f78bbaceade8352b878e8330f1141b7b25ccc5a0937bd71f37  .beagle/checks/T0241/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0241/check.sh'
budget: 60000 tokens
