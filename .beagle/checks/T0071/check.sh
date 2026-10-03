#!/bin/bash
# T0071: a reference fetch that times out is retried once with a longer timeout.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 2 \
  test_reference_fetch_retries_a_timeout_with_a_longer_timeout \
  test_reference_fetch_does_not_retry_a_refused_url
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
