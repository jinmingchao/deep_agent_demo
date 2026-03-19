# ---------- 2.1 天气查询工具 ----------
from datetime import datetime
from typing import Optional

from langchain_core.tools import tool


@tool(parse_docstring=True)
def get_weather(
        city: str,
        date: Optional[str] = None
) -> str:
    """
    查询指定城市的天气信息

    Args:
        city: 城市名称，如"北京"、"上海"、"纽约"
        date: 日期，格式为YYYY-MM-DD，不填则查询今天

    Returns:
        天气信息字符串
    """
    # 模拟天气数据（实际使用时替换为真实API）
    weather_data = {
        "北京": {"temp": "15°C", "condition": "晴朗", "humidity": "45%", "wind": "3级"},
        "上海": {"temp": "18°C", "condition": "多云", "humidity": "65%", "wind": "4级"},
        "广州": {"temp": "25°C", "condition": "小雨", "humidity": "80%", "wind": "2级"},
        "深圳": {"temp": "26°C", "condition": "阴天", "humidity": "75%", "wind": "3级"},
        "纽约": {"temp": "10°C", "condition": "多云转晴", "humidity": "55%", "wind": "5级"},
        "伦敦": {"temp": "8°C", "condition": "小雨", "humidity": "85%", "wind": "4级"},
        "东京": {"temp": "16°C", "condition": "晴朗", "humidity": "50%", "wind": "2级"},
    }

    # 日期处理
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    # 获取城市天气
    if city in weather_data:
        data = weather_data[city]
        return (
            f"🌤️ {city} {date} 天气：\n"
            f"温度：{data['temp']}\n"
            f"天气状况：{data['condition']}\n"
            f"湿度：{data['humidity']}\n"
            f"风力：{data['wind']}"
        )
    else:
        return f"❌ 抱歉，暂不支持 {city} 的天气查询"


# ---------- 2.2 计算器工具 ----------
@tool(parse_docstring=True)
def calculator(expression: str) -> str:
    """
    执行数学计算

    Args:
        expression: 数学表达式，如 "2 + 2 * 3"、"(15 + 5) / 2"、"sqrt(16)" 等

    Returns:
        计算结果
    """
    # 安全计算：只允许基本运算
    allowed_chars = set("0123456789+-*/(). sqrtpow")

    # 安全检查
    if not all(c in allowed_chars or c.isdigit() for c in expression):
        return "❌ 表达式包含非法字符"

    # 禁止使用的内置函数
    forbidden = ['__', 'import', 'eval', 'exec', 'open', 'file']
    if any(word in expression.lower() for word in forbidden):
        return "❌ 表达式包含危险操作"

    try:
        # 使用更安全的方式计算
        # 注意：这里简化处理，实际生产环境应使用更安全的方法
        namespace = {
            'sqrt': lambda x: x ** 0.5,
            'pow': pow,
            'abs': abs,
            'round': round
        }

        # 预处理：替换数学函数
        expr = expression.replace('^', '**')

        result = eval(expr, {"__builtins__": {}}, namespace)
        return f"🧮 计算结果：{expression} = {result}"
    except ZeroDivisionError:
        return "❌ 错误：除数不能为0"
    except Exception as e:
        return f"❌ 计算错误：{str(e)}"


# ---------- 2.4 翻译工具 ----------
@tool(parse_docstring=True)
def translate_text(text: str, target_language: str = "中文") -> str:
    """
    翻译文本

    Args:
        text: 要翻译的文本
        target_language: 目标语言，如"中文"、"英语"、"日语"等

    Returns:
        翻译结果
    """
    # 模拟翻译（实际使用可接入Google Translate API等）
    translations = {
        "hello": {"中文": "你好", "日语": "こんにちは", "韩语": "안녕하세요"},
        "goodbye": {"中文": "再见", "日语": "さようなら", "韩语": "안녕히 계세요"},
        "thank you": {"中文": "谢谢", "日语": "ありがとう", "韩语": "감사합니다"},
        "你好": {"英语": "Hello", "日语": "こんにちは", "韩语": "안녕하세요"},
    }

    # 简单翻译逻辑
    text_lower = text.lower().strip()

    # 检查常用短语
    for key, trans_map in translations.items():
        if key in text_lower or key == text:
            if target_language in trans_map:
                return f"🔄 翻译结果：{trans_map[target_language]}"

    # 模拟其他翻译
    mock_translations = {
        "中文": f"[模拟翻译] {text}",
        "英语": f"[Simulated translation] {text}",
        "日语": f"[シミュレーション翻訳] {text}",
        "韩语": f"[시뮬레이션 번역] {text}",
    }

    return f"🔄 翻译结果：{mock_translations.get(target_language, text)} (模拟翻译)"

@tool
def news_search(topic: str) -> str:
    """搜索最新新闻"""
    return f"关于{topic}的最新新闻：..."

@tool
def stock_query(symbol: str) -> str:
    """查询股票信息，输入股票代码"""
    return f"{symbol}当前股价：100元"