"""A call missing a required string argument is told it is missing (run R39)."""

from pathlib import Path

import pytest

from tau_coding import create_bash_tool, create_write_tool
from tau_coding.tools import ToolInputError


@pytest.mark.anyio
async def test_missing_path_names_the_missing_argument(tmp_path: Path) -> None:
    tool = create_write_tool(cwd=tmp_path)

    with pytest.raises(ToolInputError) as caught:
        await tool.execute("call-1", {"content": "abc"})

    message = str(caught.value)
    assert "`path` is missing" in message
    assert "must be a string" not in message
    assert "nothing was run" in message
    assert list(tmp_path.iterdir()) == []


@pytest.mark.anyio
async def test_missing_argument_lists_the_keys_the_call_carried(tmp_path: Path) -> None:
    tool = create_bash_tool(cwd=tmp_path)

    with pytest.raises(ToolInputError) as caught:
        await tool.execute("call-1", {"description": "list files"})

    message = str(caught.value)
    assert "`command` is missing" in message
    assert "`description`" in message


@pytest.mark.anyio
async def test_non_string_path_still_says_must_be_a_string(tmp_path: Path) -> None:
    tool = create_write_tool(cwd=tmp_path)

    with pytest.raises(ToolInputError) as caught:
        await tool.execute("call-1", {"path": 3, "content": "abc"})

    assert "path must be a string" in str(caught.value)
