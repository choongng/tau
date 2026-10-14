+++
id = "003097-pursuit"
ordinal = 3097
kind = "pursuit"
timestamp = "2026-10-14T19:47:16+00:00"
summary = "pursuit open T0599: strip the contract mode from examples/extensions/beagle.py and its tests (branch beagle-0.48)"
metric_command = ""
drains = []
hooks = []
+++

criteria: On branch beagle-0.48 (worktree ~/tautest/tau-wt-048): the contract mode is deleted from examples/extensions/beagle.py (no contract verb calls, slices, seal-the-contract, dispute/supersede, oracle/stand-in, CONTRACT_* text), entangled functions keep their mode-independent half, the extension is under 16300 lines, the extension's tests pass with the beagle venv off PATH, and a test named for bare_goal ... no_slice shows founding on a bare goal plans no task before the first milestone
decided by: sh -c 'echo "5cd7d038e00c358e1491be88bc1d8f7276d5a5a42c7a0d7e65d503533843c389  .beagle/checks/T0599/T0599.sh" | sha256sum -c --quiet && bash .beagle/checks/T0599/T0599.sh'
budget: 400000 tokens
