+++
id = "001605-pursuit"
ordinal = 1605
kind = "pursuit"
timestamp = "2026-10-10T18:45:34+00:00"
summary = "pursuit open T0377: R42 fix: the repeat refusal of a cut read quotes its continuation note"
metric_command = ""
drains = []
hooks = []
+++

criteria: When tau refuses a repeated call, the line it quotes from the earlier result is taken from the result as the model saw it, after tau appended its read-cut note, so a repeated read of a cut file quotes the 'continue with offset=N' note; an uncut result is quoted by its first line as before. Model- and prompt-independent. Tests test_repeat_refusal_quotes_the_read_cut_continuation, test_repeat_refusal_head_is_first_line_for_an_uncut_result; the repeat-breaker and session tests pass, ruff clean.
decided by: sh -c 'echo "ef7a7fd351b42e7e610b3d7a7088f8060c74b30d0fac4fd8bc264bd8dc5f70f2  .beagle/checks/T0377/T0377.sh" | sha256sum -c --quiet && bash .beagle/checks/T0377/T0377.sh'
budget: 50000 tokens
