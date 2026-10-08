"""Trial v9: anchored band with the window invariant enforced.

Invariant I1 (the only legal window state):
    rows == widgets for items[ws:we]        (row order == item order)
The retuner verifies I1 cheaply (row count and item identity at both ends)
and REBUILDS rows from the window when it breaks, instead of papering over.
Anomalous transitions get logged so the root cause surfaces.

Invariant I2: band_above == sum(heights(items[:ws]))  (recomputed, never
accumulated).

Invariant I3: band mutations end by re-anchoring to a surviving item-bearing
WIDGET (scroll_to_widget), never to a remembered coordinate.

Invariant I4: follow mode is production's. "At end" means _window_end ==
len(items) AND is_vertical_scroll_end. Band-relative max_scroll_y never
appears in an at-end test.
"""
import asyncio, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tests"))
import textual.widget as twidget
import tau_coding.tui.app as tapp
from tau_coding.tui.app import TauTuiApp
from test_tui_app import FakeSession

marks = []
orig_changed = tapp.TauTuiApp.on_text_area_changed
def changed(self, event):
    if event.text_area.id == "prompt":
        marks.append(time.perf_counter())
    return orig_changed(self, event)
tapp.TauTuiApp.on_text_area_changed = changed

DEBUG = "-v" in sys.argv

# Production window sizes rows in ITEMS (TRANSCRIPT_WINDOW_ITEMS), not in
# rows: one item renders as several rows, and with hidden thinking an item
# expands to its full detail when the window comes over it. Our band is
# item-sized like production's, only smaller, and every height in the ledger
# is an ESTIMATE for unmounted items.
GUESS = 8           # height estimate for an unmeasured item (rows)
BAND_CAP = 96       # band soft cap in ITEMS
BATCH = 24          # items per grow/drop step
KEEP = 16           # rows kept above the viewport when trimming front
MAX_ROWS = 220      # hard row ceiling (production keeps 200 items)

ANOMALIES = []


def cont_h_of(w):
    return max(w.container_size.height, 1)


