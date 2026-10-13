#!/bin/bash
# T0549: the discrimination recon note exists and answers its four questions with
# file:line evidence (R97: a sealed accept.sh that printed ok whatever the code did).
set -e
F=/home/choong/tautest/tau/dev-notes/contract-first/discriminate-recon.md
[ -f "$F" ] || { echo "no $F"; exit 1; }
for h in "## What R97 sealed" "## What sealing checks now" "## Options" "## Recommendation"; do
  grep -qF "$h" "$F" || { echo "missing section: $h"; exit 1; }
done
n=$(grep -cE '[a-z_/.]+\.(py|md|sh|json):[0-9]+' "$F")
[ "$n" -ge 6 ] || { echo "only $n file:line citations"; exit 1; }
echo "T0549: discrimination recon written, $n citations"
