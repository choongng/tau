#!/bin/bash
# T0533: the bare-goal task "semver": a one-sentence prompt with no spec or
# link, a hidden grader against Semantic Versioning 2.0.0 that a reference
# adapter passes and each planted defect fails, and launch.sh serving it.
set -e
H=/home/choong/tautest/itc-harness
P=/home/choong/tautest/semver_prompt.txt
test -s "$P"
! grep -qiE 'https?://|semver\.org' "$P"
cd "$H"
timeout 120 python3 grade_semver.py --adapter adapters/semver_reference.py >/dev/null
for trap in prerelease-order numeric-ids leading-zero build-in-order; do
  if SEMVER_TRAP=$trap timeout 120 python3 grade_semver.py --adapter adapters/semver_broken.py >/dev/null 2>&1; then
    echo "trap $trap passed the grader" >&2; exit 1
  fi
done
n=$(timeout 120 python3 grade_semver.py --adapter adapters/semver_reference.py --json | python3 -c 'import json,sys;print(json.load(sys.stdin)["total"])')
[ "$n" -ge 40 ]
./launch.sh --dry-run R999 q35 semver | grep -q "semver_prompt.txt"
./launch.sh --dry-run B999 q35 semver | grep -q "mode: baseline"