def make_culled(base_cls):
    class CulledTranscriptView(base_cls):
        def __init__(self, *args, **kwargs):
            self._pending_edge = False
            self._pending_abs = 0.0
            self._band_request = False
            self._band_pending = None
            super().__init__(*args, **kwargs)
            self._heights = {}
            self._item_index = {}
            self._pending = False
            self._in_op = False
            self._grew_last = False

        def _log_anomaly(self, msg):
            ANOMALIES.append(msg)
            if DEBUG:
                print(f"    [ANOMALY] {msg}: rows={len(self._rows())} "
                      f"ws={self._window_start} we={self._window_end}")

        def _rebuild_rows(self):
            """Production redraw with our window bounds."""
            self._redraw(scroll_end=self._follow_output, preserve_window=True)
            self._sync_boundaries()

        # ---- I2: virtual height and the coordinate boundary ----
        def _derive_above(self):
            """above = sum of ledger heights of items OUTSIDE the window.
            Ledger entries for mounted rows are measured (exact); outside the
            window they are estimates. The band's own items are NEVER in
            `above`, by construction."""
            state = self._render_state
            if state is None:
                return 0
            # EXACT ledger: sum of ledger heights of items OUTSIDE the window.
            # No extent subtraction: that made the virtual top disagree with
            # _band_top_absolute(), and scroll translation then clamped
            # legitimate positions to 0. Spacer height == this sum, so
            # textual's max_scroll_y == above + extent - cont_h is coherent.
            return sum(self._height_of(it)
                       for it in state.items[:self._window_start])

        def get_content_height(self, container, viewport, width):
            # spacer-carrying band: super()'s sum (rows + spacer heights) IS
            # the virtual height; no ledger offset here.
            return super().get_content_height(container, viewport, width)



        def _band_top_absolute(self):
            state = self._render_state
            if state is None:
                return 0
            return sum(self._height_of(it) for it in state.items[:self._window_start])

        def _band_bottom_absolute(self, state):
            return self._band_top_absolute() + self._band_extent()

        def _band_extent(self):
            """Measured height of the mounted band (spacer to spacer)."""
            rows = self._rows()
            if not rows:
                return 0
            first, last = rows[0], rows[-1]
            # trust ledger when regions are not laid out (height 0)
            ext = ((last.region.y + (last.styles.margin.top or 0)
                    + last.region.height)
                   - first.region.y)
            if ext <= 0:
                ext = sum(self._height_of(self._item_of(r))
                          for r in rows if self._item_of(r) is not None)
            # bottom spacer (mounted, unmeasured) counts as an empty row in
            # region math; the band is items only
            return ext - 1

        def _band_rel(self, y):
            """Translate an ABSOLUTE content y to band-relative, using the
            CURRENT layout: current scroll_y plus the delta between the
            absolute target and the absolute position of the viewport top.
            Works no matter which coordinate system the caller is in — it
            only ever moves by (target - current_absolute)."""
            top_boundary = self._top_boundary
            if top_boundary is None or not top_boundary.region.height:
                # no spacer: content coords already are band coords
                return max(0.0, min(float(y), float(self.max_scroll_y)))
            abs_now = self.scroll_y + top_boundary.region.height
            band = self.scroll_y + (float(y) - abs_now)
            return max(0.0, min(band, float(self.max_scroll_y)))

        def _abs_now(self):
            """Absolute transcript y currently under the viewport top."""
            tb = self._top_boundary
            return self.scroll_y + (tb.region.height if tb is not None else 0)

        def _set_abs(self, target, *, force_edge=False):
            """Scroll so absolute `target` is at the viewport top.

            The coordinate system is content = spacer + rows, so this is a
            single subtraction; no external caller should compute offsets.
            Clamped to what the band can show, and _pending_edge records
            that the request could not be fully served (the retune loop
            then moves the band toward it)."""
            band = float(target) - self._abs_now() + self.scroll_y
            clamped = band < -0.5 or band > self.max_scroll_y + 0.5
            band = max(0.0, min(band, float(self.max_scroll_y)))
            if clamped and force_edge:
                self._pending_edge = True
            self._scroll_band(band)
            return not clamped

        def _serve_edge_request(self, pairs, rows, cont_h):
            """Window slide toward an absolute target the band cannot show.

            The viewport sits at a band edge because the request clamped
            there; the target lies outside the band, so the WINDOW moves
            toward it one batch per tick. The viewport content is anchored
            through the operation: _shift_window moves items in or out at
            both edges and re-establishes the same absolute position at
            the end, whatever the spacer did meanwhile."""
            state = self._render_state
            if state is None or not pairs:
                return False
            state = self._render_state
            if state is None:
                self._pending_edge = False
                return False
            total = len(state.items)
            target = self._pending_abs
            if target is None:
                self._pending_edge = False
                return False
            now = self._abs_now()
            if target < now:
                if self._window_start <= 0:
                    self._pending_edge = False
                    return False
                n = min(BATCH, self._window_start)
                self._shift_window(-n)
                if DEBUG:
                    print(f"      [serve] slide front n={n} "
                          f"ws={self._window_start} we={self._window_end} "
                          f"now={self._abs_now():.0f}")
                return True
            band_bottom = now + self._band_extent()
            if target > band_bottom and self._window_end < total:
                n = min(BATCH, total - self._window_end)
                self._shift_window(n)
                if DEBUG:
                    print(f"      [serve] slide end n={n} "
                          f"ws={self._window_start} we={self._window_end}")
                return True
            self._pending_edge = False
            if DEBUG:
                print("      [serve] cleared")
            return False

        def _shift_window(self, n):
            """Move the window n items in one direction (n<0: toward item
            0), keeping the band size within its cap and the viewport
            anchored to the same absolute content.

            n<0: mount -n items at the front; if that puts the band over
            its cap, unmount the overflow from the END (the viewport is at
            the band front edge — the end rows are off-screen).
            n>0: mount n at the end; if over cap, unmount the overflow from
            the FRONT only when those rows are off-screen (viewport deep in
            the band); otherwise the slide cannot proceed.
            Anchor: after mounting/dropping, the absolute position is
            re-asserted through the boundary, which reads the fresh spacer.
            """
            state = self._render_state
            if state is None or n == 0:
                return False
            total = len(state.items)
            abs_before = self._abs_now()
            if n < 0:
                n = min(-n, self._window_start)
                if n <= 0:
                    return False
                self._mount_items_front(n)
                overflow = (self._window_end - self._window_start) - BAND_CAP
                if overflow > 0:
                    self._unmount_end(overflow)
            else:
                n = min(n, total - self._window_end)
                if n <= 0:
                    return False
                self._mount_items_end(n)
                overflow = (self._window_end - self._window_start) - BAND_CAP
                if overflow > 0:
                    self._unmount_front_keep(overflow)
            self.call_after_refresh(
                lambda t=abs_before: self.scroll_to(
                    y=t, animate=False, immediate=True, force=True))
            return True

        def _mount_items_front(self, count):
            state = self._render_state
            count = min(count, self._window_start)
            if count <= 0:
                return
            new_items = state.items[self._window_start - count:self._window_start]
            widgets = [w for it in new_items
                       if (w := self._widget_for_item(it)) is not None]
            self._window_start -= len(new_items)
            rows = self._rows()
            if widgets:
                if rows:
                    self.mount(*widgets, before=rows[0])
                else:
                    self.mount(*widgets, before=self._bottom_boundary)
            self._sync_boundaries()

        def _mount_items_end(self, count):
            state = self._render_state
            total = len(state.items)
            count = min(count, total - self._window_end)
            if count <= 0:
                return
            items = state.items[self._window_end:self._window_end + count]
            widgets = [w for it in items if (w := self._widget_for_item(it)) is not None]
            self._window_end += len(items)
            if widgets:
                self.mount(*widgets, before=self._bottom_boundary)
            self._sync_boundaries()

        def _unmount_rows(self, rows):
            for r in rows:
                it = self._item_of(r)
                if it is not None:
                    self._item_widgets.pop(id(it), None)
                r.remove()

        def _unmount_end(self, count):
            rows = self._rows()
            doomed = rows[len(rows) - min(count, max(0, len(rows) - 1)):]
            self._unmount_rows(doomed)
            self._window_end -= len(doomed)
            self._sync_boundaries()

        def _unmount_front_keep(self, count):
            """Unmount from the band front but never past the viewport:
            rows within KEEP of the first visible row stay."""
            rows = self._rows()
            cont_h = max(self.container_size.height, 1)
            first_vis = self._first_visible(rows, cont_h)
            allowed = max(0, first_vis - KEEP)
            doomed = rows[:min(count, allowed)]
            self._unmount_rows(doomed)
            self._window_start += len(doomed)
            self._sync_boundaries()

        def scroll_to(self, x=None, y=None, **kwargs):
            """Coordinate boundary. Callers arrive in two systems:

            * absolute transcript y — textual's own page/line/home helpers
              and any code that treats the view as its full virtual range
              (which it is: spacer + band + spacer adds up exactly);
            * band-relative y — our own band operations, which pass
              _in_op=True or _band_request=True and bypass translation.

            No heuristic is needed to tell them apart: everything arriving
            without a marker is absolute, because the virtual range is the
            only coordinate system the outside world can see. The band
            serves what it can and the retune loop moves the band toward a
            clamped request."""
            if y is not None and not self._in_op and not self._band_request:
                tb = self._top_boundary
                sp = tb.region.height if tb is not None else 0
                band = float(y) - sp
                clamped = band < -0.5 or band > self.max_scroll_y + 0.5
                band = max(0.0, min(band, float(self.max_scroll_y)))
                self._pending_edge = clamped
                self._pending_abs = float(y)
                if DEBUG:
                    print(f"    [scroll_to] y={float(y):.0f} sp={sp} "
                          f"-> band={band:.0f} (sy={self.scroll_y:.0f} "
                          f"max={self.max_scroll_y:.0f} clamped={clamped})")
                kwargs["immediate"] = True
                y = band
            if self._band_request:
                self._band_request = False
            self._schedule_retune()
            return super().scroll_to(x, y, **kwargs)

        def _scroll_band(self, band_y):
            """Scroll to a band-relative position (our own operations).

            A band write may legitimately exceed max_scroll_y as measured
            right now, when the spacer is about to grow this very tick:
            textual clamps writes against the OLD max, so the write waits
            for the new layout."""
            self._band_request = True
            self._band_pending = float(band_y)
            self.refresh(layout=True)
            self.call_after_refresh(self._write_band_pending)

        def _write_band_pending(self):
            v, self._band_pending = self._band_pending, None
            if v is None:
                return
            self._band_request = True
            self.scroll_to(y=min(v, float(self.max_scroll_y)),
                           animate=False, immediate=True, force=True)

        def scroll_home(self, **kwargs):
            if not self._in_op:
                kwargs["animate"] = kwargs.get("animate", False)
                kwargs["immediate"] = True
                self._schedule_retune()
                return self.scroll_to(y=0, **kwargs)
            return super().scroll_home(**kwargs)

        def scroll_end(self, **kwargs):
            # the transcript's end IS the band's end (band ends at state end
            # whenever follow is meaningful); keep the base behavior.
            self._schedule_retune()
            return super().scroll_end(**kwargs)

        def scroll_end(self, **kwargs):
            self._schedule_retune()
            return super().scroll_end(**kwargs)

        # ---- rows / ledger ----
        def _rows(self):
            return [c for c in self.children
                    if isinstance(c, twidget.Widget)
                    and c is not self._top_boundary and c is not self._bottom_boundary]

        def _item_of(self, row):
            return getattr(row, "item", None)

        def _measure(self):
            for r in self._rows():
                try:
                    h = r.region.height
                except Exception:
                    continue
                if not h:
                    continue
                self._heights[id(r)] = h
                item = self._item_of(r)
                if item is not None:
                    self._heights[id(item)] = h + (r.styles.margin.top or 0)

        def _height_of(self, item):
            return self._heights.get(id(item), GUESS)

        # ---- I1 check + rebuild ----
        def _expected_items(self):
            state = self._render_state
            if state is None:
                return []
            win = state.items[self._window_start:self._window_end]
            # the base render skips hidden thinking blocks except the last
            # item; anything else in-window is expected to have a row
            win = state.items[self._window_start:self._window_end]
            # hidden thinking renders no row, EXCEPT when it is the final
            # item: the transient placeholder row is owned by the window
            last = state.items[-1] if state.items else None
            return [it for it in win
                    if not (it.role == "thinking" and not state.show_thinking
                            and it is not last)]

        def _rows_of_state(self):
            """One pass: drop rows whose item left the state, return the
            remaining (row, item_index) pairs. State order IS row order: the
            renderer appends, we append; gaps are hidden-thinking items,
            which production removes together with their rows."""
            state = self._render_state
            if state is None:
                return []
            index = {id(it): i for i, it in enumerate(state.items)}
            out = []
            for r in list(self._rows()):
                from tau_coding.tui.widgets import TranscriptWindowBoundary
                if isinstance(r, TranscriptWindowBoundary):
                    continue
                it = self._item_of(r)
                if it is None:
                    continue  # placeholder: transient, not bookkept
                idx = index.get(id(it))
                if idx is None:
                    self._item_widgets.pop(id(it), None)
                    r.remove()
                    continue
                out.append((r, idx))
            return out

        def _sync_window_to_rows(self):
            """Window := span of mounted rows. Any out-of-span stray row is
            unmounted. Returns list of (row, idx)."""
            pairs = self._rows_of_state()
            if not pairs:
                return []
            lo = min(i for _, i in pairs)
            hi = max(i for _, i in pairs)
            self._window_start = lo
            self._window_end = hi + 1
            for r, i in list(pairs):
                if i < lo or i > hi:
                    it = self._item_of(r)
                    if it is not None:
                        self._item_widgets.pop(id(it), None)
                    r.remove()
                    pairs.remove((r, i))
            return pairs

        def _schedule_retune(self, *, now=False):
            if self._pending:
                return
            self._pending = True
            if now:
                self.call_next(self._retune_tick)
            else:
                self.call_after_refresh(self._retune_tick)

        async def _retune_tick(self):
            self._pending = False
            if not self.is_mounted or self._in_op:
                return
            self._in_op = True
            try:
                mutated = await self._retune_once()
                if DEBUG and mutated:
                    print(f"      [mutated] -> reschedule sy={self.scroll_y:.0f}")
            except Exception:
                import traceback
                traceback.print_exc()
                self._log_anomaly("retune-exception")
                mutated = False
            finally:
                self._in_op = False
            if mutated and self.is_mounted:
                self._schedule_retune()
            elif DEBUG and self._pending_edge:
                print("      [pending-edge] not served, loop stops")
            if DEBUG:
                print(f"      [tick end] mutated={mutated} pending={self._pending}")

        async def _retune_once(self):
            state = self._render_state
            if state is None or not state.items:
                return False
            pairs = self._sync_window_to_rows()
            self._measure()
            rows = self._rows()
            total = len(state.items)
            cont_h = max(self.container_size.height, 1)
            n_items = len(pairs)

            tb = self._top_boundary
            sp = (tb.region.height if tb is not None and tb.region.height else 0)
            if DEBUG:
                print(f"    [retune] rows={len(rows)} items={n_items} "
                      f"ws={self._window_start} we={self._window_end} "
                      f"above={self._derive_above()} spacer={sp} "
                      f"follow={self._follow_output} "
                      f"sy={self.scroll_y:.0f} max={self.max_scroll_y:.0f} "
                      f"ext={self._band_extent()} vs={self.virtual_size.height} "
                      f"state_items={total}")

            # absolute-end: viewport at the true bottom of the virtual range
            # Follow means: pinned to the true bottom of the virtual range.
            # That is the ONLY way into the follow path — a follow flag left
            # over from production's render, with the viewport anywhere
            # else, must not drive band growth toward the state end (that
            # loop pins the band at the end and wedges user scroll).
            # The truth about bottom is the WINDOW, not the virtual range:
            # a full spacer makes max_scroll_y a fiction until the band
            # grows. Follow is meaningful exactly when the band ends at the
            # state end (or nothing remains after it).
            end_known = self._window_end >= total
            at_end = end_known and (
                self._follow_output
                or self.is_vertical_scroll_end
                or self.max_scroll_y - self.scroll_y < 2)
            if DEBUG:
                print(f"      [at_end] {at_end} end_known={end_known} "
                      f"flag={self._follow_output} vse={self.is_vertical_scroll_end} "
                      f"pend_edge={self._pending_edge}")
            # The widget IS the virtual range: textual's own arithmetic on
            # spacer + rows is coherent and complete. A request outside the
            # band is served by GROWING the band to cover it, which the
            # retune loop below does; clamping here would pin a request at
            # a band edge before the band can move.

            if at_end:
                # Serving follow means the band ENDS at the state end and
                # the viewport sits at the bottom of the content. It does
                # NOT mean the band is full: mounting every streamed
                # fragment one row at a time is what makes streaming O(N)
                # in mounted widgets. Settle the band to exactly the cap at
                # both edges (batched), then fall through to the shared
                # near-edge growth so new items mount batch-wise, never
                # one per tick.
                if self._window_end < total and n_items <= BAND_CAP:
                    self._grow_end(min(BATCH, total - self._window_end))
                    return True
                over = n_items - BAND_CAP
                if over > 0 and self._window_start > 0:
                    # over cap: give the front back in BATCH-sized steps,
                    # viewport re-pinned to the absolute bottom after
                    n = self._count_for_rows(
                        pairs, min(over + BATCH, self._window_start))
                    if n <= 0:
                        return False
                    self._drop_front(n, anchor=False)
                    self.call_after_refresh(
                        lambda: self.scroll_to(y=10 ** 9, animate=False,
                                               immediate=True, force=True))
                    return True
                # settled at the end and within cap: fall through to the
                # user-driven policy below for the small growth cases

            # ---- user-driven viewport ----
            # The viewport sits at band-relative scroll_y inside a band of
            # extent (spacer .. spacer). Serve it like a viewport policy:
            #   * near band top and items remain  -> grow front (bounded)
            #   * near band bottom and items remain -> grow end (bounded)
            #   * far above the viewport          -> drop front (bounded)
            #   * far below the viewport          -> shrink back (bounded)
            # Bounds: grow keeps the band <= want; drop/shrink keep the
            # viewport inside with KEEP rows of margin, and only run when
            # the band over-serves (>= BAND_CAP rows or KEEP*2 of margin).
            changed = False
            band_extent = self._band_extent()
            first_vis = self._first_visible(rows, cont_h)
            want = max(BAND_CAP, 2 * cont_h)
            room = want - n_items

            near_top = self.scroll_y <= cont_h
            near_bot = band_extent - (self.scroll_y + cont_h) <= cont_h

            if self._pending_edge:
                if DEBUG:
                    print(f"      [pending-edge] ws={self._window_start} "
                          f"n_pairs={len(pairs)} target={self._pending_abs:.0f} "
                          f"now={self._abs_now():.0f}")
                if self._serve_edge_request(pairs, rows, cont_h):
                    return True
            if self._window_start > 0 and near_top and room > 0:
                before = self._window_start
                self._grow_front(min(room, self._window_start))
                changed = self._window_start < before
            if self._window_end < total and near_bot and room > 0 \
                    and not changed:
                self._grow_end(min(room, total - self._window_end))
                changed = True

            # Trim: while the viewport is settled (no unserved request in
            # flight) and the band is bigger than the viewport needs, give
            # rows back at both ends — the window must return to its cap
            # once the band has over-served. Rows within KEEP of the
            # viewport are never touched.
            if not changed and not self._pending_edge and n_items > BAND_CAP:
                tail = n_items - first_vis
                if first_vis >= 2 * KEEP and self._window_start > 0:
                    before = self._window_start
                    self._unmount_front_keep(
                        self._count_for_rows(pairs, first_vis - KEEP))
                    changed = self._window_start > before
                    if DEBUG:
                        print(f"      [trim-front] {before}->"
                              f"{self._window_start} sy={self.scroll_y:.0f}")
                elif tail >= 2 * KEEP:
                    # shrink the band from the END toward the viewport:
                    # only rows beyond KEEP below the last visible row go.
                    rows_all = self._rows()
                    last_vis = self._last_visible(rows_all, cont_h)
                    excess = len(rows_all) - (last_vis + KEEP)
                    if excess >= BATCH:
                        self._unmount_end(excess)
                        changed = True
                        if DEBUG:
                            print(f"      [trim-end] -{excess} -> "
                                  f"we={self._window_end}")
            return changed

        def _count_for_rows(self, pairs, wanted_rows):
            """Number of leading in-band items whose heights first cover
            `wanted_rows` of layout (rows without items count as one)."""
            total_h = 0
            n = 0
            for (r, idx) in pairs:
                it = self._item_of(r)
                total_h += (self._height_of(it) if it is not None
                            else (r.region.height or 1))
                n += 1
                if total_h >= wanted_rows:
                    break
            return n

        def _last_visible(self, rows, cont_h):
            view_bot = self.scroll_y + cont_h
            for idx, r in enumerate(rows):
                if not r.region.height:
                    continue
                if r.region.y - self.scroll_offset.y >= view_bot:
                    return idx
            return len(rows)

        def _first_visible(self, rows, cont_h):
            view_top = self.scroll_y  # band-relative; spacers live in-band
            for idx, r in enumerate(rows):
                if not r.region.height:
                    return idx
                top = r.region.y - self.scroll_offset.y
                if top + r.region.height >= view_top:
                    return idx
            return len(rows)
            return len(rows) - 1

        # ---- I3: band mutations re-anchor to a widget ----
        def _drop_front(self, count, *, anchor=True):
            """Remove `count` rows from the band front and unmount them.

            The viewport is *content-anchored by default*: the spacer
            grows to carry what the band lost, and scroll_y grows to
            match, so the content under the viewport does not move. Callers
            that want the viewport to hold its position in the (shifted)
            coordinate system pass anchor=False and adjust themselves.

            Returns the ledger height moved out of the band."""
            if self._window_start + count > self._window_end:
                self._log_anomaly("drop-front-overflow")
                count = max(0, self._window_end - self._window_start - 1)
                if count <= 0:
                    return 0
            rows = self._rows()
            doomed = rows[:count]
            removed_h = sum(self._height_of(self._item_of(r))
                            for r in doomed if self._item_of(r) is not None)
            for r in doomed:
                item = self._item_of(r)
                if item is not None:
                    self._item_widgets.pop(id(item), None)
                r.remove()
            self._window_start += count
            self._sync_boundaries()
            if anchor:
                self._restore_scroll(self.scroll_y + removed_h)
            return removed_h

        def _grow_front(self, count):
            """Mount `count` items ahead of the band.

            Content-anchored: the spacer shrinks by the ledger height of
            the newly mounted items, so band scroll grows by the same and
            the content under the viewport does not move. Synchronous: the
            spacer is exact immediately (virtual-height widgets); the mount
            itself settles in the normal layout pass, and the scroll
            restore is deferred to after it."""
            state = self._render_state
            if state is None or count <= 0 or self._window_start <= 0:
                return
            count = min(count, self._window_start)
            new_items = state.items[self._window_start - count:self._window_start]
            widgets = [w for it in new_items
                       if (w := self._widget_for_item(it)) is not None]
            inserted_h = sum(self._height_of(it) for it in new_items)
            self._window_start -= count
            rows = self._rows()
            if widgets:
                if rows:
                    self.mount(*widgets, before=rows[0])
                else:
                    self.mount(*widgets, before=self._bottom_boundary)
            self._sync_boundaries()
            self._restore_scroll(min(float(self.max_scroll_y),
                                      self.scroll_y + inserted_h))

        def _grow_end(self, count):
            state = self._render_state
            if state is None or count <= 0:
                return
            count = min(count, len(state.items) - self._window_end)
            items = state.items[self._window_end:self._window_end + count]
            widgets = [w for it in items if (w := self._widget_for_item(it)) is not None]
            self._window_end += len(items)
            if widgets:
                self.mount(*widgets, before=self._bottom_boundary)
            self._sync_boundaries()
            self.refresh(layout=True)

        def _restore_scroll(self, band_sy):
            self._scroll_band(band_sy)

        def _fix_ledger_and_above(self):
            state = self._render_state
            if state is None:
                return
            self._measure()  # updates ledger for mounted item rows

        def _snap_window_to_rows(self):
            """Set window bounds to the indices of the mounted item rows.
            Returns False (caller rebuilds) when the mounted items are not a
            contiguous run in item order."""
            state = self._render_state
            rows = self._rows()
            if DEBUG and self._item_index and any(
                    self._item_index.get(id(self._item_of(r))) is None
                    for r in rows if self._item_of(r) is not None):
                stale = [r for r in rows if self._item_of(r) is not None
                         and self._item_index.get(id(self._item_of(r))) is None]
                print(f"      [stale rows] count={len(stale)} classes={ {type(r).__name__ for r in stale} } roles={ {getattr(self._item_of(r),'role',None) for r in stale} }")
            pairs = [(r, self._item_of(r)) for r in rows]
            pairs = [(r, it) for r, it in pairs if it is not None]
            # A boundary spacer is not a message row: skip it
            from tau_coding.tui.widgets import TranscriptWindowBoundary
            pairs = [(r, it) for r, it in pairs
                     if not isinstance(r, TranscriptWindowBoundary)]
            items = [it for _, it in pairs]
            if not items:
                return True
            idxs = [self._index_of(state, it) for it in items]
            if any(i is None for i in idxs):
                # an item row not in the item list at all: stale widget from
                # before a state swap; rebuild is the honest answer
                return False
            if any(b != a + 1 for a, b in zip(idxs, idxs[1:])):
                if DEBUG:
                    print(f"      [snap-noncontig] n={len(items)} idxs[:5]={idxs[:5]} idxs[-5:]={idxs[-5:]}")
                return False
            self._window_start = idxs[0]
            self._window_end = idxs[-1] + 1
            return True

        def _unmount_stale_rows(self):
            """Remove rows whose item is no longer in the state at all.
            Returns the number removed."""
            state = self._render_state
            if state is None:
                return 0
            self._reindex(state)
            n = 0
            for r in list(self._rows()):
                it = self._item_of(r)
                if it is None:
                    continue
                if self._index_of(state, it) is None:
                    self._item_widgets.pop(id(it), None)
                    r.remove()
                    n += 1
            return n

        def _reindex(self, state):
            pass

        def _unmount_stale_rows(self):
            return self._rows_of_state() and 0

        def _snap_window_to_rows(self):
            return self._sync_window_to_rows() and True

        def _fix_ledger_and_above(self):
            state = self._render_state
            if state is None:
                return
            self._measure()

        def _sync_boundaries(self):
            state = self._render_state
            if state is None:
                return
            total = len(state.items)
            # spacer heights = ledger sums outside the window
            if self._window_start > 0:
                if self._top_boundary is None:
                    from tau_coding.tui.widgets import TranscriptWindowBoundary
                    self._top_boundary = TranscriptWindowBoundary("earlier", self._window_start)
                    rows = self._rows()
                    self.mount(self._top_boundary, before=rows[0] if rows else None)
                    self.refresh(layout=True)
                else:
                    self._top_boundary.update_count(self._window_start)
                self._top_boundary.styles.height = sum(
                    self._height_of(it) for it in state.items[:self._window_start])
            elif self._top_boundary is not None:
                self._top_boundary.remove()
                self._top_boundary = None
            if self._window_end < total:
                if self._bottom_boundary is None:
                    from tau_coding.tui.widgets import TranscriptWindowBoundary
                    self._bottom_boundary = TranscriptWindowBoundary(
                        "later", total - self._window_end)
                    self.mount(self._bottom_boundary)
                    self.refresh(layout=True)
                else:
                    self._bottom_boundary.update_count(total - self._window_end)
                self._bottom_boundary.styles.height = sum(
                    self._height_of(it) for it in state.items[self._window_end:])
            elif self._bottom_boundary is not None:
                self._bottom_boundary.remove()
                self._bottom_boundary = None

        def _widget_for_item(self, item):
            existing = self._item_widgets.get(id(item))
            if existing is not None:
                return None
            from tau_coding.tui.widgets import _transcript_widget
            state = self._render_state
            show = state.show_tool_results if state else False
            w = _transcript_widget(
                item, theme=self._render_theme, show_tool_results=show,
                custom_markup=(state.resolve_custom_markup(item, expanded=show)
                               if item.role == "custom" else None),
                invocation=state.resolve_tool_invocation(item, expanded=show) if state else None,
                result_markup=state.resolve_tool_result(item, expanded=show) if state else None)
            self._item_widgets[id(item)] = w
            return w

        # ---- production pager off under culling ----
        def _schedule_window_shift(self, direction):
            return

        # ---- hooks ----
        def watch_scroll_y(self, old_value, new_value):
            # during band ops and content growth, textual moves scroll_y as a
            # side effect (clamping against a shrinking band). Production's
            # "user scrolled -> stop following" rule only applies to scrolls
            # from OUTSIDE us; a shrink caused by our own drop_front keeps
            # `follow` alive when the view was glued to the band bottom.
            band_shrink = (
                self._in_op
                or (new_value < old_value
                    and new_value >= self.max_scroll_y - 1)
            )
            follow_before = self._follow_output
            super().watch_scroll_y(old_value, new_value)
            if band_shrink and follow_before and self._render_state is not None:
                if self._window_end >= len(self._render_state.items):
                    self._follow_output = True
            self._schedule_retune(now=True)

        def on_size(self, old, new):
            self._schedule_retune()

    return CulledTranscriptView


