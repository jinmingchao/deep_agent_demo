from deepagents import FilesystemMiddleware
from deepagents.backends import CompositeBackend, FilesystemBackend
from langchain.agents import create_agent
from utils.llm_util import deepseek_chat
import os

WORKSPACE_DIR = "C:/python_workspace/deep_agent_demo/agent_workspace"
os.makedirs(WORKSPACE_DIR, exist_ok=True)

def create_backend(runtime):
    """完整的沙箱环境：真实文件系统 + 命令执行能力"""
    return FilesystemBackend(
        root_dir=WORKSPACE_DIR,
        virtual_mode=True,  # 安全模式：防止访问 root_dir 外的文件
        max_file_size_mb=100
    )
    # FilesystemBackend 默认支持 execute 工具！

agent = create_agent(
    model=deepseek_chat,
    middleware=[FilesystemMiddleware(backend=create_backend)]
)

# 现在可以同时操作文件和执行命令
response = agent.invoke({
    "messages": [{"role": "user", "content": """
    请帮我：
    1. 在 /workspace/ 下创建一个 Python 文件 test.py，内容为：
       ```python
       print("Hello from Python!")
       with open('output.txt', 'w') as f:
           f.write('File created by Python')
                  """}]})

print(response)