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
import tempfile
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
) -> AgentToolResult:
    """Return `result` unchanged if it fits inline, else a window plus a buffer path."""
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
    shown, shown_lines = _window(text, head=head, limits=limits)
    total_lines = text.count("\n") + 1
    where = "first" if head else "last"
    if location is not None:
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
    images = [block for block in result.content if isinstance(block, ImageContent)]
    return result.model_copy(update={"content": [TextContent(text=f"{shown}\n{marker}"), *images]})


def _window(text: str, *, head: bool, limits: BufferLimits) -> tuple[str, int]:
    """The kept part of `text` and how many of its lines it shows, whole or in part."""
    lines = text.split("\n")
    kept = lines[: limits.window_lines] if head else lines[-limits.window_lines :]
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
