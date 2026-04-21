from __future__ import annotations

import time
from typing import Any, Awaitable, Callable, TypeVar

from langchain.agents.middleware import AgentMiddleware
from langchain.agents.middleware.types import ExtendedModelResponse, ModelRequest, ModelResponse
from langchain_core.messages import AIMessage
from langgraph.runtime import Runtime

StateT = TypeVar("StateT")
ContextT = TypeVar("ContextT")
ResponseT = TypeVar("ResponseT")


class FullHooksMiddleware(AgentMiddleware[StateT, ContextT, ResponseT]):
    """覆盖 AgentMiddleware 的全部 agent/model 钩子。

    - 在 stdout 打印钩子触发顺序与耗时
    - 演示通过返回 dict 更新 state（可选）
    """

    def __init__(self, *, tag: str = "full-hooks") -> None:
        self.tag = tag
        self.tools = ()

    def _log(self, event: str, extra: dict[str, Any] | None = None) -> None:
        payload = {"tag": self.tag, "event": event, **(extra or {})}
        print(f"[middleware] {payload}")

    def before_agent(self, state: StateT, runtime: Runtime[ContextT]) -> dict[str, Any] | None:
        self._log("before_agent")
        return None

    async def abefore_agent(
        self, state: StateT, runtime: Runtime[ContextT]
    ) -> dict[str, Any] | None:
        self._log("abefore_agent")
        return None

    def before_model(self, state: StateT, runtime: Runtime[ContextT]) -> dict[str, Any] | None:
        self._log("before_model")
        return None

    async def abefore_model(
        self, state: StateT, runtime: Runtime[ContextT]
    ) -> dict[str, Any] | None:
        self._log("abefore_model")
        return None

    def after_model(self, state: StateT, runtime: Runtime[ContextT]) -> dict[str, Any] | None:
        self._log("after_model")
        return None

    async def aafter_model(
        self, state: StateT, runtime: Runtime[ContextT]
    ) -> dict[str, Any] | None:
        self._log("aafter_model")
        return None

    def wrap_model_call(
        self,
        request: ModelRequest[ContextT],
        handler: Callable[[ModelRequest[ContextT]], ModelResponse[ResponseT]],
    ) -> ModelResponse[ResponseT] | AIMessage | ExtendedModelResponse[ResponseT]:
        t0 = time.perf_counter()
        self._log("wrap_model_call.before", {"model": getattr(request.model, "model", None)})
        resp = handler(request)
        dt_ms = round((time.perf_counter() - t0) * 1000, 2)
        self._log("wrap_model_call.after", {"elapsed_ms": dt_ms})
        return resp

    async def awrap_model_call(
        self,
        request: ModelRequest[ContextT],
        handler: Callable[[ModelRequest[ContextT]], Awaitable[ModelResponse[ResponseT]]],
    ) -> ModelResponse[ResponseT] | AIMessage | ExtendedModelResponse[ResponseT]:
        t0 = time.perf_counter()
        self._log("awrap_model_call.before", {"model": getattr(request.model, "model", None)})
        resp = await handler(request)
        dt_ms = round((time.perf_counter() - t0) * 1000, 2)
        self._log("awrap_model_call.after", {"elapsed_ms": dt_ms})
        return resp

    def after_agent(self, state: StateT, runtime: Runtime[ContextT]) -> dict[str, Any] | None:
        self._log("after_agent")
        return None

    async def aafter_agent(
        self, state: StateT, runtime: Runtime[ContextT]
    ) -> dict[str, Any] | None:
        self._log("aafter_agent")
        return None
