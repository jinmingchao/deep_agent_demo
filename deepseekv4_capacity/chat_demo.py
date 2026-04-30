from openai import OpenAI
import os

from utils import env_util

# 修复中文编码问题（关键！）
os.environ["PYTHONIOENCODING"] = "utf-8"

# 初始化客户端
client = OpenAI(
    api_key=env_util.DEEPSEEK_API_KEY,
    base_url=env_util.DEEPSEEK_BASE_URL,
)

# 100% 正确的请求格式
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "user", "content": "1.01的365次方等于多少？请写出详细计算过程"}
    ],
    # 推理强度
    reasoning_effort="high",  # max = Pro-Max 模式
    # 思考链（已修复官方必填格式）
    extra_body={
        "thinking": {
            "type": "enabled"
        }
    }
)

# 输出结果
print("模型回答：")
print(response.choices[0].message.model_extra.get('reasoning_content'))
print("-"*50)
print(response.choices[0].message.content)
