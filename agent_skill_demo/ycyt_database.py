"""YCYT MySQL 连接配置，供 `tools.mysql_ycyt_query` 使用。

与 `src/utils/env_util.py` 同源，确保与项目其余模块使用同一套主机、账号与库名。
"""

from __future__ import annotations

import sys
from pathlib import Path

# agent_skill_demo 的上一级为仓库根目录，保证可 `from src.utils.env_util import ...`
_repo_root = Path(__file__).resolve().parents[1]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from src.utils.env_util import (  # noqa: E402
    YCYT_DATABASE_CTR_DATABASE,
    YCYT_DATABASE_HOST,
    YCYT_DATABASE_NAME,
    YCYT_DATABASE_PASSWORD,
    YCYT_DATABASE_PAY_DATABASE,
    YCYT_DATABASE_PORT,
)

__all__ = [
    "YCYT_DATABASE_CTR_DATABASE",
    "YCYT_DATABASE_HOST",
    "YCYT_DATABASE_NAME",
    "YCYT_DATABASE_PASSWORD",
    "YCYT_DATABASE_PAY_DATABASE",
    "YCYT_DATABASE_PORT",
]
