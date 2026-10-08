# TUI CPU and pauses while text streams

While the agent streamed a reply into a long session, the TUI used most of a
CPU core and hitched visibly about once a second. This note covers how to
measure that kind of problem, what the causes turned out to be, what landed,
and how to restart the larger fix (virtual "band culling") that was tried and
shelved.

## What "slow" means here

Mean CPU was the reported symptom, but it hides what a user notices. Track
three things separately:

| metric | what the user feels | good |
|---|---|---|
| total CPU while streaming | fans, battery, a busy machine | well under one core |
| how often the UI stalls (>16ms, >50ms per second) | dropped frames, stutter | ~0 over 50ms |
| how long stalls last (p99, max) | keys that lag, scrolls that jump | p99 under one 60Hz frame (16ms) |

They have different causes. Here, layout work set the CPU, while one
infrequent, expensive operation (garbage collection) set the longest stalls.
A fix aimed at one metric can leave the others untouched.

## How to measure

[`lab/stream_probe.py`](lab/stream_probe.py) runs the real `TauTuiApp`
headless with the test suite's `FakeSession`, fills the transcript with
history, and streams a fragment every 10ms (a fast provider) into a new
assistant message. Run it from the repo root under a memory cap. A layout
loop can eat memory quickly, and the cap makes it fail fast instead of
swapping the machine:

```sh
CAP="systemd-run --user --scope -q -p MemoryMax=4G -p MemorySwapMax=0"
$CAP uv run python dev-notes/tui-stream-cpu/lab/stream_probe.py            # as shipped
$CAP uv run python dev-notes/tui-stream-cpu/lab/stream_probe.py \
    --window 200 --flush-ms 0 --gc none                                     # roughly pre-fix
$CAP uv run python dev-notes/tui-stream-cpu/lab/stream_probe.py --stacks   # who blocks the loop
```

What it measures, and how:

- **CPU**: `time.process_time()` over wall time during a 6-second window.
- **Stalls**: a task sleeps 5ms in a loop and records how late it woke up. That
  lateness is the time the event loop was blocked, which is exactly what delays
  keystrokes and frames. p50/p99/max and counts over 16ms and 50ms come from
  these samples.
- **Layouts/s**: counts calls to Textual's `Screen._refresh_layout`, a full
  reflow of the screen.
- **GC**: a `gc.callbacks` hook times every gen-2 (full) collection.
- **Who is blocking** (`--stacks`): a background thread samples the main
  thread's stack with `sys._current_frames()` whenever the heartbeat is more
  than 40ms late. One subtlety: the collector holds the GIL, so the sampler
  cannot run during a collection. Its samples bunch up at the moment GC
  finishes, inside the probe's own `on_gc` callback. A stack whose innermost
  frame is `on_gc` therefore means the stall was garbage collection.

Earlier in the investigation, a variant counted `Widget.refresh(layout=True)`
call sites to find *who* asked for each layout. Every one came from the
streaming Markdown append; nothing else in tau was forcing layouts.

Caveats. The pilot renders to nothing, so absolute numbers are lower than in
a real terminal, which also pays for writing output. Compare runs with each
other, not against a budget. Confirm any change in a real terminal too. Run
repeats (`--reps`): the max stall in particular varies run to run.

## What was wrong

### 1. A full layout per streamed fragment (CPU)

Textual's `Markdown.append` ends with `refresh(layout=True)`, and Textual 8.2.8
has no partial reflow: one changed widget makes the compositor re-arrange
every mounted transcript row. Textual's `MarkdownStream` appends whenever its
task wakes up, which under a fast provider is once per fragment. So CPU scaled
as (fragments per second) × (mounted rows).

Both factors mattered, but the first was the bigger lever. With only 8 rows
mounted, per-fragment appends still cost 42-44% CPU. Each append also parses
again and rebuilds Markdown blocks, independent of the row count.

### 2. Full garbage collections (the long pauses)

