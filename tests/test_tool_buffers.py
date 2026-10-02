from __future__ import annotations

from pathlib import Path

from tau_agent.messages import ImageContent, TextContent
from tau_agent.tools import AgentToolResult
from tau_coding.tool_buffers import BufferLimits, buffer_tool_result

LIMITS = BufferLimits(inline_chars=1_000, window_chars=500, window_lines=10)


def _text(result: AgentToolResult) -> str:
    return "\n".join(b.text for b in result.content if isinstance(b, TextContent))


def test_a_result_that_fits_is_returned_unchanged(tmp_path: Path) -> None:
    result = AgentToolResult(content=[TextContent(text="short")])
    assert (
        buffer_tool_result(result, tool_name="bash", buffer_dir=tmp_path, limits=LIMITS) is result
    )
    assert list(tmp_path.iterdir()) == []


def test_an_oversized_result_keeps_its_tail_and_names_the_full_file(tmp_path: Path) -> None:
    text = "\n".join(f"line {i}" for i in range(500))
    result = AgentToolResult(content=[TextContent(text=text)])

    buffered = buffer_tool_result(result, tool_name="bash", buffer_dir=tmp_path, limits=LIMITS)

    shown = _text(buffered)
    assert "line 499" in shown and "line 0\n" not in shown
    assert "the last 10 of 500 lines" in shown
    [path] = list(tmp_path.iterdir())
    assert str(path) in shown and path.read_text() == text
    again = buffer_tool_result(result, tool_name="bash", buffer_dir=tmp_path, limits=LIMITS)
    assert _text(again) == shown and len(list(tmp_path.iterdir())) == 1


def test_read_keeps_the_head_and_long_lines_are_capped(tmp_path: Path) -> None:
    head = buffer_tool_result(
        AgentToolResult(content=[TextContent(text="\n".join(f"row {i}" for i in range(500)))]),
        tool_name="read",
        buffer_dir=tmp_path,
        limits=LIMITS,
    )
    assert _text(head).startswith("row 0\n") and "the first 10 of 500 lines" in _text(head)

    one_line = buffer_tool_result(
        AgentToolResult(content=[TextContent(text="x" * 100_000)]),
        tool_name="bash",
        buffer_dir=tmp_path,
        limits=LIMITS,
    )
    assert len(_text(one_line)) < 1_000


def test_an_unwritable_buffer_still_truncates_and_says_why(tmp_path: Path) -> None:
    blocker = tmp_path / "file"
    blocker.write_text("")
    image = ImageContent(data="aGk=", mime_type="image/png")
    result = AgentToolResult(content=[TextContent(text="y\n" * 5_000), image])

    buffered = buffer_tool_result(
        result, tool_name="bash", buffer_dir=blocker / "sub", limits=LIMITS
    )

    assert "could not be saved" in _text(buffered)
    assert buffered.content[-1] == image
