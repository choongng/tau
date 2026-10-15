# PR draft: TUI streaming CPU

Branch `upstream/tui-stream-cpu` (on urd), based on huggingface/tau `main` at
`c41aacf7`. These notes are for us; the PR text starts at the rule below.

Before opening:

- [ ] Fork huggingface/tau on GitHub, push the branch to the fork and open the
      PR against `main`.
- [ ] Check the change by hand in a real terminal: stream a long reply into a
      session with a long history; scroll up through the transcript; press
      Ctrl+T while text is streaming.
- [ ] Decide whether to include the probe script. As written, the description
      offers to add it. `dev-notes/tui-stream-cpu/lab/stream_probe.py` runs
      unchanged on the branch. Against plain `main`, it needs
      `getattr(tui_widgets, "STREAM_FLUSH_INTERVAL_SECONDS", 0)`, because that
      constant doesn't exist there.
- [ ] If upstream `main` has moved, rebase the branch and run the checks again.
      Rebasing this branch is fine: it holds only these three commits.

---

**Title:** Cut TUI CPU use and UI stalls while streaming into a long transcript

## Motivation

When a session has a long history, the TUI keeps most of a core busy while a
reply streams in, and the UI stalls for 100–200 ms about once a second. There
are two causes:

- **Every streamed fragment triggers a full layout.** Textual's `MarkdownStream`
  appends once per provider fragment, which is roughly one per token, or
  50–150 a second. Each append re-lays out every mounted transcript row. With
  200 rows mounted, the event loop can't keep up: in the measurements below,
  only about half of the fragments reach the screen as they arrive.
- **Python's automatic full garbage collection.** A long session holds a few
  hundred thousand objects. A gen-2 collection walks all of them, which takes
  100–400 ms, and it tends to fire while text is streaming because streaming
  allocates heavily.

## Changes

Three commits. Each can be reviewed on its own.

1. **Coalesce streamed text** (`tui/widgets.py`)
   - A new `TranscriptMarkdownStream` replaces the use of `MarkdownStream` for
     transcript messages.
   - It renders the first fragment at once, then appends whatever has piled up
     at most every `STREAM_FLUSH_INTERVAL_SECONDS` (0.1 s).
   - `stop()` waits for an append already in flight before its final flush,
     because `Markdown.append` reads its parse position before taking its lock.
2. **Collect garbage when the agent settles** (`tui/app.py`)
   - After startup, and on every `AgentSettledEvent`, the app runs
     `gc.unfreeze(); gc.collect(); gc.freeze()`, scheduled after the next
     refresh.
   - Automatic collections during a turn then scan only what that turn created.
   - Each pass unfreezes first, so cycles among older objects are still
     collected, one turn late. The app unfreezes everything when it exits.
3. **Mount 80 transcript items instead of 200** (`tui/widgets.py`)
   - `TRANSCRIPT_WINDOW_ITEMS` goes from 200 to 80.
   - Paging scales with it: `TRANSCRIPT_WINDOW_PAGE_ITEMS` goes from 80 to 32,
     and `TRANSCRIPT_WINDOW_OVERSCAN_ITEMS` from 40 to 16. The page size has to
     stay below the window size, since paging keeps an already-mounted item as
     its scroll anchor.
   - Paging only starts at the scroll edge, so 80 items still leaves several
     screens of scrollback.

## Measurements

The measurements use a headless probe:

- It runs the real `TauTuiApp` through Textual's `run_test`, with the test
  suite's `FakeSession`.
- It fills the transcript with 400 history items, then streams a fragment
  every 10 ms into a new assistant message.
- **CPU** is process time over wall time across 6 s.
- **Stalls** come from a task that sleeps 5 ms in a loop and records how late
  it wakes up.

Each row is three runs.

| | CPU | p99 stall | max stall | fragments shown / s (of 100) |
|---|---|---|---|---|
| `main` | 58–60% | 107–161 ms | 166–188 ms | 48–50 |
| this branch | 16% | 8–9 ms | 13–25 ms | 91–92 |

With all three changes switched off, this branch measured the same as `main`
(57–63% CPU, p99 112–168 ms).

When we measured the three changes one at a time on our working branch:

- Coalescing alone cut CPU by roughly half.
- Idle-time collection cut the worst stalls from 140–150 ms to 40–50 ms.
- The smaller window cut both CPU and stalls a further 20–40%.

Headless numbers leave out the cost of writing to a terminal, so they are
useful for comparing runs, not as absolute figures. I can add the probe script
under `dev-notes/` if that would help review.

## Tests and checks

New tests:

- `test_transcript_markdown_stream_coalesces_fragments_between_flushes`
- `test_transcript_markdown_stream_stop_lets_an_append_in_flight_finish`
- `test_collect_garbage_while_idle_frees_cycles_frozen_by_an_earlier_call`
- `test_tui_app_collects_garbage_at_startup_and_when_agent_settles`

A `conftest.py` fixture, `skip_idle_garbage_collection`, stubs out the
collection in the other TUI tests, because a real collection would act on the
whole pytest process.

Checks run:

```
uv run pytest            # 2063 passed, 3 skipped
uv run ruff check .      # All checks passed
uv run ruff format --check .
uv run mypy              # no issues in 123 source files
```

## Compatibility

- **No config changes and no new dependencies.**
- **Streamed text shows up to 100 ms later.** That still means at most about 10
  updates a second. The first fragment of each message still shows at once.
- **`gc.freeze()` acts on the whole process.** It runs only inside the TUI app,
  not in print mode or the library, and the app unfreezes everything when it
  exits.
- **Fewer rows stay mounted.** Scrolling back past 80 items pages earlier rows
  in, as it already did past 200.
