#!/bin/bash
# T0561: beagle contract-first carries the incremental-contract build (T0554 c1eb917,
# T0555 fd2cb5a, T0556 bb1e238, T0557 c2b6bb0, T0558 b9efa1d) and its CI is green on a
# clean checkout of its tip; the worktree is clean.
set -e
BW=/home/choong/beagle-wt/contract-first
for c in c1eb917 fd2cb5a bb1e238 c2b6bb0 b9efa1d; do
  git -C "$BW" merge-base --is-ancestor "$c" HEAD || { echo "contract-first lacks $c"; exit 1; }
done
[ "$(git -C "$BW" rev-parse --abbrev-ref HEAD)" = contract-first ] || { echo "contract-first worktree not on its branch"; exit 1; }
[ -z "$(git -C "$BW" status --porcelain --untracked-files=no -- . ':!.beagle')" ] || { echo "contract-first is dirty"; exit 1; }
bash /home/choong/tautest/tau/.beagle/checks/T0523/T0523.v2.sh | tail -1 | tee /dev/stderr | grep -q "ci/check.sh green"
