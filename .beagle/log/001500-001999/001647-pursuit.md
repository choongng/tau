+++
id = "001647-pursuit"
ordinal = 1647
kind = "pursuit"
timestamp = "2026-10-10T20:59:35+00:00"
summary = "pursuit open T0384: R43 fix: a cut-off kill note says what filled the turn"
metric_command = ""
drains = []
hooks = []
+++

criteria: _WorkerEvents records what filled each cut-off turn: thinking with no reply, reply text with no call, or a call's arguments. A worker killed on cut-offs gets a kill note worded by that: 'write in parts' (or split) only when a call was cut off mid-argument; reply-text or thinking cut-offs say the worker spent its turns reasoning in prose without acting, and the next notes should say what to do first, not to write in parts. The T0372 thinking-off retry policy is unchanged (no further retry offered). Structural, no domain words. Tests test_cut_off_kill_note_names_reply_text_reasoning, test_cut_off_kill_note_says_write_in_parts_only_for_a_call_argument; whole file passes, ruff clean.
decided by: sh -c 'echo "929e4abfa25ccf92b7c64de5c7a2400283fdc10cbc52d96e5f524e0a8a342e81  .beagle/checks/T0384/T0384.sh" | sha256sum -c --quiet && bash .beagle/checks/T0384/T0384.sh'
budget: 80000 tokens
