from __future__ import annotations

import ast
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
RELEASE_DOCUMENTS = tuple(
    ROOT / name
    for name in (
        "GOALS.md",
        "README-V1.md",
        "README-V2.md",
        "api.md",
        "simple_programs.md",
        "principles.md",
        "batch_report.md",
        "render-spec.md",
        "render-chat.md",
        "goal-7/0-plan.md",
        "goal-7/7-RELEASE.md",
    )
)
CURRENT_EXECUTABLE_DOCUMENTS = (
    ROOT / "README-V2.md",
    ROOT / "api.md",
)
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _scan_document(path: Path) -> tuple[str, tuple[str, ...]]:
    prose: list[str] = []
    python_blocks: list[str] = []
    current_block: list[str] = []
    in_fence = False
    python_fence = False

    for line in path.read_text().splitlines():
        if line.lstrip().startswith("```"):
            if in_fence:
                if python_fence:
                    python_blocks.append("\n".join(current_block))
                current_block = []
                in_fence = False
                python_fence = False
            else:
                in_fence = True
                python_fence = line.lstrip()[3:].strip() == "python"
            continue
        if in_fence:
            if python_fence:
                current_block.append(line)
        else:
            prose.append(line)

    assert not in_fence, f"{path.relative_to(ROOT)} has an unclosed code fence"
    return "\n".join(prose), tuple(python_blocks)


def test_release_document_links_and_fences_are_structurally_valid() -> None:
    for path in RELEASE_DOCUMENTS:
        prose, _ = _scan_document(path)
        for target in MARKDOWN_LINK.findall(prose):
            if target.startswith(("http://", "https://", "#")):
                continue
            local_target = target.split("#", 1)[0]
            if not local_target:
                continue
            resolved = (path.parent / local_target).resolve()
            assert resolved.exists(), (
                f"{path.relative_to(ROOT)} links to missing {target!r}"
            )


def test_current_public_python_fences_parse() -> None:
    for path in CURRENT_EXECUTABLE_DOCUMENTS:
        _, python_blocks = _scan_document(path)
        assert python_blocks, f"{path.relative_to(ROOT)} has no Python examples"
        for block in python_blocks:
            ast.parse(block, filename=str(path))
