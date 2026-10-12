#!/bin/bash
# T0485: `beagle refs fetch|find|list` fetches references once, as text, and finds the line.
set -eu
exec bash .beagle/checks/fix/beagle_named.sh tests/test_refs.py 4 \
  test_refs_fetch_writes_text_and_index \
  test_refs_fetch_keeps_what_is_on_disk_and_records_a_failure \
  test_refs_find_numbers_lines_as_an_editor_does \
  test_refs_urls_in_leaves_the_sentence_its_punctuation
