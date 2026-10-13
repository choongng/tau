#!/bin/bash
# T0540: the run build carries the fixes made since R96: beagle contract-first
# contains rotation-fixes' T0536/T0537/T0541 commits with its CI green on a clean
# checkout, and the harness's tau (~/tautest/tau-harness) contains the tau
# commits for T0535 (turn cap 60), T0538 (prove reversion) and T0539 (founding).
set -e
BW=/home/choong/beagle-wt/contract-first
for c in 3ebe17d 8b6a541 24bd167; do
  git -C "$BW" merge-base --is-ancestor "$c" HEAD || { echo "contract-first lacks $c"; exit 1; }
done
TH=/home/choong/tautest/tau-harness
for c in 3d4dd3f9 df30f428 60292e5c; do
  git -C "$TH" merge-base --is-ancestor "$c" HEAD || { echo "tau-harness lacks $c"; exit 1; }
done
[ -z "$(git -C "$TH" status --porcelain --untracked-files=no -- . ':!.beagle')" ] || { echo "tau-harness is dirty"; exit 1; }
bash /home/choong/tautest/tau/.beagle/checks/T0523/T0523.v2.sh | tail -1
