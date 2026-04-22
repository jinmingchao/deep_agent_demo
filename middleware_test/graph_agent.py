from __future__ import annotations

import sys
import tempfile
import base64
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


def build_agent_graph(*, tools=None):
    """使用 LangGraph API（通过 create_agent）生成一张包含 agent 的图。"""
    agent_graph = create_agent(
        model=deepseek_chat,
        tools=tools or [],
        system_prompt="你是一个简洁的助手，请用中文回答。",
        middleware=[FullHooksMiddleware(tag="demo")],
    )
    return agent_graph


def export_mermaid(graph) -> str:
    g = graph.get_graph()
    if hasattr(g, "draw_mermaid"):
        return g.draw_mermaid()
    return str(g)


def export_png(graph, *, out_path: Path) -> Path:
    """Render the agent graph directly to a PNG file.

    Uses a public renderer (tries mermaid.ink, then kroki) to produce a PNG.
    """
    mermaid = export_mermaid(graph)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen

    data: bytes | None = None

    # 1) Try mermaid.ink (GET with base64 payload)
    try:
        payload = base64.urlsafe_b64encode(mermaid.encode("utf-8")).decode("ascii").rstrip("=")
        url = f"https://mermaid.ink/img/{payload}"
        req = Request(
            url,
            headers={
                "Accept": "image/png",
                # Some environments get blocked without a UA.
                "User-Agent": "middleware_test/1.0 (python urllib)",
            },
        )
        with urlopen(req, timeout=30) as resp:  # noqa: S310
            data = resp.read()
    except (HTTPError, URLError):
        data = None

    # 2) Fallback to kroki (POST raw diagram)
    if data is None:
        req = Request(
            "https://kroki.io/mermaid/png",
            data=mermaid.encode("utf-8"),
            headers={
                "Content-Type": "text/plain; charset=utf-8",
                "Accept": "image/png",
                "User-Agent": "middleware_test/1.0 (python urllib)",
            },
            method="POST",
        )
        with urlopen(req, timeout=30) as resp:  # noqa: S310
            data = resp.read()

    out_path.write_bytes(data)

    return out_path


if __name__ == "__main__":
    graph = build_agent_graph()
    png = export_png(graph, out_path=Path(__file__).resolve().parent / "agent_graph.png")
    print(str(png))

