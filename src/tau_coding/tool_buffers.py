"""Keep oversized tool results out of the transcript.

Every tool result passes through `buffer_tool_result` before it becomes a
transcript message. A result under the inline limit is returned unchanged. A
larger one is written whole to a buffer file, and the transcript gets a window
of it (the tail by default, the head for `read`) plus a marker that names the
file. The model pages the rest in with tools it already knows: `read` with
`offset`/`limit`, or `grep` through `bash`.

The handle is a plain file path rather than an opaque id. Small models copy an
opaque handle into a dedicated buffer tool unreliably, but they read and grep
files fine, so a path needs no new tool and no new habit.

Buffer files are named by a hash of their content, so the same output always
gets the same path, and re-running a command does not leave the earlier path
stale.
"""

from __future__ import annotations

import os
import re
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from tau_agent.messages import ImageContent, TextContent
from tau_agent.tools import AgentToolResult
from tau_coding.context_window import CHARS_PER_TOKEN

#: The inline limit is this fraction of the model's context window...
INLINE_WINDOW_DIVISOR = 25
#: ...clamped to this many tokens, so a small window still shows a useful
#: result and a large one does not take in a whole log.
MIN_INLINE_TOKENS = 2_000
MAX_INLINE_TOKENS = 12_000
#: Lines of an oversized result kept in the transcript.
WINDOW_LINES = 60
#: Tools whose oversized output is windowed from the head, not the tail. Test
#: output, tracebacks and build logs end with the part that matters; a file
#: read starts with it.
HEAD_WINDOW_TOOLS = frozenset({"read"})
#: A head-windowed result is followed by an outline of its def/class lines, so
#: the model can jump to one with read offset/limit instead of paging. The
#: outline is capped at this many entries and a quarter of the window's chars.
OUTLINE_MAX_ENTRIES = 80
OUTLINE_WINDOW_DIVISOR = 4
#: An optional line-number prefix (`17\t`, `17: `, `17|`), then a definition.
_DEFINITION = re.compile(
    r"^(?:\s*(?P<number>\d+)(?:\t|[:|\u2502\u2192] ?))?"
    r"(?P<indent>[ \t]*)(?P<kind>async\s+def|def|class)\s+(?P<name>\w+)"
)
#: The note the read tool appends when it stops at a limit; not a file line.
_READ_TOOL_NOTE = re.compile(r"\n\n\[(?:Showing lines |\d+ more lines in file\. )[^\n]*\]\Z")


