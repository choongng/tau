+++
id = "001354-pursuit"
ordinal = 1354
kind = "pursuit"
timestamp = "2026-10-09T22:59:31+00:00"
summary = "pursuit open T0324: R37 class 3: a reply that writes a tool call as text gets a bounded follow-up"
metric_command = ""
drains = []
hooks = []
+++

criteria: A reply that ends with stop reason 'stop', has no tool call, and whose text holds chat-template tool-call markup (TEMPLATE_TOOL_CALL_TOKEN) gets a follow-up user message asking for a real tool call and the loop continues; follow-ups are bounded in a row and per run; prose that only names the tag (no function or JSON call after it) gets none.
decided by: sh -c 'echo "253f383f27d63407de4c173c7bc6582eef6790794b5a4f5c4e8af90e5dee6aa3  .beagle/checks/T0324/T0324.sh" | sha256sum -c --quiet && bash .beagle/checks/T0324/T0324.sh'
budget: 80000 tokens
