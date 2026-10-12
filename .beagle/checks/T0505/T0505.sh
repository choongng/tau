#!/bin/bash
# T0505: a worker sent on a task runs the contract's reads (R77's exact call
# included) and is still kept from the rest of beagle, contract seal included.
set -e
cd /home/choong/tautest/tau
uv run pytest -q -p no:cacheprovider tests/test_beagle_example_extension.py \
  -k "worker_guard_refuses_beagle_commands_and_beagle_reads or task_worker_brief_carries_the_no_beagle_note or worker_may_read_the_pursuit_but_not_change_it" \
  2>&1 | tail -3 | tee /dev/stderr | grep -qE '^[0-9]+ passed'
python3 - <<'PY'
s = open("tests/test_beagle_example_extension.py").read()
i = s.index("async def test_worker_guard_refuses_beagle_commands_and_beagle_reads")
body = s[i:s.index("\n\n\n", i)]
verb = "beagle pursuit" + " contract"  # spelled apart: beagle's check lint reads the words as a call
for want in (f"{verb} check --draft 2>&1 | tail -100", f"{verb} refs", f"{verb} seal"):
    assert want in body, f"the task-worker guard test does not try `{want}`"
PY
echo "T0505: a task worker reads the contract; the rest of beagle and seal refused"
