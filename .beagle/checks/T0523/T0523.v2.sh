#!/usr/bin/env bash
# T0523 v2 (audit 10-13): run beagle's CI on a clean checkout of contract-first's
# tip, not in the live worktree, so a stray __pycache__ left there by someone's
# pytest run (or a run harness) cannot turn the plugin-tree gate red.
# The one standing run of beagle CI for contract-first: T0498, T0503, T0512,
# T0513, T0514, T0516 and T0530 claim "beagle CI green" and run -k subsets.
set -u
SRC=/home/choong/beagle-wt/contract-first
T=$(mktemp -d "${TMPDIR:-/tmp}/t0523.XXXXXX")
trap 'git -C "$SRC" worktree remove --force "$T/wt" >/dev/null 2>&1; rm -rf "$T"' EXIT
git -C "$SRC" worktree add --detach -q "$T/wt" HEAD || exit 1
cd "$T/wt" || exit 1
# uv.lock is gitignored, so a fresh checkout has none and the lockfile gate
# checks nothing and fails; carry the worktree's own locks across, as they are.
(cd "$SRC" && find plugins -name uv.lock -not -path '*/.venv/*') | while read -r f; do cp "$SRC/$f" "$f"; done
out=$(PYTHONDONTWRITEBYTECODE=1 bash ci/check.sh 2>&1); rc=$?
echo "$out" | tail -3
[ "$rc" = 0 ] || { echo "ci/check.sh exited $rc"; exit 1; }
echo "$out" | grep -qx "ci: all gates green" || { echo "ci/check.sh did not say all gates green"; exit 1; }
echo "T0523: beagle contract-first ci/check.sh green"
