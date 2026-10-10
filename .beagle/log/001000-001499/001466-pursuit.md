+++
id = "001466-pursuit"
ordinal = 1466
kind = "pursuit"
timestamp = "2026-10-10T03:00:16+00:00"
summary = "pursuit open T0344: Order-dependent failure of test_stop_gate_founded_session_gets_no_unfounded_followup"
metric_command = ""
drains = []
hooks = []
+++

criteria: test_stop_gate_founded_session_gets_no_unfounded_followup passes when run after test_stop_gate_says_nothing_unfounded_in_an_interactive_session (the cached extension module's BEAGLE_BIN follows the beagle and fake_beagle fixtures whichever test loaded it first), and the file passes whole and under -k session.
decided by: sh -c 'echo "2dd1043bba3ef6fb88147f8cedd01be5f5df005245c60e84ec24d0e647486fc2  .beagle/checks/T0344/T0344.sh" | sha256sum -c --quiet && bash .beagle/checks/T0344/T0344.sh'
budget: 15000 tokens
