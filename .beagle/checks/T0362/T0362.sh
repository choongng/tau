#!/bin/bash
# Worker thinking on for pursuit runs: R runs dispatch workers at the driver's level; B runs (no workers) stay off; meta records it
set -eu
H=/home/choong/tautest/itc-harness
for m in qwen mimo gemma; do
  r=$($H/launch.sh --dry-run R99 $m itc)
  lvl=$(echo "$r" | sed -n 's/^driver thinking: \([a-z]*\).*/\1/p')
  [ "$lvl" != none ] || { echo "$m: driver has no thinking level"; exit 1; }
  echo "$r" | grep -qx "worker thinking: $lvl" || { echo "$m: worker thinking is not the driver's ($lvl)"; echo "$r" | grep thinking; exit 1; }
  echo "$r" | grep -q "BEAGLE_TAU_DISPATCH_THINKING=$lvl " || { echo "$m: the command does not pass worker thinking"; exit 1; }
done
$H/launch.sh --dry-run B99 qwen cobs | grep -qx "worker thinking: off" || { echo "B run worker thinking not off"; exit 1; }
grep -q '"worker_thinking": e\["worker_think"\]' $H/launch.sh || { echo "meta records no worker_thinking"; exit 1; }
echo OK
