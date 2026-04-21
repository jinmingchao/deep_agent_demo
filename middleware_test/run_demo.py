from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from middleware_test.graph_agent import build_agent_graph, export_mermaid  # noqa: E402


def main() -> None:
    agent = build_agent_graph()

    print("=== mermaid ===")
    mermaid = export_mermaid(agent)
    print(mermaid)
    (Path(__file__).resolve().parent / "agent_graph.mmd").write_text(mermaid, encoding="utf-8")

    print("=== invoke ===")
    result = agent.invoke({"messages": [{"role": "user", "content": "用一句话解释什么是LangGraph"}]})
    print(result)


if __name__ == "__main__":
    main()

