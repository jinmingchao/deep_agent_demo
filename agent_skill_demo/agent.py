"""基于 deepagents.create_deep_agent 与 SkillsMiddleware 的多 Skill 智能体。"""

from __future__ import annotations

from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langgraph.types import Checkpointer

from .model_config import default_chat_model
from .tools import SKILL_TOOLS

_DEMO_ROOT = Path(__file__).resolve().parent

ORCHESTRATOR_PROMPT = """你是具备多种「技能（Skill）」的智能助手。系统消息中会列出可用技能及其适用场景。

**路由原则**
- 用户问题涉及数值计算、算式、四则运算时：遵循 **arithmetic** 技能，并调用 **arithmetic_calculate**。
- 用户问题涉及法律常识、权利义务、法规概念（演示级）时：遵循 **legal-knowledge** 技能，并调用 **legal_knowledge_query**。
- 用户需要从 YCYT 业务 MySQL（rds_ycyt_ctr / rds_ycyt_pay）查表、跑只读 SQL、看库表结构时：遵循 **mysql-ycyt** 技能，并调用 **mysql_ycyt_query**（参数 database 选 ctr 或 pay）。
- 用户希望用张雪峰的视角分析教育选择、志愿填报、职业规划，或提到「张雪峰」「雪峰视角」「用张雪峰的角度」等时：遵循 **zhangxuefeng-skill** 技能。先通过 **read_file** / **glob** / **grep** 按需查阅该 Skill 目录下 `references/research/` 等调研材料；需要事实数据时诚实说明信息时效，勿编造具体就业/分数线数字。
- 若与以上均无关，可直接用自然语言回答，无需勉强调用工具。

回答时保持简洁；调用工具后请整合工具输出再回复用户。"""


def _backend_factory(_runtime):  # noqa: ARG001
    return FilesystemBackend(
        root_dir=str(_DEMO_ROOT),
        virtual_mode=True,
        max_file_size_mb=10,
    )


def build_agent(model=None, checkpointer: Checkpointer | None = None):
    """创建包含 arithmetic / legal-knowledge / mysql-ycyt / zhangxuefeng-skill 的 Deep Agent。

    model 默认使用 DEEPSEEK_API_KEY 对应的 ChatDeepSeek。
    checkpointer 用于多轮对话持久化状态（例如控制台交互时使用 MemorySaver）。
    """
    m = model if model is not None else default_chat_model()
    return create_deep_agent(
        model=m,
        tools=list(SKILL_TOOLS),
        system_prompt=ORCHESTRATOR_PROMPT,
        backend=_backend_factory,
        skills=["/skills/demo/"],
        name="skill_orchestrator",
        checkpointer=checkpointer,
    )


