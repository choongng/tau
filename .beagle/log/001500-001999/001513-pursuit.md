+++
id = "001513-pursuit"
ordinal = 1513
kind = "pursuit"
timestamp = "2026-10-10T04:15:55+00:00"
summary = "pursuit open T0348: Judge-only escalation: no per-file split when only the source judge holds the task"
metric_command = ""
drains = []
hooks = []
+++

criteria: When only the known-answers source judge holds a task open (its bound check passes each time), the escalation (_unchanged_route_escalation / _judge_escalation) does not offer a per-file split; it offers a notes-only pursuit_step naming the failing cases and reference lines that give results (_unanswered_case_note / _result_lines), with stopping as the alternative. Tasks whose check fails keep the split offer. Regression tests test_judge_only_escalation_offers_no_split and test_judge_only_escalation_names_cases_and_result_lines; whole file passes, ruff clean.
decided by: sh -c 'echo "eaec5c476a305e694e39e588d6e170899bceaa5a5bffb1c9ae8de54b740b0618  .beagle/checks/T0348/T0348.sh" | sha256sum -c --quiet && bash .beagle/checks/T0348/T0348.sh'
budget: 80000 tokens
