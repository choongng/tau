+++
id = "002392-pursuit"
ordinal = 2392
kind = "pursuit"
timestamp = "2026-10-12T14:26:57+00:00"
summary = "pursuit prove T0468: WITNESSED — refuses when session.py's `return self._run_loops() or self._sentences_loo…` is put back as `return self._run_loops()`"
metric_command = ""
drains = []
hooks = []
+++

check: sh -c 'echo "65fb4304de318643623e45894a936a0cb8cacbde43ab0c093b20c6f82d5921a6  .beagle/checks/T0468/T0468.sh" | sha256sum -c --quiet && bash .beagle/checks/T0468/T0468.sh'
refutes: refuses when session.py's `return self._run_loops() or self._sentences_loo…` is put back as `return self._run_loops()` (proven 2026-10-12T14:25:59+00:00; refused at FAILED tests/test_session_output_limit.py::test_sentences_repeated_within_one_line_are_cut[asyncio])
refused after 1s of a 2s check at: FAILED tests/test_session_output_limit.py::test_sentences_repeated_within_one_line_are_cut[asyncio]
refused with: 1 failed, 9 deselected in 0.56s
standing checks red: T0335, T0360, T0368, T0386, T0419, T0420, T0421, T0422, T0336
