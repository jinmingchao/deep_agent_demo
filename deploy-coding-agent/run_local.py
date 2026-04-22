"""在本地启动与 deploy-coding-agent 对齐的 Deep Agent（控制台交互）。

本脚本固定使用 **DeepSeek Chat** 作为唯一编码模型；同时将 `deploy-coding-agent/AGENTS.md`
作为**长期记忆（memory）**注入到智能体（而非手动拼接到 system prompt）。

用法（在仓库根目录、已激活 .venv）::

    python deploy-coding-agent/run_local.py

启动时会加载仓库内 **src/.env** 中的 ``DEEPSEEK_API_KEY`` 与 ``DEEPSEEK_BASE_URL``（``override=True``，
与 `agent_skill_demo.model_config` 行为一致），并用于构造 `ChatDeepSeek`。

说明：云端沙箱由 LangSmith 提供；本地使用 LocalShellBackend，在指定工作区内读写并执行
shell 命令（与任何本地 coding 助手一样，请仅在可信目录下使用）。
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, LocalShellBackend
from deepagents.middleware.subagents import _EXCLUDED_STATE_KEYS
from langchain_deepseek import ChatDeepSeek
from langchain.agents.middleware.types import wrap_tool_call
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

_DEPLOY_ROOT = Path(__file__).resolve().parent
_REPO_ROOT = _DEPLOY_ROOT.parent
_SRC_ENV = _REPO_ROOT / "src" / ".env"
_AGENT_WORKSPACE = _DEPLOY_ROOT / "workspace"

# 固定为 DeepSeek Chat（V3 对话模型，官方 API 模型名）；不提供其它模型开关
DEEPSEEK_MODEL_NAME = "deepseek-chat"

_ENV_LOADED = False

# 将 deploy-coding-agent/AGENTS.md 作为 memory 注入（走 backend 的虚拟路径）
AGENT_MEMORY_PATHS = ["/memory/AGENTS.md"]


def _ensure_src_env_loaded() -> None:
    """从仓库 ``src/.env`` 注入环境变量（优先于进程内已有值）。"""
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    if _SRC_ENV.is_file():
        load_dotenv(_SRC_ENV, override=True)
    else:
        print(
            f"警告: 未找到 {_SRC_ENV}，将仅使用当前进程环境变量中的 DeepSeek 配置。",
            file=sys.stderr,
        )
    _ENV_LOADED = True


def _build_deepseek_chat_model() -> ChatDeepSeek:
    """使用 ``src/.env`` 中的 DEEPSEEK_* 构造客户端（与 agent_skill_demo 一致）。"""
    _ensure_src_env_loaded()
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        msg = f"未设置 DEEPSEEK_API_KEY：请在 {_SRC_ENV} 中配置"
        raise RuntimeError(msg)
    base = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    return ChatDeepSeek(
        model=DEEPSEEK_MODEL_NAME,
        api_key=key,
        base_url=base,
        temperature=0.5,
        streaming=False,
    )

# 与 AGENTS.md 中 task(subagent_type="researcher") 对齐
_RESEARCHER_SUBAGENT = {
    "name": "researcher",
    "description": (
        "Research APIs, documentation, or codebase patterns before implementation. "
        "Use for exploration that can be answered by reading and searching files."
    ),
    "system_prompt": (
        "You are a focused researcher. Use grep, glob, and read_file to explore the "
        "repository. Summarize findings concisely with file references. Do not change "
        "code unless explicitly asked."
    ),
}

# 与 AGENTS.md「Subagents」中 jmc-test 说明对齐：仅注册供测试/对齐用，主智能体不得委派任务给它
_JMC_TEST_SUBAGENT = {
    "name": "jmc-test",
    "description": (
        "仅用于测试注册的占位 subagent。请勿将任何实际任务委派给本代理；请改用 "
        "`researcher` 或 `general-purpose`。"
    ),
    "system_prompt": (
        "仅占位用。若被误调用，请用一行简短回复说明 jmc-test 不应用于常规模型任务。"
    ),
}


def _debug_task_state_middleware():
    """Log tool calls; for `task`, also log subagent state."""

    @wrap_tool_call(name="DebugTaskStateMiddleware")
    def _debug_task_state(request, handler):
        tool_call = getattr(request, "tool_call", None) or {}
        tool_name = tool_call.get("name", "<missing tool name>")
        args = tool_call.get("args", {}) or {}

        # Print concrete arguments, but avoid dumping unbounded data.
        # (Tool args can include large file contents / long prompts.)
        def _pformat_limited(v, *, limit: int = 4000) -> str:
            import pprint

            try:
                s = pprint.pformat(v, width=120, compact=True, sort_dicts=True)
            except Exception:
                try:
                    s = repr(v)
                except Exception:
                    return "<unrepr-able>"
            if len(s) <= limit:
                return s
            return s[: limit - 3] + "..."

        if tool_name != "task":
            print(
                "[tool-call]",
                tool_name,
                "| args:",
                _pformat_limited(args),
                file=sys.stderr,
            )
            return handler(request)

        # `task`: also print the subagent state right before invoking it.
        subagent_type = args.get("subagent_type", "<missing subagent_type>") if isinstance(args, dict) else "<invalid args>"
        description = args.get("description", "") if isinstance(args, dict) else ""

        # Mirror deepagents.middleware.subagents._validate_and_prepare_state
        parent_state = getattr(request, "state", {}) or {}
        subagent_state = {k: v for k, v in parent_state.items() if k not in _EXCLUDED_STATE_KEYS}
        subagent_state["messages"] = [HumanMessage(content=description)]

        print(
            "[tool-call] task",
            "| subagent_type:",
            subagent_type,
            "| args:",
            _pformat_limited(args),
            file=sys.stderr,
        )
        print(
            "[subagent-state] content:",
            _pformat_limited(subagent_state),
            file=sys.stderr,
        )
        if description:
            print("[subagent-state] messages[0] content:", _pformat_limited(description, limit=4000), file=sys.stderr)

        return handler(request)

    return _debug_task_state


def _build_system_prompt() -> str:
    lint = _DEPLOY_ROOT / "skills" / "code-review" / "lint_check.py"
    extra = (
        "\n\n## Local runtime notes\n\n"
        "- File tools use a virtual path rooted at `deploy-coding-agent/workspace/`. Bundled skills are under `/skills/`.\n"
        "- `execute()` runs in the workspace directory on your machine (not a cloud sandbox).\n"
        f"- For the code-review lint helper, call Python with the real path: "
        f'`python "{lint}" .` (virtual `/skills/...` paths may not work in shell).\n'
    )
    return extra


def _backend_factory():
    """Composite: 默认工作区固定为 deploy-coding-agent/workspace；`/skills/` 目录不变。"""

    def factory(_runtime):
        skills_root = _DEPLOY_ROOT / "skills"
        return CompositeBackend(
            default=LocalShellBackend(
                root_dir=str(_AGENT_WORKSPACE),
                virtual_mode=True,
                inherit_env=True,
            ),
            routes={
                "/skills/": LocalShellBackend(
                    root_dir=str(skills_root),
                    virtual_mode=True,
                    inherit_env=True,
                ),
                "/memory/": LocalShellBackend(
                    root_dir=str(_DEPLOY_ROOT),
                    virtual_mode=True,
                    inherit_env=True,
                ),
            },
        )

    return factory


def _last_assistant_text(messages: list) -> str:
    from langchain_core.messages import AIMessage

    for m in reversed(messages or []):
        if isinstance(m, AIMessage):
            content = getattr(m, "content", None)
            if content is None:
                continue
            if isinstance(content, str) and content.strip():
                return content
            if isinstance(content, list):
                parts: list[str] = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        parts.append(str(block.get("text", "")))
                    elif isinstance(block, str):
                        parts.append(block)
                text = "".join(parts)
                if text.strip():
                    return text
    return ""


def _summarize_tool_args(args: object, *, limit: int = 240) -> str:
    """Keep tool args readable and avoid dumping large content."""
    try:
        s = repr(args)
    except Exception:
        return "<unrepr-able>"
    if len(s) <= limit:
        return s
    return s[: limit - 3] + "..."


def _print_actions(messages: list) -> None:
    """Print incremental tool/subagent actions to console."""
    from langchain_core.messages import AIMessage

    for m in messages or []:
        if not isinstance(m, AIMessage):
            continue
        tool_calls = getattr(m, "tool_calls", None) or []
        for tc in tool_calls:
            # tc is usually a dict-like: {"name": "...", "args": {...}, "id": "..."}
            name = tc.get("name", "<unknown>") if isinstance(tc, dict) else "<unknown>"
            args = tc.get("args", {}) if isinstance(tc, dict) else {}
            print(f"[action] {name} { _summarize_tool_args(args) }", file=sys.stderr)


def build_local_agent():
    model = _build_deepseek_chat_model()
    return create_deep_agent(
        model=model,
        system_prompt=_build_system_prompt(),
        memory=AGENT_MEMORY_PATHS,
        skills=["/skills/"],
        subagents=[_RESEARCHER_SUBAGENT, _JMC_TEST_SUBAGENT],
        middleware=[_debug_task_state_middleware()],
        backend=_backend_factory(),
        name="deepagents-deploy-coding-agent-local",
        checkpointer=MemorySaver(),
    )


def _invoke(graph, text: str, config: dict) -> str:
    """Run one turn; print agent actions while running; return final text."""
    last_seen = 0
    final_state: dict | None = None

    for state in graph.stream(
        {"messages": [{"role": "user", "content": text}]},
        config=config,
        stream_mode="values",
    ):
        final_state = state
        msgs = state.get("messages", [])
        if len(msgs) > last_seen:
            new_msgs = msgs[last_seen:]
            _print_actions(new_msgs)
            last_seen = len(msgs)

    out = final_state or {}
    msgs = out.get("messages", [])
    t = _last_assistant_text(msgs)
    if t:
        return t
    last = msgs[-1] if msgs else None
    return str(getattr(last, "content", last) if last is not None else out)


def _interactive(graph) -> None:
    thread_id = "deploy-coding-agent-local-cli"
    config = {"configurable": {"thread_id": thread_id}}
    print()
    print("=" * 60)
    print("  Coding Agent（本地）— 输入 exit / quit 结束")
    print("=" * 60)
    print()

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
            print(_invoke(graph, line, config))
            print()
        except Exception as e:
            print(f"[错误] {e}", file=sys.stderr)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

    _ensure_src_env_loaded()
    _AGENT_WORKSPACE.mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser(
        description="本地启动 deploy-coding-agent 对应的 Deep Agent（仅 DeepSeek Chat，配置见 src/.env）",
    )
    parser.parse_args()

    graph = build_local_agent()
    print(f"[工作区] {_AGENT_WORKSPACE}")
    print(f"[模型] {DEEPSEEK_MODEL_NAME} @ {os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')}")
    _interactive(graph)


if __name__ == "__main__":
    main()