The 130-430ms stalls lined up one to one with Python's automatic gen-2
collections. A 400-item session tracks around 270,000 objects, and a full
collection walks all of them. Streaming allocates heavily, so collections
fired mid-stream. This did not depend on how many rows were mounted, and
rendering optimizations could not have touched it.

### 3. The mounted window size (per-layout cost)

`TranscriptView` mounts only a window of items. At 200 items (152 mounted
rows in the probe) each reflow cost a few milliseconds. That was enough to
push p99 past a 60Hz frame even after fixes 1 and 2.

## What landed

Three commits on `choong-dev`, one per cause:

| commit | change | where |
|---|---|---|
| `fd0bd79d` | `TranscriptMarkdownStream` replaces `MarkdownStream`. It shows the first fragment at once, then appends what has piled up at most every `STREAM_FLUSH_INTERVAL_SECONDS` (0.1s). | `tui/widgets.py` |
| `c98b5f6b` | `_collect_garbage_while_idle()` does `gc.unfreeze(); gc.collect(); gc.freeze()` after startup and on every `AgentSettledEvent`, deferred until after the next paint. Automatic collections during a turn then scan only what that turn created. | `tui/app.py` |
| `da73b977` | `TRANSCRIPT_WINDOW_ITEMS` 200 → 80 (page 80 → 32, overscan 40 → 16). | `tui/widgets.py` |

Results with `stream_probe.py` (400 history items, a fragment every 10ms, 6s
runs, ranges over repeats; measured 2026-10-08):

| configuration | CPU | layouts/s | p99 stall | max stall | >16ms/s | >50ms/s |
|---|---|---|---|---|---|---|
| pre-fix: window 200, per-fragment, plain GC | 77-82% | 32-38 | 166-203ms | 178-277ms | 3.3-5.2 | 1.2-1.5 |
| + coalescing only (window 200) | 35% | 15-16 | 16-17ms | 140-150ms | 1.7-2.3 | 0.7-0.8 |
| + coalescing + idle GC (window 200) | 30-32% | 16 | 18-24ms | 38-53ms | 3.3-4.7 | 0-0.2 |
| as shipped (window 80) | 23-25% | 17 | 12-14ms | 30-39ms | 0.5-0.8 | 0 |

In the pre-fix row the feeder only got 48 of its 100 fragments per second
through, because the loop was that busy.

Idle GC is a trade, not a pure win. It turns the rare 130-150ms full
collection into several 20-30ms ones: with the old heap frozen, few
long-lived objects count toward Python's gen-2 trigger, so it fires more
often but each pass is small. At window 200 that nudges p99 and frame drops
up slightly. The smaller window then brings them below where coalescing
alone left them.

Design notes, so the next change does not undo these by accident:

- **Coalescing**: `stop()` waits for an append already in flight before its
  final flush. `Markdown.append` reads its parse position *before* it takes its
  lock, so two overlapping appends can corrupt the parse. A test pins this
  (`test_transcript_markdown_stream_stop_lets_an_append_in_flight_finish`).
- **GC**: freezing alone would leak, because frozen objects are never
  collected. That is why every pass unfreezes first: a cycle among old objects
  is freed one settled turn late, never kept. Turning gen-2 off during turns
  was measured as slightly better (max stall ~19ms) and rejected: a long
  unattended turn could then grow memory without bound. `on_unmount`
  unfreezes. The tests stub the collection out in `tests/conftest.py`
  because it acts on the whole pytest process. The remaining 30-40ms max
  stalls are gen-2 passes over objects created during the current turn.
- **Window**: paging requires `PAGE < WINDOW`, because a shift keeps an item
  that was already mounted as its scroll anchor. Paging only happens when the
  view is scrolled to an edge, so 80 items is still several screens of
  scrollback.

Going further along the same lines, a 40-item window measured ~18% CPU and
p99 ~9ms against ~24% and ~10ms at 80, in an earlier probe with gen-2
deferred rather than frozen. That is the cheapest next step if 80 proves
heavy in a real terminal (`stream_probe.py --window 40`).

