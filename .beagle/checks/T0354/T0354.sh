#!/bin/bash
# Baseline launch mode: B runs use plain tau (no extensions) on a beagle-free prompt; R runs unchanged
set -eu
H=/home/choong/tautest/itc-harness
for t in itc cobs; do
  p=$H/prompts/${t}_baseline_prompt.txt
  [ -s $p ] || { echo "no $p"; exit 1; }
  if grep -qiE "beagle|pursuit" $p; then echo "$p mentions beagle/pursuit"; exit 1; fi
  # the reference links are kept
  diff <(grep -oE "https?://\S+" /home/choong/tautest/${t}_prompt.txt) <(grep -oE "https?://\S+" $p)
done
b=$($H/launch.sh --dry-run B99 qwen cobs)
echo "$b" | grep -q -- "--no-extensions" || { echo "B run without --no-extensions"; echo "$b"; exit 1; }
echo "$b" | grep -q "mode: baseline" || { echo "dry-run does not say mode: baseline"; exit 1; }
echo "$b" | grep -qi "pursuit" && { echo "B run prompt still mentions pursuit"; exit 1; }
r=$($H/launch.sh --dry-run R99 qwen cobs)
echo "$r" | grep -q -- "--no-extensions" && { echo "R run got --no-extensions"; exit 1; }
echo "$r" | grep -q "mode: pursuit" || { echo "dry-run does not say mode: pursuit"; exit 1; }
grep -q '"mode"' $H/launch.sh || { echo "meta records no mode"; exit 1; }
echo OK
