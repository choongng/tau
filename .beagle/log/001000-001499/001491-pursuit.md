+++
id = "001491-pursuit"
ordinal = 1491
kind = "pursuit"
timestamp = "2026-10-10T04:05:54+00:00"
summary = "pursuit open T0359: Result lines hold across prompts: hex values and table rows, not code lines"
metric_command = ""
drains = []
hooks = []
+++

criteria: _result_lines picks reference lines that give a concrete result across prompts: hex byte runs and 0x values count as values, a table row whose cell is a value sequence counts, and code-like lines (a trailing ';', pointer increments such as *x++) do not; the code's comments name no project domain. On the R35 COBS reference fixture the table rows (01 01 00, 03 11 22 02 33 00) are named and '*decode++ = 0;' is not; the ITC case of T0347's test still passes. Tests test_result_lines_name_hex_table_rows_not_code_lines and test_result_lines_skip_code_statements beside T0347's; whole file passes, ruff clean.
decided by: sh -c 'echo "38a838e0950554371d4c6bcd4b101a3488fef272b1264278928aa080183230bf  .beagle/checks/T0359/T0359.sh" | sha256sum -c --quiet && bash .beagle/checks/T0359/T0359.sh'
budget: 80000 tokens
