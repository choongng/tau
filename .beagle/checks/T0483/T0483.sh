#!/bin/bash
# T0483: pursuit brief carries the contract's wording for each kind of task.
set -eu
exec bash .beagle/checks/fix/beagle_named.sh tests/test_contract.py 4 \
  test_brief_gives_work_on_the_contract_the_inventory \
  test_brief_keeps_a_second_extraction_from_reading_the_first \
  test_brief_says_the_sealed_contract_is_what_done_means \
  test_brief_says_nothing_of_a_contract_none_declares
