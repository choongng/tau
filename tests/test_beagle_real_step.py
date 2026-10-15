"""One pursuit_step's open, stub worker and close against the real, pinned beagle CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from beagle_real_cli import (
    GOAL,
    beagle_cli,
    beagle_json,
    bound,
    pinned_beagle,
    show,
    step_hello,
    task_node,
)
from test_beagle_example_extension import _tool

pytestmark = [pytest.mark.real_beagle, pytest.mark.anyio]


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def real_beagle(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    return pinned_beagle(tmp_path, monkeypatch)


async def test_real_step_opens_dispatches_the_worker_and_closes(
    tmp_path: Path, real_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hello, _, result = await step_hello(tmp_path, monkeypatch, {"hello.txt": "hi\n"})

    [run] = [json.loads(line) for line in (tmp_path / "stub-tau" / "runs.jsonl").open()]
    assert run["argv"][:3] == ["-p", "--mode", "json"]
    assert hello in run["stdin"]
    record = show(real_beagle, hello)
    assert record["done_when"] == "grep -q hi hello.txt"
    assert record["status"] == "done", result.text
    assert "closed done" in result.text, result.text


async def test_real_step_commits_work_a_worker_left_uncommitted_then_closes(
    tmp_path: Path, real_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A real worker is refused `git commit`: pursuit_step commits its scope.
    monkeypatch.setenv("STUB_TAU_COMMITS", "0")
    hello, _, result = await step_hello(tmp_path, monkeypatch, {"hello.txt": "hi\n"})

    assert "closed done" in result.text, result.text
    assert show(real_beagle, hello)["status"] == "done"
    tracked = subprocess.run(
        ["git", "log", "--format=%s", "--", "hello.txt"],
        cwd=real_beagle,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert tracked.strip(), result.text
    assert not subprocess.run(
        ["git", "status", "--porcelain", "--", "hello.txt"],
        cwd=real_beagle,
        capture_output=True,
        text=True,
        check=True,
    ).stdout


SPEC = (
    "Calc.\n"
    "add(a, b) returns the sum of a and b.\n"
    "add raises TypeError when a or b is not a number.\n"
)

CALC = (
    "def add(a, b):\n"
    "    if not all(isinstance(x, (int, float)) for x in (a, b)):\n"
    "        raise TypeError('add takes numbers')\n"
    "    return a + b\n"
)


def _anchors(project: Path) -> dict[int, str]:
    """`spec`'s line anchors as `beagle refs show` prints them: `2#ff4| add(...`."""
    out = beagle_cli(project, "refs", "show", "spec").stdout
    lines = [line.split("|", 1)[0].strip() for line in out.splitlines() if "|" in line]
    return {int(anchor.split("#")[0]): anchor for anchor in lines if "#" in anchor}


