+++
id = "001260-pursuit"
ordinal = 1260
kind = "pursuit"
timestamp = "2026-10-09T19:26:04+00:00"
summary = "pursuit open T0293: Audit 10: known-answer results under 4 chars or equal to an input are checked against the source"
metric_command = ""
drains = []
hooks = []
+++

criteria: A known-answer case whose expected result is shorter than RESULT_MIN_CHARS, or equal to one of its inputs, is no longer exempt from the source check: when the case's source quotes a reference line, the result must appear in that quoted line or the reference line after it (the narrow context _lines_after gives), not merely anywhere in the source, and a result absent there flags the case as unquoted. R35's empty_input case (result "00" equal to its input, against a reference whose line for the empty input gives a different encoding) is flagged; a short correct result present on its quoted reference line passes; a short result with no quoted context stays unflagged (no false refusal from '1' or 'ok' occurring by chance). R35's six correct worked examples, including the elided 'FF 01 02 03 ... FD FE 00' form, still pass, and existing known-answer tests pass. Keyed on structure (lengths, quotes, reference lines), no prompt-domain words.
decided by: sh -c 'echo "3c8056cf56b42515e88daa6f2833bbb46e7501c31a9cdddfd1b9ba09b89c84b6  .beagle/checks/T0293/T0293.sh" | sha256sum -c --quiet && bash .beagle/checks/T0293/T0293.sh'
budget: 120000 tokens
