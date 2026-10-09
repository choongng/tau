+++
id = "001243-pursuit"
ordinal = 1243
kind = "pursuit"
timestamp = "2026-10-09T18:32:35+00:00"
summary = "pursuit open T0295: Harness: gemma4-12b-q4 in the rotation; record the driver's provider, model and thinking level per run"
metric_command = ""
drains = []
hooks = []
+++

criteria: Harness (~/tautest/itc-harness, outside tau): launch.sh accepts gemma -> gemma4-12b-q4 beside mimo and qwen (workers dispatched to the same model), refuses unknown names; its dry run prints 'driver thinking: <level> (sent)' or '(NOT sent: <why>)' from tau's own config resolution (catalog thinking_default/levels/parameter, as provider_thinking_config_warning sees it), and meta.json records provider and driver_thinking {level, sent}. scorecard.py reports driver_thinking_level (from the driver session's thinking_level_change) and driver_reasoning_chars. A new .beagle/checks/runs/v6/{scored.sh,selftest.sh,diagnosed.sh} copies v5 with gemma=gemma4-12b-q4 in the model map; v5 stays unchanged for old rechecks.
decided by: sh -c 'echo "1d1eb64f0efbf4921df6f5c8476857d584d98653caab9c34d6a365fabc71f229  .beagle/checks/T0295/T0295.sh" | sha256sum -c --quiet && bash .beagle/checks/T0295/T0295.sh'
budget: 60000 tokens
