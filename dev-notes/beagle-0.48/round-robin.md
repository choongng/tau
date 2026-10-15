# Round robin: 30 rounds across models and workloads (T0610)

Owner 2026-10-14, after lift-12: round-robin models and workloads for 30 more rounds, each capped at
30 min. A round is one run that is graded (curve.py, time to green), read, and given a row and
section in `dev-notes/contract-first/eval.md`.

Fixes still land between rounds, one patch at a time: proven, merged to choong-dev, and tau-harness
moved before the next launch. A fix must hold across models, not just the one that showed the
problem.

Round i (from 0) runs model `M[i % 3]` on task `W[i % 4]`, so each 12 rounds cover all 12 pairs.

- **Models (krang):**
  - `q35` = qwen3.6-35b-q6-mtp-thinking-coding;
  - `g26` = gemma4-26b-a4b-qat-q4;
  - `lfm24` = lfm2.5-24b-a2b-qad-q4.
- **Tasks:** wrenfold (spec), semver (bare goal), itc, cobs.
- **Bars:** plain tau with q35 — B04 itc, B05 cobs, B06 wrenfold 9.1 min, B07 semver 8.1 min. g26 and
  lfm24 have no plain baseline yet.

Watch on lfm24: llama.cpp #30490. After about 8 rejected tool calls in a row it writes
`<function=…>` as text. Tau's text-tool-call follow-up (2 in a row, 4 per run) is the only guard.

| Round | Run | Model | Task | Result | Fix after |
|---|---|---|---|---|---|
| 1 | R104 | q35 | wrenfold | 12/54; T0002+T0003 closed (18.5, 21.3 min) | T0620 |
| 2 | R105 | g26 | semver | 0/76; setup milestone 18.5 min, URL source unfetched | T0621 |
| 3 | R106 | lfm24 | itc | 0/42; prose in pursuit_step's task, breaker stop at 11 min | T0623 (+T0622) |
| 4 | R107 | q35 | cobs | 37/44; all 6 closed, ended at 27.8 min; no source named, so no cases | T0624 |
| 5 | R108 | g26 | wrenfold | 0/54; tests-only scope, data-test route, 2 cases workers, code refused | T0625 |
| 6 | R109 | lfm24 | semver | 0/76; 6 refused plans, 3 cases workers' cites all #0b7, open refused | T0626 |
| 7 | R110 | q35 | itc | 17/42; tied at 11 min, 22/24 cases; gap-case corrections put back twice | T0627 |
| 8 | R111 | g26 | cobs | 3/44; tied at 15 min; code worker 3 time cuts in a row, no action; placeholder cobs.py | T0628 |
| 9 | R112 | lfm24 | wrenfold | 0/54, no code; T0002 never opened: no-scope refusal came after a 6 min cases worker | T0629 |
| 10 | R113 | q35 | semver | **75/76 at 4 min** (plain 8.1), all-done at 16 min | — |
| 11 | R114 | g26 | itc | | |
| 12 | R115 | lfm24 | cobs | | |
| 13 | R116 | q35 | wrenfold | | |
| 14 | R117 | g26 | semver | | |
| 15 | R118 | lfm24 | itc | | |
| 16 | R119 | q35 | cobs | | |
| 17 | R120 | g26 | wrenfold | | |
| 18 | R121 | lfm24 | semver | | |
| 19 | R122 | q35 | itc | | |
| 20 | R123 | g26 | cobs | | |
| 21 | R124 | lfm24 | wrenfold | | |
| 22 | R125 | q35 | semver | | |
| 23 | R126 | g26 | itc | | |
| 24 | R127 | lfm24 | cobs | | |
| 25 | R128 | q35 | wrenfold | | |
| 26 | R129 | g26 | semver | | |
| 27 | R130 | lfm24 | itc | | |
| 28 | R131 | q35 | cobs | | |
| 29 | R132 | g26 | wrenfold | | |
| 30 | R133 | lfm24 | semver | | |
