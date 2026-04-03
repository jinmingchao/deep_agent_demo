"""命令行演示：从仓库根目录执行

  python -m agent_skill_demo.main

启动后在控制台用 input() 逐行输入问题，与智能体多轮对话（含 arithmetic / legal-knowledge /
mysql-ycyt 三 Skill）。可选参数：--dump-skills（启动时打印 Skill 元数据 JSON）。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml
from langgraph.checkpoint.memory import MemorySaver

# 与 skills/demo 下三个 SKILL.md 的 name 字段一致
EXPECTED_SKILL_NAMES: frozenset[str] = frozenset({"arithmetic", "legal-knowledge", "mysql-ycyt"})


def _ensure_repo_root() -> Path:
    root = Path(__file__).resolve().parents[1]
    r = str(root)
    if r not in sys.path:
        sys.path.insert(0, r)
    return root


def _print_registered_tools(graph) -> None:
    tool_node = graph.get_graph().nodes["tools"].data
    names = sorted(tool_node.tools_by_name.keys())
    print("[DeepAgent 工具列表]", ", ".join(names))


def _parse_skill_md(skill_md_path: Path) -> dict:
    """Parse Agent Skills frontmatter into a SkillMetadata-like dict."""
    content = skill_md_path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, flags=re.DOTALL)
    if not m:
        return {"path": str(skill_md_path), "error": "No valid YAML frontmatter"}

    frontmatter_data = yaml.safe_load(m.group(1)) or {}
    if not isinstance(frontmatter_data, dict):
        return {"path": str(skill_md_path), "error": "Frontmatter is not a mapping"}

    raw_tools = frontmatter_data.get("allowed-tools")
    allowed_tools: list[str] = []
    if isinstance(raw_tools, str):
        allowed_tools = [t.strip(",") for t in raw_tools.split() if t.strip(",")]

    agent_root = Path(__file__).resolve().parent
    try:
        rel = skill_md_path.relative_to(agent_root).as_posix()
    except ValueError:
        rel = skill_md_path.as_posix()

    virtual_path = f"/{rel.lstrip('/')}"

    return {
        "path": virtual_path,
        "name": str(frontmatter_data.get("name", "")).strip(),
        "description": str(frontmatter_data.get("description", "")).strip(),
        "license": (str(frontmatter_data.get("license", "")).strip() or None),
        "compatibility": (str(frontmatter_data.get("compatibility", "")).strip() or None),
        "allowed_tools": allowed_tools,
        "metadata": frontmatter_data.get("metadata", {}) if isinstance(frontmatter_data.get("metadata", {}), dict) else {},
    }


def _collect_skills_meta() -> list[dict]:
    skills_root = Path(__file__).resolve().parent / "skills" / "demo"
    if not skills_root.exists():
        return []
    skills: list[dict] = []
    for child in sorted(skills_root.iterdir(), key=lambda p: p.name):
        if not child.is_dir():
            continue
        skill_md = child / "SKILL.md"
        if not skill_md.is_file():
            continue
        skills.append(_parse_skill_md(skill_md))
    return skills


def _print_skills_schema(skills: list[dict]) -> None:
    print("[DeepAgent Skill 元数据]", json.dumps(skills, ensure_ascii=False, indent=2))


def _validate_three_skills(skills: list[dict]) -> None:
    names = {s.get("name") for s in skills if isinstance(s, dict)}
    missing = EXPECTED_SKILL_NAMES - names
    extra = names - EXPECTED_SKILL_NAMES - {""}
    if missing:
        print(f"[提示] 未找到全部预期 Skill，缺少: {sorted(missing)}", file=sys.stderr)
    if extra:
        print(f"[提示] 存在未在预期集合中的 Skill 名称: {sorted(extra)}", file=sys.stderr)


def _print_skill_banner(skills: list[dict]) -> None:
    print()
    print("=" * 60)
    print("  Deep Agent · 三 Skill 演示（arithmetic / legal-knowledge / mysql-ycyt）")
    print("=" * 60)
    for s in skills:
        if not isinstance(s, dict):
            continue
        name = s.get("name", "")
        tools = ", ".join(s.get("allowed_tools") or [])
        print(f"  · {name}: [{tools}]")
    print("  输入 exit / quit 结束；Ctrl+Z+Enter（Windows）或 Ctrl+D 退出")
    print("=" * 60)
    print()


def _last_assistant_text(messages: list) -> str:
    """从消息列表中取最后一条 AI 文本回复。"""
    from langchain_core.messages import AIMessage

    for m in reversed(messages or []):
        if isinstance(m, AIMessage):
            content = getattr(m, "content", None)
            if content is None:
                continue
            if isinstance(content, str) and content.strip():
                return content
            if isinstance(content, list):
                parts = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        parts.append(block.get("text", ""))
                    elif isinstance(block, str):
                        parts.append(block)
                text = "".join(parts)
                if text.strip():
                    return text
    return ""


def build_three_skill_demo_agent():
    """创建已注册三个业务 Skill 与对应工具的 Deep Agent（含会话记忆，供控制台多轮使用）。"""
    from agent_skill_demo.agent import build_agent
    from agent_skill_demo.tools import SKILL_TOOLS

    if len(SKILL_TOOLS) != 3:
        raise RuntimeError(f"预期 3 个 Skill 工具，当前为 {len(SKILL_TOOLS)} 个")

    return build_agent(checkpointer=MemorySaver())


def run_invoke(graph, user_text: str, config: dict | None) -> str:
    """执行一轮对话，返回助手文本。"""
    out = graph.invoke(
        {"messages": [{"role": "user", "content": user_text}]},
        config=config,
    )
    msgs = out.get("messages", [])
    text = _last_assistant_text(msgs)
    if text:
        return text
    last = msgs[-1] if msgs else None
    return str(getattr(last, "content", last) if last is not None else out)


def run_interactive_loop(graph) -> None:
    """控制台多轮交互（固定 thread，保留上下文）。"""
    thread_id = "skill-demo-cli"
    config = {"configurable": {"thread_id": thread_id}}

    while True:
        try:
            line = input("用户> ").strip()
        except EOFError:
            print()
            break
        if not line:
            continue
        if line.lower() in ("exit", "quit"):
            break
        try:
            reply = run_invoke(graph, line, config)
            print(reply)
            print()
        except Exception as e:
            print(f"[错误] {e}", file=sys.stderr)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

    _ensure_repo_root()

    parser = argparse.ArgumentParser(
        description="Deep Agent：集成 arithmetic、legal-knowledge、mysql-ycyt 三 Skill；启动后在控制台输入问题交互",
    )
    parser.add_argument(
        "--dump-skills",
        action="store_true",
        help="启动时打印 skills/demo 下全部 SKILL.md 解析后的 JSON，然后进入交互",
    )
    args = parser.parse_args()

    skills_meta = _collect_skills_meta()
    _validate_three_skills(skills_meta)

    graph = build_three_skill_demo_agent()
    _print_registered_tools(graph)

    if args.dump_skills:
        _print_skills_schema(skills_meta)
        print()

    _print_skill_banner(skills_meta)
    if not args.dump_skills:
        print("[Skill 摘要] 使用 --dump-skills 可在启动时打印各 Skill 完整 frontmatter JSON\n")

    run_interactive_loop(graph)


if __name__ == "__main__":
    main()