def fill(state, n):
    for i in range(n):
        role = ["user", "assistant", "tool", "thinking"][i % 4]
        state.add_item(role, f"history item {i} " + ("lorem ipsum dolor sit amet " * 12))


async def run(cull, label):
    Base = tapp.TranscriptView
    tapp.TranscriptView = make_culled(Base) if cull else Base
    ANOMALIES.clear()
    try:
        app = TauTuiApp(FakeSession())
        async with app.run_test(size=(100, 40)) as pilot:
            tv = app.query_one("#transcript")
            fill(app.state, 400)
            tv.update_from_state(app.state, theme=app.tui_settings.resolved_theme)
            await pilot.pause(0.8)
            if cull:
                # one-shot placement: measure, keep the last BAND_CAP rows,
                # then re-anchor to the bottom once.
                await pilot.pause(0.2)
                tv._measure()
                rows = tv._rows()
                excess = len(rows) - BAND_CAP
                if excess > 0:
                    for r in rows[:excess]:
                        item = getattr(r, "item", None)
                        if item is not None:
                            tv._item_widgets.pop(id(item), None)
                        r.remove()
                    tv._window_start += excess
                tv.refresh(layout=True)
                await pilot.pause(0.3)
                tv.scroll_end(animate=False, immediate=True)
                await pilot.pause(0.3)
            mounted = len([c for c in tv.children if isinstance(c, twidget.Widget)])
            streamer = await tv.start_assistant_message(
                theme=app.tui_settings.resolved_theme, scroll_end=True)
            stop = False
            async def feeder():
                while not stop:
                    await streamer.append_fragment("word ")
                    await asyncio.sleep(0.01)
            task = asyncio.create_task(feeder())
            await asyncio.sleep(0.4)
            lags = []
            c0 = time.process_time(); w0 = time.perf_counter()
            for _ in range(6):
                marks.clear(); t0 = time.perf_counter()
                from textual import events
                ke = events.Key("z", "z"); ke.set_sender(app)
                app._driver.send_message(ke)
                while not marks and time.perf_counter() - t0 < 3:
                    await asyncio.sleep(0.002)
                lags.append((marks[0] - t0) * 1000 if marks else 0.0)
                await asyncio.sleep(0.2)
            cpu = time.process_time() - c0; wall = time.perf_counter() - w0
            stop = True
            await task
            await pilot.pause(0.3)
            end_gap = tv.max_scroll_y - tv.scroll_y
            results = {}

            def band_top(w):
                tb = getattr(w, "_top_boundary", None)
                if tb is None:
                    return 0
                return tb.region.y + tb.region.height - w.scroll_y

            def band_y_abs(w, y):
                """Absolute transcript y -> band scroll y.

                Exact when the first mounted row is an item whose state index
                is known: band y = scroll_y + (target_idx - first_idx) * h,
                no spacer geometry involved."""
                if not cull:
                    return y
                pairs = w._rows_of_state() if hasattr(w, "_rows_of_state") else []
                tb = getattr(w, "_top_boundary", None)
                top = (tb.region.y + tb.region.height - w.scroll_y) if tb else 0
                return max(0, y - top)

            async def idle(max_passes=40):
                for _ in range(max_passes):
                    await pilot.pause(0.1)
                    if not getattr(tv, "_pending", False) and \
                            not getattr(tv, "_pending_edge", False) and \
                            not getattr(tv, "_in_op", False):
                        return True
                return False

            async def settle(n=8):
                for _ in range(n):
                    await pilot.pause(0.15)

            # The band spans [spacer_h, spacer_h + extent) in the widget's
            # content coordinates, spacer_h being the height of the top
            # spacer. Any scroll target a USER would name is an absolute
            # content y; the view translates. A band-relative target is one
            # the retune loop serves by growing. Both are checked against
            # where the mounted rows actually are.

            # up: one page up from the bottom.
            # The probe speaks USER input: scroll pages relative to where
            # the user SEES they are, and the band cannot show a page above
            # itself, so it slides. The probe's notion of "settled" must be
            # the band's, not a fixed pause: settle until the retune loop
            # is idle with no pending request, then verify.
            tv.scroll_page_up(animate=False)
            await idle()
            results["up"] = tv.scroll_y > 0

            tv.scroll_page_up(animate=False)
            await idle()
            results["pgup"] = tv.scroll_y > 0

            # top: pages up until the band itself has reached the beginning
            for _ in range(40):
                tv.scroll_page_up(animate=False)
                await idle()
                if tv._window_start == 0 and tv.scroll_y <= 1:
                    break
            results["top"] = tv._window_start == 0 and tv.scroll_y <= 1
            if DEBUG and cull:
                print(f"    [probe] top: sy={tv.scroll_y:.0f} "
                      f"ws={tv._window_start} rows={len(tv._rows())}")

            # mid: jump to an absolute y that, after the top probe, lies in
            # the not-yet-mounted middle. Express it band-relative to the
            # CURRENT band top minus what the band must grow by: the view's
            # scroll_to takes absolute content y in non-culled mode; in
            # culled mode the same number is meaningless (the content moved)
            # — so compute it from live geometry: target is the ledger
            # offset of the item whose height-sum crosses 1000.
            if cull:
                state = tv._render_state
                y = 0
                i = 0
                while i < len(state.items) and y < 1000:
                    y += tv._height_of(state.items[i])
                    i += 1
                target = y  # absolute ledger y of item i
                tv.scroll_to(y=target, animate=False, immediate=True)
                await idle(60)
                tb = tv._top_boundary
                landed = tv.scroll_y + (tb.region.height if tb is not None
                                        and tb.region.height else 0)
                if DEBUG:
                    print(f"    [probe] mid: target={target:.0f} "
                          f"landed={landed:.0f} ws={tv._window_start}")
                results["mid"] = abs(landed - target) <= 40
            else:
                # baseline (no culling): plain scrollable; scroll_to takes
                # content y directly and lands there
                tv.scroll_to(y=1000, animate=False, immediate=True)
                await idle(60)
                results["mid"] = abs(tv.scroll_y - 1000) <= 40

            tv.scroll_end(animate=False, immediate=True)
            await idle()
            results["follow"] = (tv.max_scroll_y - tv.scroll_y) < 3

            rows = len([c for c in tv.children if isinstance(c, twidget.Widget)])
            print(f"{label}: cpu={cpu/wall*100:5.1f}% lag={sum(lags)/len(lags):4.1f}/{max(lags):5.1f}ms "
                  f"mounted={mounted} rows={rows} gap={end_gap:.0f} "
                  + " ".join(f"{k}={'Y' if v else 'n'}" for k, v in results.items())
                  + (f" ANOM={len(ANOMALIES)}@{ANOMALIES[-1] if ANOMALIES else ''}" if cull else ""))
            await streamer.finalize()
    finally:
        tapp.TranscriptView = Base


async def main():
    for cull in (False, True, False, True):
        await run(cull, f"cull={str(cull):5s}")

asyncio.run(main())
