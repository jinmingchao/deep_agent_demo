"""仅加载 DeepSeek 聊天模型，避免导入 src.utils.llm_util 时初始化其它需密钥的客户端。"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek

_REPO = Path(__file__).resolve().parents[1]
for _env in (_REPO / ".env", _REPO / "src" / ".env"):
    if _env.is_file():
        load_dotenv(_env, override=True)
        break
else:
    load_dotenv(override=True)


def default_chat_model() -> ChatDeepSeek:
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        msg = "请设置环境变量 DEEPSEEK_API_KEY（可在项目根目录配置 .env）"
        raise RuntimeError(msg)
    base = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    return ChatDeepSeek(
        model="deepseek-chat",
        temperature=0.5,
        streaming=False,
        api_key=key,
        base_url=base,
    )
