#!/bin/bash
# T0507: a contract worker is briefed to read the references by `contract refs`,
# those calls do not count toward the nothing-written refusals and pass the late
# one, and a refused reference read names them; other workers' briefs are unchanged.
set -e
cd /home/choong/tautest/tau
uv run pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "contract_worker_reads_the_references_by_contract_refs or reread_refusal_on_reference_offers_search or known_answers_worker_ranged_reference_read_is_not_refused or nth_reread_of_a_reference_window" \
  2>&1 | tail -3 | tee /dev/stderr | grep -qE '^4 passed'
echo "T0507: contract workers read references by contract refs, uncounted; other briefs as before"
