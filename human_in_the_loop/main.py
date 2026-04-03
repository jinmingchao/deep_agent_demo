"""命令行演示：显著展示 HumanInTheLoopMiddleware 的影响。

从仓库根目录运行：
  python -m human_in_the_loop.main
"""

from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path
from typing import Any

from human_in_the_loop.tools import add_numbers


def _ensure_repo_root() -> Path:
    root = Path(__file__).resolve().parents[1]
    r = str(root)
    if r not in sys.path:
        sys.path.insert(0, r)
    src_dir = str(root / "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    return root


def _require_deps() -> None:
    try:
        import langchain  # noqa: F401
        import langgraph  # noqa: F401
    except ModuleNotFoundError as e:
        msg = (
            "缺少依赖：未找到 langchain/langgraph。\n\n"
            "请使用本仓库的虚拟环境运行，例如在仓库根目录执行：\n"
            "  .\\.venv\\Scripts\\python -m human_in_the_loop.main\n"
        )
        raise SystemExit(msg) from e


SYSTEM_PROMPT = """你是一个非常听话的计算智能体。

规则（必须遵守）：
- 只允许通过工具 add_numbers 来计算加法，禁止心算。
- 当用户让你计算 a+b 时，你必须调用 add_numbers(a=?, b=?)
- 最终回答只输出一个数字（不要解释）。
"""


def _last_text(out: dict[str, Any]) -> str:
    msgs = out.get("messages", [])
    if not msgs:
        return str(out)
    last = msgs[-1]
    content = getattr(last, "content", last)
    if isinstance(content, list):
        return "".join(
            b.get("text", "") if isinstance(b, dict) else str(b) for b in content
        ).strip()
    return str(content).strip()


def build_agent(*, hitl: bool):
    _ensure_repo_root()
    _require_deps()

    from langchain.agents import create_agent  # noqa: WPS433
    from langchain.agents.middleware import HumanInTheLoopMiddleware  # noqa: WPS433
    from langgraph.checkpoint.memory import InMemorySaver  # noqa: WPS433
    from utils.llm_util import deepseek_chat  # noqa: WPS433

    middleware = []
    if hitl:
        middleware.append(HumanInTheLoopMiddleware(interrupt_on={"add_numbers": True}))

    return create_agent(
        model=deepseek_chat,
        tools=[add_numbers],
        system_prompt=SYSTEM_PROMPT,
        middleware=middleware,
        checkpointer=InMemorySaver(),
        name=("demo_with_hitl" if hitl else "demo_without_hitl"),
    )


def run_without_hitl() -> None:
    agent = build_agent(hitl=False)
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    question = "请计算 12+8，并且只输出结果数字。"
    out = agent.invoke({"messages": [{"role": "user", "content": question}]}, config=config)
    print("[无人干预] 结果:", _last_text(out))


def run_with_hitl() -> None:
    agent = build_agent(hitl=True)
    from langgraph.types import Command  # noqa: WPS433

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    question = "请计算 12+8，并且只输出结果数字。"

    interrupt_payload = None
    for chunk in agent.stream({"messages": [{"role": "user", "content": question}]}, config=config):
        if "__interrupt__" in chunk:
            interrupt_payload = chunk["__interrupt__"][0].value
            break

    if not interrupt_payload:
        out = agent.invoke({"messages": [{"role": "user", "content": question}]}, config=config)
        print("[开启 HITL 但未触发中断] 结果:", _last_text(out))
        return

    print("[人工介入] 拦截到工具调用请求：")
    print(json.dumps(interrupt_payload, ensure_ascii=False, indent=2))

    edited = {"type": "edit", "edited_action": {"name": "add_numbers", "args": {"a": 12, "b": 80}}}
    resume_value = {"decisions": [edited]}

    final = None
    for chunk in agent.stream(Command(resume=resume_value), config=config):
        final = chunk

    # 最后一跳通常是 values/update，不稳定；稳妥起见再拿一次最终 state
    out = agent.get_state(config).values
    print("[人工介入] 将 b 从 8 改成 80 后，结果:", _last_text(out))


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

    run_without_hitl()
    run_with_hitl()


if __name__ == "__main__":
    main()

