+++
id = "001297-pursuit"
ordinal = 1297
kind = "pursuit"
timestamp = "2026-10-09T21:24:35+00:00"
summary = "pursuit open T0313: R36 fix: chat-template tokens in tool arguments are refused, not stored"
metric_command = ""
drains = []
hooks = []
+++

criteria: tau's session refuses, before it runs, any tool call (built-in or extension-registered, driver or sub-agent session) whose string arguments, at any depth, carry a chat template's tool-call or channel control tokens: gemma's <|tool_call>, <tool_call|>, <|channel>, <channel|> and qwen's <tool_call>/</tool_call> followed by a function or call opening. The refusal goes through the existing before_tool_call refusal path (_refuse_unproductive_call, counting toward REPEATED_CALL_STOP) and says: its arguments carry the chat template's own tool-call tokens, so the reply's next call ran into this one; send one call per reply, with the text alone. Matching is on token syntax only, with no model names; ordinary text with angle brackets, HTML/XML, generics, and a lone mention of the word tool_call run normally (negative test). Tests use R36's real founding-statement tail as a fixture.
decided by: sh -c 'echo "cccd087687dd25f0c86c2a3a515317de4ea18f693dd400bfbe635f9bb8699e8a  .beagle/checks/T0313/T0313.sh" | sha256sum -c --quiet && bash .beagle/checks/T0313/T0313.sh'
budget: 100000 tokens
