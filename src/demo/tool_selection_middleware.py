from langchain.agents import create_agent
from langchain.agents.middleware import LLMToolSelectorMiddleware
from langgraph.graph import StateGraph
from pydantic.v1 import create_model
from demo.tools.tools_1 import get_weather,calculator,translate_text
from demo.model import GraphMsgState
from utils.llm_util import deepseek_chat, ali_qwen3_max

# model = init_chat_model("gpt-4.1", profile=ModelProfile.deepseek32_fast_profile())
# builder = StateGraph(GraphMsgState)
# builder.add_node()
# builder.add_node()

m = LLMToolSelectorMiddleware(
            model=deepseek_chat,
            max_tools=1,
            always_include=["calculator"],
        )
m.before_agent()

agent = create_agent(
    model=deepseek_chat,
    system_prompt="请仔细阅读提供给你的工具列表，并谨慎选用工具并返回",
    tools=[get_weather, calculator, translate_text],
    middleware=[
        LLMToolSelectorMiddleware(
            model=deepseek_chat,
            max_tools=1,
            always_include=["calculator"],
        ),
    ],
);

state = {
    "messages":["帮我查一下北京今天的天气"]
}
response = agent.invoke(state)
print(response)
