# Beagle 0.48 — who carries tau's policy text

T0603's audit of the policy text in `examples/extensions/beagle.py` (the
driver and worker prompts, the `*_NOTE` texts, refusal wording and the
`Next:` lines tau writes), under the owner's rule "beagle decides, hosts
carry". Each text is weighed against what the pinned 0.48.0
(`~/beagle-wt/0.48`, 08e642c) puts in front of a model: the brief, `pursuit
rules`, its refusals, its `next:` lines, and the driver commands
(`pursuit.md`, `pursuit-run.md`) tau loads.

- **deleted**: 0.48 already says it, and its text reaches the model; tau's
  copy is gone.
- **kept**: a host's to carry (tau's tool names, its own dispatch and guards,
  turn caps, its UI and session lifecycle), or beagle's text never reaches
  the model under tau. The reason is given.
- **ask**: beagle should say it and 0.48 does not, or says it more vaguely
  than a small worker needs. Filed in `upstream-asks.md`; tau keeps its
  wording until beagle carries it.

The wait-protocol deletion rests on 0.48 retiring the bare `beagle loop
tick` as a release ("Releasing a wait is said, never implied", `loop.py`)
and adding named waits (`--wait-id`, `--clear-wait ID`). Tau's copy told
the driver to release with a bare tick, which 0.48 no longer does. With it
gone, the driver follows `pursuit-run.md`, so the extension now reads named
waits too (`_live_wait` takes `waits` beside `awaiting`), and its scope-guard
refusal and stopped-worker note name the tick that releases the wait.

