+++
id = "001439-pursuit"
ordinal = 1439
kind = "pursuit"
timestamp = "2026-10-10T02:34:24+00:00"
summary = "pursuit open T0338: Template-token leak in an optional argument: run the clean call, not refuse it"
metric_command = ""
drains = []
hooks = []
+++

criteria: When a tool call's leaked chat-template tool-call tokens sit only in arguments the tool does not require (R39: bash's description), session.py cuts each such argument at the first token and runs the call, and the result says the tail was dropped and to send each call separately; a leak inside a required argument stays refused, and that refusal names the clean prefix as the call to send. Regression tests in tests/test_session_template_tokens.py.
decided by: sh -c 'echo "2959040c5899a55336b14e84bc7da6e65831d9b7f326ac577cef0890bc99e15a  .beagle/checks/T0338/T0338.sh" | sha256sum -c --quiet && bash .beagle/checks/T0338/T0338.sh'
budget: 60000 tokens
