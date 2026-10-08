"""Measure the TUI while text streams: CPU, event-loop stalls, layouts, GC.

Runs the real TauTuiApp headless (Textual's run_test pilot) with a FakeSession,
fills the transcript with history, then streams a fragment every --frag-ms into
a new assistant message and reports what that cost. Nothing in tau is patched
except the knobs named below, so the numbers describe the code as it ships.

Run it from the repo root, with a memory cap so a runaway layout loop cannot
take the machine down:

    systemd-run --user --scope -q -p MemoryMax=4G -p MemorySwapMax=0 \\
        uv run python dev-notes/tui-stream-cpu/lab/stream_probe.py --items 400

Output, one line per run:

    cpu%        process CPU time / wall time while streaming (100% = one core)
    layout/s    full screen reflows per second (Screen._refresh_layout calls)
    stall ...   how late a 5ms heartbeat woke: the time the event loop was
                blocked. p99/max are what a user feels as hitches; >16ms/s is
                dropped 60Hz frames per second, >50ms/s visible pauses.
    gen2        automatic full GC passes and the slowest one

--stacks also samples the main thread's stack whenever the loop has been blocked
for more than 40ms and prints the commonest stacks, which is how the long
pauses were traced to garbage collection rather than rendering.
"""

from __future__ import annotations

import argparse
import asyncio
import collections
import gc
import sys
import threading
import time
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(REPO / "src"), str(REPO / "tests")]

import textual.screen as textual_screen  # noqa: E402

import tau_coding.tui.app as tui_app  # noqa: E402
import tau_coding.tui.widgets as tui_widgets  # noqa: E402
from test_tui_app import FakeSession  # noqa: E402

layouts = [0]
_refresh_layout = textual_screen.Screen._refresh_layout


def _counting_refresh_layout(self, *args, **kwargs):  # type: ignore[no-untyped-def]
    layouts[0] += 1
    return _refresh_layout(self, *args, **kwargs)


textual_screen.Screen._refresh_layout = _counting_refresh_layout  # type: ignore[method-assign]


def fill(state, count: int) -> None:  # type: ignore[no-untyped-def]
    for index in range(count):
        role = ("user", "assistant", "tool", "thinking")[index % 4]
        state.add_item(role, f"history item {index} " + "lorem ipsum dolor sit amet " * 12)


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(len(ordered) * fraction))] if ordered else 0.0


class StackSampler:
    """Background thread that records the main thread's stack during long stalls."""

    def __init__(self) -> None:
        self.beat = time.perf_counter()
        self.armed = False
        self.samples: collections.Counter[str] = collections.Counter()
        self._main = threading.get_ident()
        threading.Thread(target=self._watch, daemon=True).start()

    def _watch(self) -> None:
        while True:
            time.sleep(0.01)
            if not self.armed or time.perf_counter() - self.beat < 0.04:
                continue
            frame = sys._current_frames().get(self._main)
            stack = traceback.extract_stack(frame)
            key = " < ".join(
                f"{f.name}({Path(f.filename).name}:{f.lineno})"
                for f in reversed(stack[-40:])
                if "asyncio" not in f.filename
            )
            self.samples[key[:900]] += 1


