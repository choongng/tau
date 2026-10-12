#!/bin/bash
# T0489: pursuit_step under [contract]: contract checks allowed, known-answers machinery off, seals when ready, beagle's done verdict.
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 6 \
  test_a_close_seals_the_contract_once_beagle_reads_it_ready \
  test_nothing_ready_says_what_the_contracts_acceptance_found \
  test_a_check_may_run_the_contract_and_nothing_else_of_beagle \
  test_a_declared_contract_turns_the_known_answers_machinery_off \
  test_a_task_on_the_contract_witnesses_a_quote_not_code
mkdir -p "$HOME/.cache/tau-pytest"
timeout 900 uv run --no-sync --with pytest-xdist pytest -q -p no:cacheprovider -n auto \
  --basetemp="$HOME/.cache/tau-pytest/T0489" $T 2>&1 | tail -1 | grep -E '^[0-9]+ passed in'
uv run --no-sync ruff check $F $T
uv run --no-sync ruff format --check $F $T
