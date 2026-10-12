+++
id = "002197-pursuit"
ordinal = 2197
kind = "pursuit"
timestamp = "2026-10-12T09:47:09+00:00"
summary = "pursuit open T0462: Under lean, no remaining driver text recommends locks= (audit of T0458)"
metric_command = ""
drains = []
hooks = []
+++

criteria: Under BEAGLE_TAU_LEAN, _uncommitted_note, _oracle_with_code_problem and _open_mixed_refusal recommend no locks; with lean off each text is byte-for-byte unchanged (audit of T0458). Named test test_lean_uncommitted_note_and_oracle_hints_recommend_no_locks passes; suite and ruff pass.
decided by: sh -c 'echo "e6cfc2eef4e0170e2248307686e9682a3ae8600474ed3aa28fd79c089c3b1a8f  .beagle/checks/T0462/T0462.sh" | sha256sum -c --quiet && bash .beagle/checks/T0462/T0462.sh'
budget: 150000 tokens