## Textual 8.2.8 facts learned the hard way

- `Widget.refresh(layout=True)` anywhere means a full-screen reflow on the next
  frame; there is no per-widget reflow. Count `Screen._refresh_layout` calls to
  see them.
- `visible = False` still takes part in layout (it is just not drawn).
  `display = False` / `display: none` skips layout but also collapses the
  widget's height out of the scrollable virtual size.
- Scrolling by wheel, page keys, `scroll_end` and `scroll_to` all funnels
  through `scroll_to`, which makes that the one place to translate
  coordinates. `scroll_to_widget` works from widget regions and is the safe way
  to restore a position after rows above the viewport change.
- There is no `refresh_layout()` (use `refresh(layout=True)`), `Region` has `.y`
  not `.top`, and the method is `scroll_home` not `page_home`.
- `MarkdownStream` builds a fresh Markdown parser on every append.

## Band culling (shelved)

### What it is

Keep only a small band of rows mounted around the viewport (~96 items), and
represent everything above and below with spacer widgets whose height is the
sum of the unmounted items' heights. Reflow cost then depends on the band, not
on the transcript. It targets cause 1's row-count factor and nothing else.

It was built over about 11 hours in a tau session (07122c87, 2026-10-07/08)
before throttling had been tried, even though that session's own findings had
recommended trying throttling first.

### Why it is shelved

After the three fixes above, the most it could still win is the gap between a
window of 80 and a much smaller one: about 24% → 18% CPU and 13 → 9ms p99.
It would not help the max stall (GC) at all. Against that, it rewrites
scrolling, which is the most delicate part of the transcript. That
complexity is not worth 6 points of CPU unless something changes; see "When
to revisit" below.

### Files

- [`lab/band-culling.patch`](lab/band-culling.patch): the port into
  `widgets.py` as left by that session (+707 lines). It renames the original
  class to `TranscriptViewBase` and adds a culling `TranscriptView` subclass.
  It applies to `0902aa20`, the commit before the fixes above, and not to the
  current `widgets.py`.
- [`lab/culllab9.py`](lab/culllab9.py): the standalone lab where the mechanism
  works. It wraps the real `TranscriptView` in a culling subclass and runs
  baseline vs culled, printing CPU, key lag, mounted rows and pass/fail for
  scroll probes (`up`, `pgup`, `top`, `mid`, `follow`). `-v` traces the retune
  loop. Its CPU numbers predate coalescing.
- [`lab/findings-2026-10-07.md`](lab/findings-2026-10-07.md): that session's own
  findings (mechanism, early numbers, open correctness issues).

### The design and its invariants

- `scroll_y` is band-relative. Absolute transcript coordinates enter only
  through an overridden `scroll_to` (one translation boundary) and leave
  through one helper.
- **Window invariant**: mounted rows are exactly the widgets for
  `items[window_start:window_end]`, in order. Check it cheaply (count and
  identity at both ends) and rebuild when it breaks, rather than patching
  around it.
- **Height ledger**: per item, the measured `region.height + margin.top` while
  mounted and an estimate (8 lines) before that. The spacer height is always
  recomputed as a sum from the ledger, never accumulated.
- **Anchoring**: every band mutation ends by re-anchoring to a surviving,
  item-bearing widget (`scroll_to_widget`), never to a remembered coordinate.
- **Follow mode**: "at the end" means `window_end == len(items)` *and*
  `is_vertical_scroll_end`. A follow flag set while the band is not at the end
  must be cleared, or the view loops snapping to the bottom.
- A retune loop (`watch_scroll_y` → `call_after_refresh`) grows the band when
  the viewport nears its top, trims it past a cap, and serves scroll requests
  that landed outside the band by sliding the window, then re-asserting the
  absolute position. Batches of ~24 items give hysteresis.
- Rows without an item (the streaming message, the hidden-thinking
  placeholder) must sit at the band's end and never be dropped or counted.

