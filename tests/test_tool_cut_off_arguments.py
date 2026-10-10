"""Calls whose arguments are only unparsed text name the cut-off (run R38)."""

from pathlib import Path

import pytest

from tau_coding import create_bash_tool, create_write_tool
from tau_coding.tools import ToolInputError


@pytest.mark.anyio
async def test_cut_off_write_names_the_cut_off_not_the_path(tmp_path: Path) -> None:
    tool = create_write_tool(cwd=tmp_path)
    text = '{"path":"x.txt","content":"abc'

    with pytest.raises(ToolInputError) as caught:
        await tool.execute("call-1", {"_raw_arguments": text})

    message = str(caught.value)
    assert f"after {len(text)} characters" in message
    assert "cut off" in message
    assert "nothing was written" in message
    assert "path must be a string" not in message
    assert not (tmp_path / "x.txt").exists()


@pytest.mark.anyio
async def test_cut_off_bash_does_not_run(tmp_path: Path) -> None:
    tool = create_bash_tool(cwd=tmp_path)

    with pytest.raises(ToolInputError) as caught:
        await tool.execute("call-1", {"_raw_arguments": '{"command":"touch MARK'})

    assert "the bash tool did not run" in str(caught.value)
    assert not (tmp_path / "MARK").exists()


@pytest.mark.anyio
async def test_parsed_arguments_still_reach_the_tool(tmp_path: Path) -> None:
    tool = create_write_tool(cwd=tmp_path)

    await tool.execute("call-1", {"path": "x.txt", "content": "abc"})

    assert (tmp_path / "x.txt").read_text(encoding="utf-8") == "abc"