@dataclass(frozen=True, slots=True)
class BufferLimits:
    """How much of a tool result stays inline, in characters."""

    inline_chars: int
    window_chars: int
    window_lines: int = WINDOW_LINES

    @classmethod
    def for_context_window(cls, context_window_tokens: int) -> BufferLimits:
        tokens = min(
            MAX_INLINE_TOKENS,
            max(MIN_INLINE_TOKENS, context_window_tokens // INLINE_WINDOW_DIVISOR),
        )
        inline_chars = tokens * CHARS_PER_TOKEN
        return cls(inline_chars=inline_chars, window_chars=inline_chars // 2)


def default_buffer_dir() -> Path:
    """Where buffers go when the session has no file of its own."""
    return Path(tempfile.gettempdir()) / "tau-buffers"


def buffer_tool_result(
    result: AgentToolResult,
    *,
    tool_name: str,
    buffer_dir: Path,
    limits: BufferLimits,
    first_line: int = 1,
    limit: int | None = None,
) -> AgentToolResult:
    """Return `result` unchanged if it fits inline, else a window plus a buffer path.

    `first_line` is the file line the text starts at (a read's offset), so the
    marker and outline of a head-windowed read name the file's own line numbers.
    `limit` is the read's explicit line limit: a read that asked for a number
    of lines is cut by characters only, not by `window_lines`.
    """
    texts = [block.text for block in result.content if isinstance(block, TextContent)]
    text = "\n".join(texts)
    if len(text) <= limits.inline_chars:
        return result
    location: str | None = None
    failure = ""
    try:
        location = str(_write_buffer(buffer_dir, text))
    except OSError as exc:
        failure = f"{type(exc).__name__}: {exc}"
    head = tool_name in HEAD_WINDOW_TOOLS
    max_lines = None if head and limit is not None else limits.window_lines
    shown, shown_lines = _window(text, head=head, limits=limits, max_lines=max_lines)
    total_lines = text.count("\n") + 1
    where = "first" if head else "last"
    if head:
        marker = _read_marker(
            text, shown, first_line=first_line, location=location, failure=failure
        )
    elif location is not None:
        marker = (
            f"[Output truncated: the {where} {shown_lines:,} of {total_lines:,} lines "
            f"({len(shown):,} of {len(text):,} chars) are shown. Full output: {location} "
            "— page it with read (offset/limit) or grep it.]"
        )
    else:
        marker = (
            f"[Output truncated: the {where} {shown_lines:,} of {total_lines:,} lines "
            f"({len(shown):,} of {len(text):,} chars) are shown. The full output could "
            f"not be saved ({failure}).]"
        )
    if head:
        outline = _outline(
            text, first_line=first_line, max_chars=limits.window_chars // OUTLINE_WINDOW_DIVISOR
        )
        if outline:
            marker = f"{marker}\n{outline}"
    images = [block for block in result.content if isinstance(block, ImageContent)]
    return result.model_copy(update={"content": [TextContent(text=f"{shown}\n{marker}"), *images]})


def read_request(arguments: Mapping[str, object]) -> tuple[int, int | None]:
    """The file line a read with these arguments starts at, and its explicit limit."""
    limit = arguments.get("limit")
    explicit = isinstance(limit, int) and not isinstance(limit, bool) and limit > 0
    return read_first_line(arguments), limit if explicit else None


def read_first_line(arguments: Mapping[str, object]) -> int:
    """The file line a read with these arguments starts at (its offset, 1-indexed)."""
    offset = arguments.get("offset")
    if isinstance(offset, int) and not isinstance(offset, bool) and offset > 1:
        return offset
    return 1


def _read_marker(
    text: str, shown: str, *, first_line: int, location: str | None, failure: str
) -> str:
    """Which file lines a cut read shows, of those it returned, and where to go on."""
    body = _READ_TOOL_NOTE.sub("", text).removesuffix("\n")
    last_asked = first_line + body.count("\n")
    whole = shown.count("\n") + (1 if text[len(shown) : len(shown) + 1] in ("\n", "") else 0)
    last_shown = min(first_line + whole - 1, last_asked)
    if last_shown >= first_line:
        shown_part = f"lines {first_line}-{last_shown} of the file are shown"
    else:
        shown_part = f"line {first_line} is too long to show whole"
    marker = (
        f"[Read cut: {shown_part} (of {first_line}-{last_asked} asked); "
        f"continue with offset={last_shown + 1}."
    )
    if location is not None:
        return f"{marker} Full output: {location} — page it with read (offset/limit) or grep it.]"
    return f"{marker} The full output could not be saved ({failure}).]"


def _outline(text: str, *, first_line: int, max_chars: int) -> str:
    """The def/class lines of `text` with their file line numbers, bounded."""
    entries: list[str] = []
    for index, line in enumerate(text.split("\n")):
        match = _DEFINITION.match(line)
        if match is None:
            continue
        number = match["number"]
        line_number = int(number) if number is not None else first_line + index
        depth = len(match["indent"].expandtabs(4)) // 4
        kind = " ".join(match["kind"].split())
        entries.append(f"  L{line_number} {'  ' * depth}{kind} {match['name']}")
    if not entries:
        return ""
    header = "Definitions (jump with read offset=<line>):"
    kept: list[str] = []
    used = len(header)
    for entry in entries[:OUTLINE_MAX_ENTRIES]:
        if used + 1 + len(entry) > max_chars:
            break
        kept.append(entry)
        used += 1 + len(entry)
    left_out = len(entries) - len(kept)
    tail = [f"  ... {left_out:,} more definitions not listed"] if left_out else []
    return "\n".join([header, *kept, *tail])


def _window(
    text: str, *, head: bool, limits: BufferLimits, max_lines: int | None
) -> tuple[str, int]:
    """The kept part of `text` and how many of its lines it shows, whole or in part."""
    lines = text.split("\n")
    if max_lines is not None:
        lines = lines[:max_lines] if head else lines[-max_lines:]
    kept = lines
    shown = "\n".join(kept)
    if len(shown) > limits.window_chars:
        # A few very long lines (minified JSON, an event stream) would defeat a
        # line window on their own, so the character cap always applies too.
        shown = shown[: limits.window_chars] if head else shown[-limits.window_chars :]
    return shown, shown.count("\n") + 1


def _write_buffer(buffer_dir: Path, text: str) -> Path:
    data = text.encode("utf-8", "replace")
    path = buffer_dir / f"{sha256(data).hexdigest()[:16]}.txt"
    if path.exists():
        return path
    buffer_dir.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=buffer_dir, prefix=".buffer-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as file:
            file.write(data)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise
    return path
