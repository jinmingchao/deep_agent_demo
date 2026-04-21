from __future__ import annotations

import sys
from pathlib import Path

from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from middleware_test.middleware import FullHooksMiddleware  # noqa: E402
from utils import env_util  # noqa: E402


deepseek_chat = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.5,
    streaming=False,
    api_key=env_util.DEEPSEEK_API_KEY,
    base_url=env_util.DEEPSEEK_BASE_URL,
)


def build_agent_graph():
    """使用 LangGraph API（通过 create_agent）生成一张包含 agent 的图。"""
    agent_graph = create_agent(
        model=deepseek_chat,
        system_prompt="你是一个简洁的助手，请用中文回答。",
        middleware=[FullHooksMiddleware(tag="demo")],
    )
    return agent_graph


def export_mermaid(graph) -> str:
    g = graph.get_graph()
    if hasattr(g, "draw_mermaid"):
        return g.draw_mermaid()
    return str(g)


if __name__ == "__main__":
    graph = build_agent_graph()
    print(export_mermaid(graph))

