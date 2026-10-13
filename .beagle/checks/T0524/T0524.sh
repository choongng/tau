#!/bin/bash
# T0524: an acceptance that runs beagle's contract run again is refused, not
# run. R88's accept.sh was `exec beagle pursuit contract run`, which runs
# accept.sh; the two started each other until the kernel killed the run at 23 min.
set -e
W=/home/choong/beagle-wt/contract-no-recursion
BEAGLE=$W/plugins/beagle-pursuit/bin/beagle
r86=/home/choong/tautest/tau/.beagle/checks/T0509/r86
here=/home/choong/tautest/tau/.beagle/checks/T0524
(cd $W/plugins/beagle-pursuit/tooling/beagle &&
 UV_PROJECT_ENVIRONMENT=$HOME/.cache/beagle/venv-ops PYTHONPYCACHEPREFIX=$HOME/.cache/beagle/pycache-ops \
 uv run --quiet --with pytest --extra browser python -m pytest tests/test_contract.py -q -p no:cacheprovider \
   -k "beagle_again" 2>&1 | tail -1 | tee /dev/stderr | grep -qE '^1 passed')
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
mkdir -p "$t/.beagle" "$t/contract" "$t/bin"
cp -r "$r86/references" "$t/"
cp "$r86"/*.json "$t/contract/"
cp "$here/r88-accept.sh" "$t/contract/accept.sh"   # R88's own
printf '#!/bin/sh\nexec %s "$@"\n' "$BEAGLE" > "$t/bin/beagle"; chmod +x "$t/bin/beagle"
printf '[goal]\nstatement="x"\ncriteria=["y"]\n[contract]\npath="contract/contract.json"\nsecond="contract/contract.second.json"\nacceptance="sh contract/accept.sh"\nfiles=["contract/"]\n' > "$t/.beagle/pursuit.toml"
(cd "$t" && git init -q)
# The static check names it before anything runs it.
out=$(cd "$t" && PATH="$t/bin:$PATH" "$BEAGLE" pursuit contract check --draft 2>&1) || true
echo "$out" | grep -q "acceptance file contract/accept.sh runs .beagle" ||
  { echo "check --draft did not name the acceptance that runs beagle"; echo "$out"; exit 1; }
# Run for real, capped: without the guard this would not end.
set +e
out=$(cd "$t" && PATH="$t/bin:$PATH" systemd-run --user --scope -q -p MemoryMax=1G -p TasksMax=64 \
      timeout 60 "$BEAGLE" pursuit contract run 2>&1); rc=$?
set -e
echo "contract run exit $rc" >&2
[ "$rc" -ne 0 ] && [ "$rc" -ne 124 ] && [ "$rc" -ne 137 ] || { echo "contract run did not end refused (exit $rc)"; exit 1; }
echo "$out" | grep -q "would start itself again" || { echo "$out" | tail -5; exit 1; }