async def run(args: argparse.Namespace, sampler: StackSampler | None) -> None:
    tui_widgets.TRANSCRIPT_WINDOW_ITEMS = args.window
    tui_widgets.TRANSCRIPT_WINDOW_PAGE_ITEMS = max(1, args.window * 2 // 5)
    tui_widgets.TRANSCRIPT_WINDOW_OVERSCAN_ITEMS = max(1, args.window // 5)
    tui_widgets.STREAM_FLUSH_INTERVAL_SECONDS = args.flush_ms / 1000
    gc.unfreeze()
    gc.collect()

    app = tui_app.TauTuiApp(FakeSession())
    async with app.run_test(size=(120, 45)) as pilot:
        view = app.query_one("#transcript", tui_widgets.TranscriptView)
        theme = app.tui_settings.resolved_theme
        fill(app.state, args.items)
        view.update_from_state(app.state, theme=theme)
        await pilot.pause(1.0)
        mounted = len(view.children)
        if args.gc == "app":
            gc.unfreeze()  # undo the startup pass; collect what the history fill left
            tui_app._collect_garbage_while_idle()  # what the app does when a turn settles
        else:
            gc.unfreeze()

        gen2: list[float] = []
        gc_started = [0.0]

        def on_gc(phase: str, info: dict[str, int]) -> None:
            if phase == "start":
                gc_started[0] = time.perf_counter()
            elif info["generation"] == 2:
                gen2.append((time.perf_counter() - gc_started[0]) * 1000)

        gc.callbacks.append(on_gc)
        stop = False
        sent = [0]
        message = await view.start_assistant_message(theme=theme, scroll_end=True)

        async def feed() -> None:
            index = 0
            while not stop:
                await message.append_fragment("word\n\n" if index % 12 == 0 else "word ")
                sent[0] += 1
                index += 1
                await asyncio.sleep(args.frag_ms / 1000)

        lateness: list[float] = []

        async def heartbeat() -> None:
            while not stop:
                started = time.perf_counter()
                if sampler:
                    sampler.beat = started
                await asyncio.sleep(0.005)
                lateness.append((time.perf_counter() - started) * 1000 - 5)

        feeder = asyncio.create_task(feed())
        beat = asyncio.create_task(heartbeat())
        await asyncio.sleep(0.5)
        layouts[0] = 0
        sent[0] = 0
        lateness.clear()
        gen2.clear()
        if sampler:
            sampler.armed = True
        cpu_start, wall_start = time.process_time(), time.perf_counter()
        await asyncio.sleep(args.secs)
        cpu = time.process_time() - cpu_start
        wall = time.perf_counter() - wall_start
        if sampler:
            sampler.armed = False
        stalls = list(lateness)
        gc.callbacks.remove(on_gc)
        stop = True
        await beat
        await feeder
        await message.finalize()

    slowest_gc = f"{max(gen2):.0f}ms" if gen2 else "-"
    print(
        f"items={args.items} mounted={mounted} window={args.window} flush={args.flush_ms}ms "
        f"gc={args.gc} | cpu={cpu / wall * 100:4.1f}% frag/s={sent[0] / wall:3.0f} "
        f"layout/s={layouts[0] / wall:5.1f} | stall p50={percentile(stalls, 0.5):4.1f} "
        f"p99={percentile(stalls, 0.99):5.1f} max={max(stalls):5.1f}ms "
        f">16ms/s={sum(s > 16 for s in stalls) / wall:4.1f} "
        f">50ms/s={sum(s > 50 for s in stalls) / wall:4.1f} "
        f"| gen2={len(gen2)} slowest={slowest_gc}",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--items", type=int, default=400, help="history items before streaming")
    parser.add_argument(
        "--window",
        type=int,
        default=tui_widgets.TRANSCRIPT_WINDOW_ITEMS,
        help="TRANSCRIPT_WINDOW_ITEMS (page and overscan scale with it)",
    )
    parser.add_argument(
        "--flush-ms",
        type=float,
        default=tui_widgets.STREAM_FLUSH_INTERVAL_SECONDS * 1000,
        help="stream flush interval; 0 is roughly the old one-append-per-fragment behaviour",
    )
    parser.add_argument(
        "--gc",
        choices=("app", "none"),
        default="app",
        help="app: collect+freeze like a settled turn; none: plain automatic GC (pre-fix)",
    )
    parser.add_argument("--frag-ms", type=float, default=10, help="ms between fragments")
    parser.add_argument("--secs", type=float, default=6, help="measured seconds per run")
    parser.add_argument("--reps", type=int, default=2)
    parser.add_argument("--stacks", action="store_true", help="sample stacks during stalls")
    args = parser.parse_args()

    sampler = StackSampler() if args.stacks else None
    for _ in range(args.reps):
        asyncio.run(run(args, sampler))
    if sampler:
        print("commonest stacks while blocked >40ms (10ms samples):")
        for stack, count in sampler.samples.most_common(6):
            print(f"  {count:4d}  {stack}")


if __name__ == "__main__":
    main()
