#!/bin/bash
# T0474: a worker's git commit gets the worker refusal (R59)
set -e
T=tests/test_beagle_example_extension.py
F=examples/extensions/beagle.py
bash .beagle/checks/fix/named_tests.sh $T 1 test_worker_git_commit_gets_the_worker_refusal_not_commit_claims_advice
uv run pytest -q $T
uv run ruff check $F $T
