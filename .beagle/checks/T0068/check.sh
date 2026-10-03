#!/bin/bash
# T0068: a not-done step names implementation its worker wrote under tests/.
set -eu
bash .beagle/checks/fix/named_tests.sh tests/test_beagle_example_extension.py 3 \
  test_not_done_step_names_implementation_written_under_tests \
  test_worker_scope_refusal_of_source_says_not_under_tests_either \
  test_brief_for_a_data_task_gives_the_request_as_context_only
.venv/bin/ruff check examples/extensions/beagle.py tests/test_beagle_example_extension.py
