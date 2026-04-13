import os
from pathlib import Path

from dotenv import load_dotenv

# 仓库根目录（src/utils/env_util.py → parents[2]）
_REPO_ROOT = Path(__file__).resolve().parents[2]
# 无论从哪个工作目录启动，都加载项目根与 src 下的 .env（后者同名键可覆盖前者）
load_dotenv(_REPO_ROOT / ".env", override=True)
load_dotenv(_REPO_ROOT / "src" / ".env", override=True)

BAILIAN_BASE_URL = os.getenv("BAILIAN_BASE_URL")
BAILIAN_API_KEY = os.getenv("BAILIAN_API_KEY")

XIAOAI_BASE_URL = os.getenv("XIAOAI_BASE_URL")
XIAOAI_API_KEY = os.getenv("XIAOAI_API_KEY")

HUAWEIYUN_API_KEY = os.getenv("HUAWEIYUN_API_KEY")
HUAWEIYUN_BASE_URL = os.getenv("HUAWEIYUN_BASE_URL")

ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
ZHIPU_API_BASE_URL=  os.getenv("ZHIPU_API_BASE_URL")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

# postgresql
POSTGRESQL_DB_URI=os.getenv("POSTGRESQL_DB_URI")

# mysql（YCYT）— 与 agent_skill_demo.tools.mysql_ycyt_query / ycyt_database 共用
# 优先使用环境变量或上述 .env；未设置时沿用原「work」本地默认值
YCYT_DATABASE_HOST = os.getenv("YCYT_DATABASE_HOST", "127.0.0.1")
YCYT_DATABASE_PORT = int(os.getenv("YCYT_DATABASE_PORT", "3306"))
YCYT_DATABASE_NAME = os.getenv("YCYT_DATABASE_NAME", "root")
YCYT_DATABASE_PASSWORD = os.getenv("YCYT_DATABASE_PASSWORD", "root")
YCYT_DATABASE_CTR_DATABASE = os.getenv("YCYT_DATABASE_CTR_DATABASE", "rds_ycyt_ctr")
YCYT_DATABASE_PAY_DATABASE = os.getenv("YCYT_DATABASE_PAY_DATABASE", "rds_ycyt_pay")