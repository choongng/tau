+++
id = "001495-pursuit"
ordinal = 1495
kind = "pursuit"
timestamp = "2026-10-10T04:07:43+00:00"
summary = "pursuit prove T0360: WITNESSED — refuses when R39.md's `test_refusal_names_the_clean_prefix.` is put back as `test_refusal_names_the_clean_prefix_call.`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "f664e6b1ca81610d72eb30cb24ee5a482a2e712559c929044c2a58e681dafdeb  .beagle/checks/T0360/T0360.sh" | sha256sum -c --quiet && bash .beagle/checks/T0360/T0360.sh'
refutes: refuses when R39.md's `test_refusal_names_the_clean_prefix.` is put back as `test_refusal_names_the_clean_prefix_call.` (proven 2026-10-10T04:06:46+00:00; refused at Traceback (most recent call last):)
refused after 0s of a 0s check at: Traceback (most recent call last):
refused with: dev-notes/itc-runs/R39.md: tests/test_session_template_tokens.py::test_refusal_names_the_clean_prefix_call
