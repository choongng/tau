+++
id = "001637-pursuit"
ordinal = 1637
kind = "pursuit"
timestamp = "2026-10-10T20:45:04+00:00"
summary = "pursuit open T0386: Re-point R42.md's Tests lines to where T0377 and T0378 put the tests"
metric_command = ""
drains = []
hooks = []
+++

criteria: dev-notes/itc-runs/R42.md's class 3 and class 4 Tests lines name tests/test_tool_history.py::test_repeat_refusal_quotes_the_read_cut_continuation, ::test_repeat_refusal_head_is_first_line_for_an_uncut_result and tests/test_session_output_limit_nudge.py::test_loop_cut_nudge_keeps_the_session_provider, ::test_output_limit_cut_nudge_still_uses_the_thinking_off_twin; test_names_resolve.sh on R42.md exits 0; nothing else in the note changes
decided by: sh -c 'echo "e4951b6b9afce621cf32c86148808f8a30cac5f28a8bb854f0f20afac051e1d0  .beagle/checks/T0386/T0386.sh" | sha256sum -c --quiet && bash .beagle/checks/T0386/T0386.sh'
budget: 20000 tokens