| Text | Where / what carries it | Verdict | Why |
| --- | --- | --- | --- |
| `whatever its status` | `TAU_HOST_NOTE`, the dispatch bullet: "clear the wait with a bare tick whatever its status"; `pursuit-run.md` "When a worker returns, release its wait with `beagle loop tick --clear-wait T0007`" | deleted | 0.48's driver says how to release a wait, and a bare tick no longer releases one; tau's copy was wrong under 0.48. The bullet now says "release its wait as the driver says". |
| `the driver's believed wait` | `TAU_HOST_NOTE`: "record `beagle loop tick --awaiting … --for N --resuming-in N`, `--for` the driver's believed wait"; `pursuit-run.md` "While a worker is dispatched" (`--awaiting`, `--wait-id`, `--for`, `--resuming-in`) | deleted | `pursuit-run.md` follows the host mapping in the same turn and gives the 0.48 form with `--wait-id`; tau's older form lacked the id. |
| `the bare tick that clears it` | `TAU_HOST_NOTE`, the `pursuit_dispatch` bullet | deleted | Named the retired bare-tick release; now "declare no wait for it", since `pursuit_dispatch` returns within the turn. |
| `Read the work and the checks; change nothing.` | `AUDIT_NOTE`; 0.48's audit brief: "Change nothing: report." | deleted | The auditor gets beagle's brief (cut before "For the driver:"), which says it. |
| `End your report with one line: SOUND, or DEFECTS and how many.` | `AUDIT_NOTE`; 0.48's audit brief: "Then one line: SOUND, or DEFECTS and how many." | deleted | Same words in beagle's brief. Tau's copy also put the verdict last, against the brief's order (SOUND, then `PACE:`, then the open tree's line); `_audit` falls back to finding DEFECTS or SHORT anywhere. |
| `AUDIT_NOTE` (what is left) | "Do not run `beagle pursuit audit`: the session that sent you records what you report." | kept | Tau's `_audit` records the verdict itself and its worker guard refuses beagle; beagle's "For the driver:" paragraph is cut from the auditor's brief. |
| `TAU_HOST_NOTE` (the rest) | Preamble to the `/pursuit-run` driver turn | kept | Maps Claude Code's names to tau's (`pursuit_wakeup`, the `agent` tool, `steer_subagent`, `get_subagent_result`, `pursuit_dispatch`, worktree isolation, `${CLAUDE_PLUGIN_ROOT}`, hooks run in the extension): host-only facts. |
| `goes in a quoted heredoc` | `TAU_HOST_NOTE`, the prose-in-shell bullet | ask | Beagle's verbs take prose as shell arguments and nothing a driver reads says how to quote it (only `owe add --help`). Ask 8. |
| `AGENT_HOST_NOTE` | Prefix of every agent type translated from beagle's agents | kept | Tau's tool names (`read`, `write`, `edit`, `bash`), no MCP, the plugin root: host facts. |
| `ENDED_RUN_NOTE` | Leads the first `/pursuit-run` after a run whose tau session ended | kept | Tau's session lifecycle (workers and the wakeup end with the session) and its transcript paths. |
| `STOPPED_WORKER_NOTE` | Appended to a `stop_subagent` result while a wait stands | kept | Tau's tool, and a cancelled tau worker sends no notification. Its release now names 0.48's `--clear-awaiting` or `--clear-wait ID`. |
| `refusing to write` | `make_scope_guard`'s refusal | kept | Tau's guard on the driver while a worker holds the scope; it names tau's `steer_subagent`. Its release now names 0.48's tick. |
| `DRIVER_PROCEDURE` | Driver system prompt, fixed at load | kept | Maps beagle's three calls onto `pursuit_step`, `pursuit_plan` and `pursuit_driver`: tau's dispatch. Fixed text, so the prefix holds. |
| `DRIVER_STEERS_NOTE` | Driver system prompt and the founding result; rules core: "The orchestrator does not do the work", "a reconnaissance leaf, not inline research" | ask | Beagle's lines are vaguer than a 9B driver needs: it read the reference and reasoned past its output limit in every ITC trial. Ask 5. |
| `FOUND_FIRST_NOTE` | Steer after a request to set beagle up; `rules 1` says nothing on what comes before founding | ask | "Found first, the design is not a milestone, workers read the references" is beagle policy that 0.48 lacks. The six-setup-call guard it names is tau's. Ask 6. |
| `GIT_IDENTITY_NOTE` | Driver and worker system prompts; 0.48 says it only in the brief's commit steps and the `pursuit commit` refusal | kept | Tau strips the commit steps (`pursuit_step` commits) and never runs `pursuit commit`, so beagle's text does not reach the model under tau. |
| `_unconfirmed_refusal` | `pursuit_found` with no `user_confirmed`; `pursuit.md` §1 "Read them back to the user verbatim" | kept | Tau's `pursuit_found` tool stands in for §1's interview, which tau's driver does not load. Print mode is tau's UI, and 0.48 has no found verb by design. |
| `PIECE_BY_PIECE_NOTE` | Worker system prompt; the brief's habit "Write the code, then run it … A case traced in your head costs a whole reply" | ask | Beagle names the failure but not the way round it when the rule is unknown (cases first, one piece per turn, the one open question). Ask 7. |
| `NO_COMMIT_NOTE` | Replaces the brief's commit and claim steps (`_without_commit_steps`) | kept | `pursuit_step` commits on close and the worker guard refuses `git commit` and `pursuit commit`: tau's dispatch. |
| `Run every test, build and check capped and redirected, as a plain command` | Replaces the brief's `beagle contain run` habit (`_without_beagle_habits`) | kept | The worker guard refuses `beagle`; tau's bound (`_command_bound`) is the host's containment. |
| `_SCOPE_REFUSED` | "(writes outside it are refused)" on the brief's Scope line | kept | Tau's worker guard refuses those writes; beagle's aside says only that they are named at close. |
| `NO_BEAGLE_NOTE` | Every worker brief, and the cases brief | kept | Tau's worker guard and the reads it allows. |
| `_turn_cap_note` | End of every worker brief | kept | Turn caps and the bash timeout are tau's. |
| `WITNESS_NOTE` | Worker brief, when the check can be shown to refuse | kept | Under tau the worker names the defect and `pursuit_step` runs `prove`. The WITNESS block is the format tau parses; `rules 2d` addresses whoever runs `prove`. |
| `Each defect becomes work before more is opened` | `_audit`'s result after a DEFECTS verdict; beagle's "For the driver:" paragraph | kept | Tau has already run `audit --record` and cuts beagle's paragraph, which names that verb; the result says the same in `pursuit_plan` and `pursuit_step` terms. |
| `_cases_brief` | The cases worker's brief before a spec-tied open; "Run `beagle pursuit rules 2e` first" | ask | 0.48 briefs only open tasks, so tau writes this worker's instructions. Filed as ask 2 before this audit. |
| `ABANDON_HINT` | `pursuit_step` results for a duplicate task | kept | Names `pursuit_step`'s `abandon` argument. Beagle's route (`close --outcome abandoned`) is refused to the driver and rewritten by `_steer_resemblance`. |
| `_tau_next` | The "Next:" line of `pursuit_step` and `pursuit_plan` results | kept | Relays beagle's own `next:` move as the tau call that makes it; a move no tool makes is passed on verbatim. The fallback lines name tau tools. |
| `_rules_note` | Appended to a dispatch result when `dispatch.toml` has `model_rules` | kept | Tau reads `dispatch model --json`, which carries the rules but not beagle's stderr note; the note names tau's `model`, `provider` and `thinking` arguments. |
