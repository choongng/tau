+++
id = "002366-pursuit"
ordinal = 2366
kind = "pursuit"
timestamp = "2026-10-12T14:09:37+00:00"
summary = "pursuit open T0463: The source judge judges results under encoded_hex/decoded_hex keys (R56)"
metric_command = ""
drains = []
hooks = []
+++

criteria: The source judge judges results under encoded/decoded keys (e.g. encoded_hex, decoded_hex), and input_* keys count as inputs (R56). Named test test_source_judge_judges_results_under_encoded_and_decoded_keys passes; suite and ruff pass.
decided by: sh -c 'echo "60eb3275f8969a1e9dcb670c5e14c97ee2ff4f9c99a65ae9101e149690724f99  .beagle/checks/T0463/T0463.sh" | sha256sum -c --quiet && bash .beagle/checks/T0463/T0463.sh'
budget: 150000 tokens
