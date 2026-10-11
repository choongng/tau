+++
id = "001717-pursuit"
ordinal = 1717
kind = "pursuit"
timestamp = "2026-10-11T00:21:28+00:00"
summary = "pursuit open T0397: Detect contradictions and stuck loops"
metric_command = ""
drains = []
hooks = []
+++

criteria: itc-harness/mine/contradictions.py (--events --refused --kinds --out) writes findings.json with three lists, each finding giving run, model, role, session, the trace lines and the kinds involved. offered_then_refused: a refused result whose text offers a call (a tool and its task or arguments), followed by the driver's next call being that offered call, which is refused too; a stop the refusal offered, refused by the stop gate's nudge, counts with next_is_stop. alternating: two or more refusal kinds alternating on one task in one session (A B A at least). repeated: the same refusal kind three or more times on one task with no successful pursuit tool result between. Found in R42, R43 and R44 at least (the known cases), and R44's refused stop after the step cap's offer. Fields: session, refusal_line, call_line, next_line, kinds, offered text, next call digest. Tests in mine/test_contradictions.py incl. an offered call that succeeds (not a finding); ruff clean.
decided by: sh -c 'echo "1db125fc2935bd5a756ba18c045026833e8a0af087e4764ffa16679227bb81c8  .beagle/checks/T0397/T0397.sh" | sha256sum -c --quiet && bash .beagle/checks/T0397/T0397.sh'
budget: 140000 tokens
