#!/bin/bash
# T0463: source judge judges results under encoded_hex/decoded_hex keys (R56)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_source_judge_judges_results_under_encoded_and_decoded_keys
uv run pytest -q $T
uv run ruff check $F $T
