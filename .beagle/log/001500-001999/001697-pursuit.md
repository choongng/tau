+++
id = "001697-pursuit"
ordinal = 1697
kind = "pursuit"
timestamp = "2026-10-10T23:58:36+00:00"
summary = "pursuit open T0400: Audit 14 fix: the argument-leak scan keeps its own pattern, without T0393's reply-only shapes"
metric_command = ""
drains = []
hooks = []
+++

criteria: The reply follow-up (session.py ~2256) keeps T0393's match of a text tool call without its opening tag. The tool-argument leak scan (_template_tokens_in_arguments, ~6356) uses the pattern as it was before T0393 (faf061f5), so a write or edit whose content holds <function=x><parameter=… or </function></tool_call> is not refused as a leak, while the shapes it caught before are still caught. Tests test_argument_scan_accepts_unopened_call_markup_in_a_write and the existing test_text_tool_call_without_opening_tag_is_followed_up; the file passes, ruff clean.
decided by: sh -c 'echo "7e25a540bcd3a0ba428ee31dcc0d218fb093a25f19a035a59b6f039523c716f3  .beagle/checks/T0400/T0400.sh" | sha256sum -c --quiet && bash .beagle/checks/T0400/T0400.sh'
budget: 50000 tokens
