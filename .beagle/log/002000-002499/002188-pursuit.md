+++
id = "002188-pursuit"
ordinal = 2188
kind = "pursuit"
timestamp = "2026-10-12T09:40:20+00:00"
summary = "pursuit open T0460: After an import-only prove, the next step asks for a WITNESS, not a new check; the spawn-limit refusal doesn't offer a sub-agent (R55)"
metric_command = ""
drains = []
hooks = []
+++

criteria: After an import-only prove the next step asks for the WITNESS on the same check, not a new check, and the new-route refusal no longer contradicts its sub-agent offer (R55). Named test test_import_only_not_proof_next_asks_for_a_witness_not_a_new_check passes; suite and ruff pass.
decided by: sh -c 'echo "a4026e4b864ca7693d647106f7918de62ec87c357443fe8c4fe847938f32c38a  .beagle/checks/T0460/T0460.sh" | sha256sum -c --quiet && bash .beagle/checks/T0460/T0460.sh'
budget: 150000 tokens
