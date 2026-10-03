+++
id = "000077-pursuit"
ordinal = 77
kind = "pursuit"
timestamp = "2026-10-03T13:02:39+00:00"
summary = "pursuit open T0036: Audit fix: test that thinking off reaches the openai-compatible payload as enable_thinking false"
metric_command = ""
drains = []
hooks = []
+++

criteria: A test shows the openai-compatible provider with thinking_format qwen-chat-template and reasoning_effort 'none' (what --thinking off maps to via the catalog) sends chat_template_kwargs.enable_thinking false and no reasoning_effort; and the user catalog maps both bane 9B models' off level to 'none' with thinkingFormat qwen-chat-template.
decided by: sh -c 'echo "d9ed3d4ad4b3a8f8cb4e6834f001e7f41f1bb8cb3581e9886c15c8094270e5e7  .beagle/checks/T0036/check.sh" | sha256sum -c --quiet && bash .beagle/checks/T0036/check.sh'
budget: 30000 tokens
