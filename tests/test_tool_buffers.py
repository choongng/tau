from __future__ import annotations

from pathlib import Path

import pytest

from tau_agent.messages import ImageContent, TextContent
from tau_agent.tools import AgentToolResult
from tau_coding.tool_buffers import BufferLimits, buffer_tool_result, read_first_line
from tau_coding.tools import create_read_tool

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


def _python_source(classes: int) -> tuple[str, dict[str, int]]:
    """A synthetic module and the 1-indexed file line of each definition."""
    lines = ['"""Synthetic module."""', "", "import os", ""]
    where: dict[str, int] = {}
    for c in range(classes):
        where[f"class Thing{c}"] = len(lines) + 1
        lines.append(f"class Thing{c}:")
        lines.append(f'    """Thing number {c}."""')
        lines.append("")
        where[f"def method_{c}"] = len(lines) + 1
        lines.append(f"    def method_{c}(self, value: int) -> int:")
        lines.extend(f"        value += {k}" for k in range(8))
        lines.append("        return value")
        lines.append("")
        where[f"async def fetch_{c}"] = len(lines) + 1
        lines.append(f"    async def fetch_{c}(self) -> None:")
        lines.extend(f"        await os.sleep({k})" for k in range(4))
        lines.append("")
        where[f"def helper_{c}"] = len(lines) + 1
        lines.append(f"def helper_{c}() -> int:")
        lines.extend(f"    x = {k}" for k in range(5))
        lines.append("    return x")
        lines.append("")
    return "\n".join(lines) + "\n", where


async def _read(tmp_path: Path, source: str, arguments: dict[str, object]) -> AgentToolResult:
    (tmp_path / "module.py").write_text(source)
    return await create_read_tool(cwd=tmp_path).execute("call", {"path": "module.py", **arguments})


@pytest.mark.anyio
async def test_cut_read_of_python_lists_definitions_with_line_numbers(tmp_path: Path) -> None:
    source, where = _python_source(classes=20)
    assert 500 < source.count("\n") < 600
    limits = BufferLimits(inline_chars=2_000, window_chars=8_000, window_lines=60)
    buffers = tmp_path / "buffers"

    for arguments in ({}, {"offset": 101}):
        result = await _read(tmp_path, source, arguments)
        buffered = buffer_tool_result(
            result,
            tool_name="read",
            buffer_dir=buffers,
            limits=limits,
            first_line=read_first_line(arguments),
        )
        shown = _text(buffered)
        outline = shown.split("Definitions (", 1)[1]
        late = [name for name, line in where.items() if line > 200]
        for name in [
            "class Thing7",
            "  def method_7",
            "  async def fetch_7",
            "def helper_15",
            late[0],
        ]:
            line = where[name.strip()]
            assert f"L{line} {name}" in outline, (arguments, name, line)
        assert where["class Thing7"] > 60
        if arguments:
            assert "L5 class Thing0" not in outline
        else:
            assert "L5 class Thing0" in outline


def test_cut_read_outline_is_bounded(tmp_path: Path) -> None:
    source, where = _python_source(classes=200)
    result = AgentToolResult(content=[TextContent(text=source)])
    limits = BufferLimits(inline_chars=2_000, window_chars=4_000, window_lines=60)

    shown = _text(buffer_tool_result(result, tool_name="read", buffer_dir=tmp_path, limits=limits))

    outline = shown.split("Definitions (", 1)[1]
    assert len(outline) <= limits.window_chars // 4 + 100
    listed = outline.count("\n  L")
    assert 0 < listed <= 80
    assert f"{len(where) - listed:,} more definitions not listed" in outline

    bash = _text(buffer_tool_result(result, tool_name="bash", buffer_dir=tmp_path, limits=limits))
    assert "Definitions (" not in bash
    plain = AgentToolResult(content=[TextContent(text="no code here\n" * 500)])
    assert "Definitions (" not in _text(
        buffer_tool_result(plain, tool_name="read", buffer_dir=tmp_path, limits=limits)
    )
