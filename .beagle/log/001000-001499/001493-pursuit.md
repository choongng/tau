+++
id = "001493-pursuit"
ordinal = 1493
kind = "pursuit"
timestamp = "2026-10-10T04:06:37+00:00"
summary = "pursuit open T0360: Run notes' named tests resolve: R39.md names fixed, tau-subagents names resolvable"
metric_command = ""
drains = []
hooks = []
+++

criteria: Every test named on the Tests: lines of R36.md-R39.md exists, in tau or in the tau-subagents extension repo, checked by the shared .beagle/checks/fix/test_names_resolve.sh; R39.md's six stale names point at the tests that were written (test_session_template_tokens.py: test_leak_in_optional_argument_runs_the_clean_call, test_leak_inside_required_argument_still_refused, test_refusal_names_the_clean_prefix; test_tool_missing_argument.py: test_missing_path_names_the_missing_argument, test_non_string_path_still_says_must_be_a_string; test_known_answers_close_refuses_cases_test_copying_data_test).
decided by: sh -c 'echo "f664e6b1ca81610d72eb30cb24ee5a482a2e712559c929044c2a58e681dafdeb  .beagle/checks/T0360/T0360.sh" | sha256sum -c --quiet && bash .beagle/checks/T0360/T0360.sh'
budget: 15000 tokens
