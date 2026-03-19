from langgraph.graph import StateGraph

from demo.model import GraphMsgState

# model = init_chat_model("gpt-4.1", profile=ModelProfile.deepseek32_fast_profile())
builder = StateGraph(GraphMsgState)
builder.add_node()
builder.add_node()