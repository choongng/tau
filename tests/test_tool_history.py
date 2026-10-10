from pathlib import Path

import pytest

from pi_event_helpers import assistant_done, assistant_start
from tau_agent import (
    AgentTool,
    AgentToolResult,
    AssistantMessage,
    TextContent,
    ToolCall,
    ToolResultMessage,
    UserMessage,
)
from tau_agent.messages import assistant_content
from tau_agent.session import JsonlSessionStorage
from tau_agent.tool_history import repair_tool_history
from tau_ai import FakeProvider
from tau_coding import CodingSession, CodingSessionConfig


def _call(call_id: str = "call-1", name: str = "read") -> ToolCall:
    return ToolCall(id=call_id, name=name, arguments={"path": "README.md"})


def _result(
    call_id: str = "call-1",
    *,
    text: str = "contents",
    is_error: bool = False,
) -> ToolResultMessage:
    return ToolResultMessage(
        tool_call_id=call_id,
        tool_name="read",
        content=[TextContent(text=text)],
        is_error=is_error,
    )


def test_valid_tool_history_is_unchanged() -> None:
    call = _call()
    result = _result()
    messages = (
        UserMessage(content="read"),
        AssistantMessage(content=[call]),
        result,
        AssistantMessage(content="done"),
    )

    repair = repair_tool_history(messages)

    assert repair.changed is False
    assert repair.messages == messages
    assert repair.diagnostic_data() == {
        "synthesizedResults": 0,
        "droppedOrphanResults": 0,
        "droppedDuplicateResults": 0,
        "reorderedResults": 0,
    }


def test_missing_result_gets_synthetic_interruption() -> None:
    call = _call()

    repair = repair_tool_history((UserMessage(content="read"), AssistantMessage(content=[call])))

    assert repair.changed is True
    result = repair.messages[-1]
    assert isinstance(result, ToolResultMessage)
    assert result.tool_call_id == call.id
    assert result.tool_name == call.name
    assert result.text == "Tool call interrupted by user"
    assert result.is_error is True
    assert repair.synthesized_results == 1


def test_orphan_result_is_dropped_without_inventing_a_call() -> None:
    user = UserMessage(content="continue")
    orphan = _result("call-missing")

    repair = repair_tool_history((orphan, user))

    assert repair.changed is True
    assert repair.messages == (user,)
    assert repair.dropped_orphan_results == 1
    assert repair.synthesized_results == 0


def test_late_result_moves_next_to_its_call() -> None:
    call = _call()
    assistant = AssistantMessage(content=[call])
    user = UserMessage(content="continue")
    result = _result()

    repair = repair_tool_history((assistant, user, result))

    assert repair.messages == (assistant, result, user)
    assert repair.changed is True
    assert repair.reordered_results == 1


def test_duplicate_results_prefer_real_output_over_interruption() -> None:
    call = _call()
    assistant = AssistantMessage(content=[call])
    interrupted = _result(text="Tool call interrupted by user", is_error=True)
    actual = _result(text="contents")

    repair = repair_tool_history((assistant, interrupted, actual))

    assert repair.messages == (assistant, actual)
    assert repair.dropped_duplicate_results == 1


def test_repeated_call_ids_keep_one_result_per_turn() -> None:
    first_call = _call("same")
    first_assistant = AssistantMessage(content=[first_call])
    first_result = _result("same", text="first")
    second_call = _call("same")
    second_assistant = AssistantMessage(content=[second_call])
    second_result = _result("same", text="second")
    messages = (first_assistant, first_result, second_assistant, second_result)

    repair = repair_tool_history(messages)

    assert repair.changed is False
    assert repair.messages == messages
    assert repair.dropped_duplicate_results == 0


def test_repeated_call_id_reserves_later_adjacent_result() -> None:
    first_assistant = AssistantMessage(content=[_call("same")])
    user = UserMessage(content="continue")
    second_assistant = AssistantMessage(content=[_call("same")])
    second_result = _result("same", text="second")

    repair = repair_tool_history((first_assistant, user, second_assistant, second_result))

    first_result = repair.messages[1]
    assert isinstance(first_result, ToolResultMessage)
    assert first_result.text == "Tool call interrupted by user"
    assert repair.messages == (first_assistant, first_result, user, second_assistant, second_result)
    assert repair.synthesized_results == 1


def test_parallel_results_follow_tool_call_order() -> None:
    first = _call("call-1", "read")
    second = _call("call-2", "bash")
    assistant = AssistantMessage(content=[first, second])
    second_result = ToolResultMessage(tool_call_id="call-2", tool_name="bash", content="second")
    first_result = _result("call-1", text="first")

    repair = repair_tool_history((assistant, second_result, first_result))

    assert repair.messages == (assistant, first_result, second_result)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


async def _repeat_refusal(tmp_path: Path, text: str) -> str:
    """The refusal of a third identical `read` whose result is `text`."""

    async def execute(
        tool_call_id: object, arguments: object, signal: object = None, on_update: object = None
    ) -> AgentToolResult:
        return AgentToolResult(content=[TextContent(text=text)])

    read = AgentTool(
        name="read",
        label="read",
        description="Read a file.",
        parameters={"type": "object"},
        execute_fn=execute,
    )
    call = ToolCall(id="call", name="read", arguments={"path": "data.txt"})
    turns: list[list[object]] = [
        [
            assistant_start(model="fake"),
            assistant_done(
                message=AssistantMessage(
                    content=assistant_content(
                        "Reading.", [call.model_copy(update={"id": f"call-{i}"})]
                    ),
                    stop_reason="toolUse",
                )
            ),
        ]
        for i in range(3)
    ]
    turns.append(
        [assistant_start(model="fake"), assistant_done(message=AssistantMessage(content="Done"))]
    )
    session = await CodingSession.load(
        CodingSessionConfig(
            provider=FakeProvider(turns),
            model="fake",
            system="You are Tau.",
            storage=JsonlSessionStorage(tmp_path / "session.jsonl"),
            cwd=tmp_path,
            tools=[read],
        )
    )
    async for _ in session.prompt("Go."):
        pass
    refusal = [m for m in session.messages if m.role == "toolResult"][2].text
    assert refusal.startswith("Not run: this `read` call ran 2 times")
    return refusal


@pytest.mark.anyio
async def test_repeat_refusal_quotes_the_read_cut_continuation(tmp_path: Path) -> None:
    # Run R42: a worker re-read a cut file without an offset eight times, and
    # each refusal quoted the file's first line, not where to continue from.
    text = "\n".join(f"2020/11/27 entry {i}" for i in range(20_000))
    refusal = await _repeat_refusal(tmp_path, text)
    said = refusal.split("It said: ", 1)[1]
    assert said.startswith("[Read cut: lines 1-")
    assert "continue with offset=" in said
    assert "2020/11/27" not in said


@pytest.mark.anyio
async def test_repeat_refusal_head_is_first_line_for_an_uncut_result(tmp_path: Path) -> None:
    refusal = await _repeat_refusal(tmp_path, "\n2020/11/27\nlater lines")
    assert "It said: 2020/11/27 Do what that result asks" in refusal
    assert "Read cut" not in refusal
