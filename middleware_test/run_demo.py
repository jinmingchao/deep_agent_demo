from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from middleware_test.graph_agent import build_agent_graph, export_png  # noqa: E402
from langchain_core.tools import tool  # noqa: E402


def main() -> None:
    @tool
    def demo_tool(text: str) -> str:
        """A tiny demo tool that echoes a response."""
        return f"[demo_tool] got: {text}"

    agent = build_agent_graph(tools=[demo_tool])

    png_path = export_png(agent, out_path=Path(__file__).resolve().parent / "agent_graph.png")
    print(f"[graph] wrote {png_path}")

    print("=== invoke ===")
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "请调用 demo_tool，入参 text='hello'，并展示返回值。"}]}
    )
    print(result)


if __name__ == "__main__":
    main()