### Where it broke

The lab works because it controls the whole lifecycle. The port does not,
because the base class's incremental paths (`append_item`,
`append_thinking_delta`, `update_thinking_visibility`, and the `_redraw` in
`update_from_state`) all assume *window == mounted rows*, and culling breaks
that. The session tried two strategies:

1. Let the base's incremental paths run, then retune. This broke
   hidden-thinking and streaming: for example, `add_item("assistant")`
   finalizes the thinking stream widget and leaves a raw row that later comes
   back.
2. Gate `update_from_state` on "window agrees with rows" and fall back to a
   full redraw otherwise. This regressed ~40 tests, probably because the check
   was wrong about transient widgets, or about hidden thinking items, which
   legitimately have no row.

There was also nondeterminism: the same lab run alternated between snapping
and chasing. The likely cause is a race between after-refresh restores and
retune scheduling. The fix it pointed at was one arbiter, with one pending
band operation at a time.

With the patch applied at `0902aa20`, `tests/test_tui_app.py` no longer
finishes in reasonable time: after 400s it had reached 55%, with 200 passed
and 46 failed (unpatched, the whole file takes ~100s). The failures reach
well beyond scrolling: sidebar toggles, compaction status, pickers, slash
command completion, the activity indicator. Anything that redraws the
transcript while the band is out of step with the window goes wrong. Expect
to fix that general problem before chasing individual tests.

The tests that are hardest to keep green (all in `tests/test_tui_app.py`):

- `test_long_transcript_mounts_bounded_latest_window_and_pages_earlier`: pins
  production paging (`_window_start` values with a window of 6). The band has
  to be an extra, smaller mount set beneath production paging, not a
  replacement for it.
- `test_tui_streaming_deltas_update_active_message_without_full_refresh`
- `test_tui_app_toggles_thinking_tokens_from_keybinding_while_running`
- `test_tui_app_hidden_thinking_placeholder_gives_way_to_the_streamed_answer`
- `test_tui_app_hidden_thinking_status_line_does_not_accumulate_across_turns`

The base also owns widgets outside the item ledger: `_hidden_thinking_widget`,
`_active_assistant_widget`, `_active_thinking_widget` and
`_active_message_widgets`. The band must never evict them, and they must not
define the window's span.

### How to restart it

```sh
git worktree add ../tau-cull 0902aa20 && cd ../tau-cull
git apply ../tau/dev-notes/tui-stream-cpu/lab/band-culling.patch
uv run pytest -q tests/test_tui_app.py -k "thinking or window or scrollback or streaming"
uv run python ../tau/dev-notes/tui-stream-cpu/lab/culllab9.py      # lab, -v to trace
```

Then rebase onto the current code. The new streaming class and window
constants touch the same file. The open design problem is the first thing to
solve, before chasing individual tests: make the band the single owner of
which rows are mounted, and have the base's incremental paths go through it
instead of mounting and unmounting rows themselves. Keep the lab's comments;
they hold the coordinate invariants.

### When to revisit

- Real-terminal profiling shows layout cost at 80 mounted rows still hurts,
  and a 40-item window has been tried and found too short for scrollback.
- Rows get much more expensive to lay out (rich tool output, images), so the
  per-row cost grows rather than the count.
- Textual gains partial reflow or virtualized containers. Check that first;
  it could make culling unnecessary or much simpler.

## Lessons for the next performance problem like this

- Measure all three metrics before designing anything. Mean CPU alone would
  have hidden the GC pauses, which no rendering change could fix.
- Break the cost into factors (rate × per-item cost × count) and try the cheap
  knob on each factor first. A 30-line throttle beat 700 lines of
  virtualization on CPU.
- Attribute stalls before guessing. A stack sampler plus GC callbacks found a
  cause that had nothing to do with rendering.
- Check whether the framework already does the expensive thing per event
  (`MarkdownStream` appends per wake) before building around it.
- Run probes memory-capped, repeat them, and confirm the result in a real
  terminal.
