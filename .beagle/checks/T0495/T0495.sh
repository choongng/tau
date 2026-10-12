#!/bin/bash
# T0495: a [contract] files entry may be a directory: seal, drift, guard and the acceptance check read every file under it.
set -eu
exec bash .beagle/checks/fix/beagle_named.sh tests/test_contract.py 3 \
  test_a_sealed_directory_holds_every_file_under_it \
  test_a_sealed_directory_needs_a_test_besides_the_contract
