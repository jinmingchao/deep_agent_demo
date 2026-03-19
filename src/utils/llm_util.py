from langchain.chat_models import init_chat_model
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.chat_models import ChatZhipuAI
from zhipuai import ZhipuAI
from langchain_ollama import OllamaLLM, ChatOllama
from langchain_qwq import ChatQwen

from utils import env_util

# 华为云 - openAI调用
huawei_openai_llm = ChatOpenAI(
    model="DeepSeek-R1",
    temperature=0.5,
    api_key=env_util.HUAWEIYUN_API_KEY,
    base_url=env_util.HUAWEIYUN_BASE_URL
)
# 阿里云百炼- openAI库调用
bailian_openai_llm = ChatOpenAI(
    model="deepseek-v3",
    # model="deepseek-r1",
    # model="qwen3-max",
    temperature=0.5,
    api_key=env_util.BAILIAN_API_KEY,
    base_url=env_util.BAILIAN_BASE_URL
)

# 阿里云百炼- langchain-deepseek库调用
bailian_langchain_llm = ChatDeepSeek(
    model="deepseek-v3",
    temperature=0.5,
    api_key=env_util.BAILIAN_API_KEY,
    base_url=env_util.BAILIAN_BASE_URL
)

xiaoai_openai_llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.5,
    api_key=env_util.XIAOAI_API_KEY,
    base_url=env_util.XIAOAI_BASE_URL
)


#速率限制模型
rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.01,  # 每10秒允许1个请求
    check_every_n_seconds=0.1,  # 每100毫秒检查一次是否允许发出请求
    max_bucket_size=10,  #  控制最大突发请求数量
)

rate_limit_llm = init_chat_model(  # V1.0后才有的写法
    model="deepseek-r1-0528",
    model_provider="openai",
    api_key=env_util.BAILIAN_API_KEY,
    base_url=env_util.BAILIAN_BASE_URL,
    rate_limiter=rate_limiter
)

local_qwen3_8b_llm = ChatOllama(
        model="qwen3:8b",  # 模型名称，必须与 Ollama 中运行的一致
        base_url="http://localhost:11434",  # Ollama 本地服务地址
        temperature=0.1,  # 温度值，越低越稳定
        num_ctx=4096  # 上下文窗口大小
    )

local_qwen2_7b_llm = ChatOllama(
        model="qwen2:7b",  # 模型名称，必须与 Ollama 中运行的一致
        base_url="http://localhost:11434",  # Ollama 本地服务地址
        temperature=0.1,  # 温度值，越低越稳定
        num_ctx=40 *1024  # 上下文窗口大小
    )


# 智谱
zhipu_ai_llm = ChatZhipuAI(
    model="glm-4.7-flash", #智谱免费模型，巨慢无比
    temperature=0.1,
    streaming=False,
    api_key=env_util.ZHIPU_API_KEY,
    base_url=env_util.ZHIPU_API_BASE_URL
)

# deepseek v3.2
deepseek_chat = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.5,
    streaming=False,
    api_key=env_util.DEEPSEEK_API_KEY,
    base_url=env_util.DEEPSEEK_BASE_URL
)

text_embedding = OpenAIEmbeddings(
    api_key=env_util.BAILIAN_API_KEY,
    base_url=env_util.BAILIAN_BASE_URL,
    model="text-embedding-v4",
    dimensions=1024,
    check_embedding_ctx_length=False  # 关键参数
)

multi_modal_llm = ChatOpenAI(  # 多模态大模型
    model='qwen3-vl-plus',
    api_key=env_util.BAILIAN_API_KEY,
    base_url=env_util.BAILIAN_BASE_URL,
)


zhipuai_client = ZhipuAI(api_key=env_util.ZHIPU_API_KEY)


ali_qwen3_max = ChatQwen(
    model="qwen3-max",
    temperature=0.5,
    api_key=env_util.BAILIAN_API_KEY,
    base_url=env_util.BAILIAN_BASE_URL
)