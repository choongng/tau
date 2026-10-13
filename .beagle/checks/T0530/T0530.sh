#!/bin/bash
# T0530: the contract check lists unnamed properties in one problem naming the
# files it read, without "encode it", and an id in a JSON file is not a test.
# R93: 19 per-property lines sent workers to give properties inputs, then the
# check passed on ids written into JSON files under contract/.
set -e
cd /home/choong/beagle-wt/property-acceptance-message/plugins/beagle-pursuit/tooling/beagle
export UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops
uv run --quiet --with pytest --extra browser python -m pytest tests/test_contract.py -q -p no:cacheprovider \
  -k "unnamed_property_in_one_problem or property_named_in_a_json_file or skip_a_property" 2>&1 \
  | tail -1 | tee /dev/stderr | grep -qE '^3 passed'
