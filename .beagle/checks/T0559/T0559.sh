#!/bin/bash
# T0559: tau founds a contract-first pursuit on slices: one `Slice: examples` task ahead of
# the milestones, every `Slice:` task scoped to contract/ and checked by `contract check
# --draft`, its close sealing the draft as the slice it names, and beagle's --operation
# refusal answered with the slice to plan; Second extraction, Reconcile and
# _settle_after_seal are gone (incremental-contract.md task 6).
set -e
cd /home/choong/tautest/tau
E=examples/extensions/beagle.py
if grep -nE 'Second extraction|Reconcile|_settle_after_seal|"seal", "--reason"' "$E"; then echo "retired flow still present"; exit 1; fi
X() { env -u VIRTUAL_ENV -u UV_PROJECT_ENVIRONMENT PATH="$(echo "$PATH" | tr : '\n' | grep -v '/beagle/' | paste -sd:)" \
  timeout 900 uv run --quiet pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py "$@" 2>&1 | tail -1 | tee /dev/stderr; }
X -k "founding_seeds_examples_slice_only or slice_step_scope_and_check_fixed or close_seals_draft_as_slice or operation_refusal_offers_slice or contract_worker_adds_entries_by_contract_add or contract_worker_reads_the_references_by_contract_refs" | grep -qE '^6 passed'
X | grep -qE '^[0-9]+ passed( in|,)'