async def test_real_spec_tied_step_writes_cases_opens_tied_and_closes_done(
    tmp_path: Path, real_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # T0601: a milestone with a source is one pursuit_step: the cases worker's
    # marked tests, an open 0.48 accepts with --cites/--cases, the code worker.
    (real_beagle / "references").mkdir()
    (real_beagle / "references" / "spec.txt").write_text(SPEC)
    subprocess.run(["git", "add", "references"], cwd=real_beagle, check=True)
    subprocess.run(["git", "commit", "--quiet", "-m", "spec"], cwd=real_beagle, check=True)
    runtime = bound(tmp_path)
    goal = {
        **GOAL,
        "statement": "A calculator",
        "criteria": ["add works as the spec says", "bye.txt says bye"],
        "milestones": [
            {"part": "Add::add(a, b) in calc.py", "source": "spec"},
            "Bye::write bye.txt saying bye",
        ],
    }
    founded = await _tool(runtime, "pursuit_found").execute("c1", goal)
    assert "root task" in founded.text, founded.text
    tree = beagle_json(real_beagle, "pursuit", "tree", "--json")
    add = task_node(tree, "Add")["id"]
    assert show(real_beagle, add)["intent"].endswith("Source: spec")
    anchors = _anchors(real_beagle)
    cases = (
        "import pytest\n"
        "from calc import add\n\n\n"
        f"# beagle-case: add-sum cite=spec:{anchors[2]} kind=example op=add\n"
        "def test_add_sum():\n    assert add(2, 3) == 5\n\n\n"
        f"# beagle-case: add-type cite=spec:{anchors[3]} kind=invalid op=add\n"
        "def test_add_type():\n    with pytest.raises(TypeError):\n        add('2', 3)\n"
    )
    monkeypatch.setenv("STUB_TAU_CASES_WRITES", json.dumps({"tests/test_calc.py": cases}))
    monkeypatch.setenv("STUB_TAU_WRITES", json.dumps({"calc.py": CALC}))
    witness = "WITNESS: calc.py\nNEEDLE:\nreturn a + b\nREPLACEMENT:\nreturn a - b\nEND WITNESS"
    monkeypatch.setenv("STUB_TAU_REPORT", witness)
    step = _tool(runtime, "pursuit_step")
    shown = await step.execute("c2", {})
    assert add in shown.text and "Its source is spec" in shown.text, shown.text

    result = await step.execute(
        "c3",
        {
            "task": add,
            "criteria": "add returns the sum and refuses what is not a number",
            "done_when": f"{sys.executable} -m pytest -q -p no:cacheprovider tests/test_calc.py",
            "scope": ["calc.py"],
        },
    )

    runs = [json.loads(line) for line in (tmp_path / "stub-tau" / "runs.jsonl").open()]
    assert [run["role"] for run in runs] == ["cases", "executor"], result.text
    assert "beagle pursuit rules 2e" in runs[0]["stdin"]
    record = show(real_beagle, add)
    assert record["cites"] == [f"spec.txt:{anchors[2]}", f"spec.txt:{anchors[3]}"], record
    assert record["cases"] == ["tests/test_calc.py"]
    assert record["status"] == "done", result.text
    assert "closed done" in result.text, result.text
    committed = subprocess.run(
        ["git", "log", "--format=%s", "--", "tests/test_calc.py"],
        cwd=real_beagle,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert committed.strip(), result.text


async def _spec_tied_step_with_a_wrong_case(
    tmp_path: Path, project: Path, monkeypatch: pytest.MonkeyPatch, report: str
) -> tuple[str, str, Any]:
    """A spec-tied Add step whose cases worker wrote `add(2, 3) == 6`, against the
    spec, and whose code worker corrects it to 5 and reports `report`."""
    (project / "references").mkdir()
    (project / "references" / "spec.txt").write_text(SPEC)
    subprocess.run(["git", "add", "references"], cwd=project, check=True)
    subprocess.run(["git", "commit", "--quiet", "-m", "spec"], cwd=project, check=True)
    runtime = bound(tmp_path)
    goal = {
        **GOAL,
        "statement": "A calculator",
        "criteria": ["add works as the spec says"],
        "milestones": [{"part": "Add::add(a, b) in calc.py", "source": "spec"}],
    }
    await _tool(runtime, "pursuit_found").execute("c1", goal)
    add = task_node(beagle_json(project, "pursuit", "tree", "--json"), "Add")["id"]
    anchors = _anchors(project)
    case_sum = f"# beagle-case: add-sum cite=spec:{anchors[2]} kind=example op=add\n"
    head = "import pytest\nfrom calc import add\n\n\n"
    tail = (
        f"\n\n\n# beagle-case: add-type cite=spec:{anchors[3]} kind=invalid op=add\n"
        "def test_add_type():\n    with pytest.raises(TypeError):\n        add('2', 3)\n"
    )
    wrong = head + case_sum + "def test_add_sum():\n    assert add(2, 3) == 6" + tail
    right = head + case_sum + "def test_add_sum():\n    assert add(2, 3) == 5" + tail
    monkeypatch.setenv("STUB_TAU_CASES_WRITES", json.dumps({"tests/test_calc.py": wrong}))
    monkeypatch.setenv(
        "STUB_TAU_WRITES", json.dumps({"calc.py": CALC, "tests/test_calc.py": right})
    )
    witness = "WITNESS: calc.py\nNEEDLE:\nreturn a + b\nREPLACEMENT:\nreturn a - b\nEND WITNESS"
    monkeypatch.setenv("STUB_TAU_REPORT", f"{report}\n\n{witness}")
    result = await _tool(runtime, "pursuit_step").execute(
        "c2",
        {
            "task": add,
            "criteria": "add returns the sum and refuses what is not a number",
            "done_when": f"{sys.executable} -m pytest -q -p no:cacheprovider tests/test_calc.py",
            "scope": ["calc.py"],
        },
    )
    return add, (project / "tests" / "test_calc.py").read_text(), result


async def test_real_spec_tied_step_amends_a_case_the_code_worker_corrects_from_the_source(
    tmp_path: Path, real_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Run R100: the code worker corrected cases that read the source wrong, the
    # changed pin refused the close, and the task never closed. With the source's
    # words for the case, tau re-pins the cases by `pursuit amend`, and it closes.
    add, cases, result = await _spec_tied_step_with_a_wrong_case(
        tmp_path, real_beagle, monkeypatch, 'CASE add-sum: "returns the sum of a and b"'
    )
    assert "== 5" in cases
    record = show(real_beagle, add)
    assert record["status"] == "done", result.text
    assert "re-pinned on the record by `pursuit amend`" in result.text, result.text
    runs = [json.loads(line) for line in (tmp_path / "stub-tau" / "runs.jsonl").open()]
    assert "write the code to them, not them to the code" in runs[-1]["stdin"]


async def test_real_spec_tied_step_puts_back_a_case_changed_without_the_source_words(
    tmp_path: Path, real_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The stub's second attempt would commit nothing new and fail; it commits none.
    monkeypatch.setenv("STUB_TAU_COMMITS", "0")
    add, cases, result = await _spec_tied_step_with_a_wrong_case(
        tmp_path, real_beagle, monkeypatch, 'CASE add-sum: "the sum is five"'
    )
    assert "== 6" in cases
    assert show(real_beagle, add)["status"] != "done", result.text
    assert "its cited lines (spec" in result.text and "put back as pinned" in result.text, (
        result.text
    )


async def test_real_spec_tied_step_names_cases_whose_markers_have_no_name(
    tmp_path: Path, real_beagle: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Run S03: the markers read `# beagle-case: wrenfold-r3:25#019 kind=… op=…`, then
    # `# beagle-case: cite=wrenfold-r3:25#019 …`; none tied, and sound cases were redone.
    (real_beagle / "references").mkdir()
    (real_beagle / "references" / "spec.txt").write_text(SPEC)
    subprocess.run(["git", "add", "references"], cwd=real_beagle, check=True)
    subprocess.run(["git", "commit", "--quiet", "-m", "spec"], cwd=real_beagle, check=True)
    runtime = bound(tmp_path)
    goal = {
        **GOAL,
        "statement": "A calculator",
        "criteria": ["add works as the spec says"],
        "milestones": [{"part": "Add::add(a, b) in calc.py", "source": "spec"}],
    }
    await _tool(runtime, "pursuit_found").execute("c1", goal)
    add = task_node(beagle_json(real_beagle, "pursuit", "tree", "--json"), "Add")["id"]
    anchors = _anchors(real_beagle)
    cases = (
        "import pytest\nfrom calc import add\n\n\n"
        f"# beagle-case: spec:{anchors[2]} kind=example op=add\n"
        "def test_add_sum():\n    assert add(2, 3) == 5\n\n\n"
        f"# beagle-case: cite=spec:{anchors[3]} kind=invalid op=add\n"
        "def test_add_type():\n    with pytest.raises(TypeError):\n        add('2', 3)\n"
    )
    monkeypatch.setenv("STUB_TAU_CASES_WRITES", json.dumps({"tests/test_calc.py": cases}))
    monkeypatch.setenv("STUB_TAU_WRITES", json.dumps({"calc.py": CALC}))
    witness = "WITNESS: calc.py\nNEEDLE:\nreturn a + b\nREPLACEMENT:\nreturn a - b\nEND WITNESS"
    monkeypatch.setenv("STUB_TAU_REPORT", witness)
    result = await _tool(runtime, "pursuit_step").execute(
        "c2",
        {
            "task": add,
            "criteria": "add returns the sum and refuses what is not a number",
            "done_when": f"{sys.executable} -m pytest -q -p no:cacheprovider tests/test_calc.py",
            "scope": ["calc.py"],
        },
    )
    assert show(real_beagle, add)["status"] == "done", result.text
    written = (real_beagle / "tests" / "test_calc.py").read_text()
    assert f"# beagle-case: add-5 cite=spec:{anchors[2]} kind=example op=add" in written
    assert f"# beagle-case: add-10 cite=spec:{anchors[3]} kind=invalid op=add" in written
