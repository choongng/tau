#!/bin/bash
# T0471: a rank refusal offers no flag pursuit_step cannot pass (R58)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_rank_refusal_of_a_step_open_offers_no_flag_the_driver_cannot_pass
uv run pytest -q $T
uv run ruff check $F $T
