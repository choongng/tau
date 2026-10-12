#!/bin/bash
# T0487: gather-contract-plan stated where Claude Code reads it; 0.47.0; ci/check.sh green.
set -eu
W=${BEAGLE_WT:-/home/choong/beagle-wt/contract-first}
P=$W/plugins/beagle-pursuit
grep -q '1.5 — Gather, then contract, then plan' "$P/commands/pursuit.md"
grep -q 'beagle refs fetch --request' "$P/commands/pursuit.md"
grep -q 'With a `\[contract\]`, a `next` that finds nothing left' "$P/commands/pursuit.md"
grep -q 'A check asks about the work' "$P/commands/pursuit.md"
grep -q 'every leaf is settled, with a `\[contract\]`' "$P/commands/pursuit-run.md"
grep -q '^## 0.47.0$' "$W/docs/upgrade-notes.md"
grep -q '"version": "0.47.0"' "$P/.claude-plugin/plugin.json"
grep -q '^version = "0.47.0"$' "$P/tooling/beagle/pyproject.toml"
grep -q '^__version__ = "0.47.0"$' "$P/tooling/beagle/src/beagle/cli.py"
cd "$W"
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export UV_PROJECT_ENVIRONMENT=${XDG_CACHE_HOME:-$HOME/.cache}/beagle/venv-contract-first-dev
export PYTHONPYCACHEPREFIX=${XDG_CACHE_HOME:-$HOME/.cache}/beagle/pycache
find plugins \( -name .venv -type d -o -name __pycache__ -o -name .pytest_cache \) -exec rm -rf {} +
out=$(timeout 900 bash ci/check.sh 2>&1) || { echo "$out" | grep -v NOLANG | tail -40; exit 1; }
echo "$out" | tail -1
