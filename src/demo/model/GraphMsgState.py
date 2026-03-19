import datetime
import time
from typing import Annotated, List, Dict, Any

from langchain_core.messages import BaseMessage
from langgraph.graph import MessagesState, add_messages
from pydantic.v1 import BaseModel, Field


class GraphMsgState(BaseModel):
    """Agent状态管理"""
    # 用户输入
    query: str = Field(description="用户输入的问题")

    # 消息历史（使用add_messages归约器自动追加）
    messages: Annotated[List[BaseMessage], add_messages] = Field(
        default_factory=list,
        description="对话历史"
    )

    # # 工具执行结果记录
    # tool_results: List[Dict[str, Any]] = Field(
    #     default_factory=list,
    #     description="工具执行结果"
    # )
    #
    # # 最终答案
    # answer: str = Field(default="", description="最终回答")
    #
    # # 会话信息
    # session_id: str = Field(default_factory=lambda: f"session_{int(time.time())}")
    # created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    class Config:
        arbitrary_types_allowed = True