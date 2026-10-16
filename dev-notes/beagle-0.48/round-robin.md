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
- **Bars:** plain tau (`tau -p --no-extensions`), one run per pair. See *Plain baselines* below.

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
| 11 | R114 | g26 | itc | 0/42, no code; references/ scope refused after a 5 min cases worker; 2 open refusals (no per-op invalid case), workers skipped the dry run | T0630 |
| 12 | R115 | lfm24 | cobs | 0/44, no code; 12.5 min cases worker skipped its dry run and was refused at the open; second worker mending at the cap | T0633 |
| 13 | R116 | q35 | wrenfold | **54/54 at 21 min** (plain 9.1); T0003's worker borrowed T0002's witness from its close body, a second worker ran | T0634 |
| 14 | R117 | g26 | semver | **75/76 at 14 min** (plain 8.1); misses `1.2.3\n` as R113; code passed 4 min into its worker, then 10 min went on a 280-char witness needle | T0635 |
| 15 | R118 | lfm24 | itc | **0/42**; founding kept a 'Setup complete: beagle init written …' milestone as T0002 and the 30 min went there | T0636 |
| 16 | R119 | q35 | cobs | 0/44 (no code; cases workers checked the table with their own encoder) | T0637 |
| 17 | R120 | g26 | wrenfold | 48/54 (encode/decode right at 17 min; no `count`: founded from a cut extract) | T0638 |
| 18 | R121 | lfm24 | semver | 0/76 (no code; every milestone sourced "N/A", cases workers wrote from it) | T0639 |
| 19 | R122 | q35 | itc | 2/42 (founded intervals-with-counters from the paper's introduction; no fork/event/join) | T0640 |
| 20 | R123 | g26 | cobs | 35/44 (setup milestone kept as T0002, 28 min; code written under it) | T0641 |
| 21 | R124 | lfm24 | wrenfold | 0/54 (milestone sources were descriptions; spec-tied T0002 never reached code) | T0642 |
| 22 | R125 | q35 | semver | 75/76 at 27 min (plain 8.1; cases 5–6 min per spec-tied task; one page fetched per fragment) | T0643 |
| 23 | R126 | g26 | itc | 9/42 ('Examine ... patterns' kept as a study T0002, 22 min; implementation never opened) | T0644 |
| 24 | R127 | lfm24 | cobs | 0/44 at 12 min (three driver cut-offs in a row after founding; tau's nudges ran out and the run ended) | T0645 |
| 25 | R128 | q35 | wrenfold | 48/54 capped (encoder, decoder closed; cases workers ~21 of 30 min) | T0646 |
| 26 | R129 | g26 | semver | 27/76 final; **75/76 at t13–t23** then a witness-ask follow-up worker regressed the regex | T0647 |
| 27 | R130 | lfm24 | itc | 0/42, no code; cases cited interval-tree-clocks lines under itc2008, re-anchoring made one a blank line, 3 cases workers | T0657 |
| 28 | R131 | q35 | cobs | 3/44 final (best encode 8/44); decode never started; a worked-out `limit` case the code worker could not satisfy or dispute, last edit regressed | none (no sound check; see eval) |
| 29 | R132 | g26 | wrenfold | 51/54 final (54/54 at 13 min); T0002 never closed: an `example` case copied one integer's bytes as encode's output (end marker dropped), the worker's correction was accepted but cost a 6.4-min cut reply; bare `pytest` check failed collection, retry worker fixed it at its 277 s wall; decode rewrite regressed | none (clock; see eval) |
| 30 | R133 | lfm24 | semver | | |

## Plain baselines (B04–B15)

These were run after R132, from the harness pinned at f331db78. Each pair has one plain
`tau -p --no-extensions` run on the same prompt and cap. B04–B07 ran on 10-14 and B08–B15 on
10-15. Every baseline ended on its own, and none was capped. The adapters are in
`itc-harness/runs/BNN/adapter.py` (committed 2d99f05).

| Model | Task | Plain | Min | Rounds (final; best seen) |
|---|---|---|---|---|
| q35 | wrenfold | B06 54/54 | 9.1 | R104 12, R116 **54 at 21 min**, R128 48 |
| q35 | semver | B07 75/76 | 8.1 | R113 **75 at 4 min**, R125 75 at 27 min |
| q35 | itc | B04 0/42 (interval lists, not ITC) | 5.0 | R110 **17**, R122 2 |
| q35 | cobs | B05 41/44 | 48.8 | R107 37, R119 0, R131 3 |
| g26 | wrenfold | B08 54/54 | 12.4 | R108 0, R120 48, R132 51 (54 at 13 min) |
| g26 | semver | B09 75/76 | 5.1 | R105 0, R117 75 at 14 min, R129 27 (75 at t13) |
| g26 | itc | B10 0/42 (interval lists, not ITC) | 4.8 | R114 0, R126 **9** |
| g26 | cobs | B11 0/44 (no code: 3 turns of all-thinking, no tool call) | 15.9 | R111 3, R123 **35** |
| lfm24 | wrenfold | B12 54/54, **contaminated** | 7.3 | R112 0, R124 0 |
| lfm24 | semver | B13 62/76 | 3.9 | R109 0, R121 0 |
| lfm24 | itc | B14 0/42 (interval lists, not ITC) | 6.0 | R106 0, R118 0, R130 0 |
| lfm24 | cobs | B15 2/44 (an escape scheme, not COBS) | 3.3 | R115 0, R127 0 |

Plain tau beats or matches beagle on the two bounded tasks, wrenfold and semver, for every model. It
does so in a third to a half of the time, and with no runs at 0. Beagle comes out ahead only where
plain tau built the wrong thing: itc for q35 and g26 (17 and 9 against 0) and cobs for g26 (35 against
0). Even there its own scores are low. On lfm24 beagle never scored, while plain semver reached 62.
The goal is to beat plain tau on reliability and time, and on these runs beagle doesn't yet do that on
any pair.

**B12 is contaminated.** After fetching the spec, lfm24 ran `find / -name "*wrenfold*"`. It then
`cat` the harness's `wrenfold_ref.py`, `adapters/wrenfold_reference.py` and `adapters/wrenfold_broken.py`,
and checked its module against the reference. R109 (lfm24 semver), R124 (lfm24 wrenfold) and R130
(lfm24 itc) ran the same kind of `find /`, and their listings showed the harness's reference and
broken adapters. None of them read those files, and all three scored 0. No other run's tool calls
name a harness reference or grader file. The run directory can also reach earlier runs' finished
trees, such as `~/wrenfold.b06` (54/54) and `~/<task>.rNNN`. Runs need a sandbox that shows them only
the project, TAU_HOME, tau and beagle (bwrap is installed).
