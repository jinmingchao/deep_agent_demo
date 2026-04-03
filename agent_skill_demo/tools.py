"""Skills 配套工具：四则运算、模拟法律知识检索与 YCYT MySQL 查询。"""

from __future__ import annotations

import ast
import operator
import re
from typing import Any

from langchain_core.tools import tool

from .ycyt_database import (
    YCYT_DATABASE_CTR_DATABASE,
    YCYT_DATABASE_HOST,
    YCYT_DATABASE_NAME,
    YCYT_DATABASE_PASSWORD,
    YCYT_DATABASE_PAY_DATABASE,
    YCYT_DATABASE_PORT,
)

# 仅四则运算（加减乘除）
_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _eval_arith(node: ast.AST) -> float | int:
    if isinstance(node, ast.Expression):
        return _eval_arith(node.body)
    if isinstance(node, ast.Constant):
        v = node.value
        if isinstance(v, bool):
            raise ValueError("不支持布尔值")
        if isinstance(v, (int, float)):
            return v
        raise ValueError("仅支持数字常量")
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.UAdd):
            return +_eval_arith(node.operand)
        if isinstance(node.op, ast.USub):
            return -_eval_arith(node.operand)
        raise ValueError("不支持的单目运算符")
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _BINOPS:
            raise ValueError("仅支持加、减、乘、除与括号")
        left = _eval_arith(node.left)
        right = _eval_arith(node.right)
        if op_type is ast.Div and right == 0:
            raise ValueError("除数不能为零")
        fn = _BINOPS[op_type]
        out: Any = fn(left, right)
        return out
    raise ValueError("表达式结构不支持，请使用四则运算与括号")


@tool
def arithmetic_calculate(expression: str) -> str:
    """计算仅含数字与四则运算（及括号）的数学表达式。

    参数 expression：标准数学表达式字符串，例如 "3 + 5 * 2" 或 "(10 - 4) / 2"。
    返回计算结果的字符串表示；出错时返回简短错误说明。
    """
    expr = (expression or "").strip()
    if not expr:
        return "错误：表达式为空"
    try:
        tree = ast.parse(expr, mode="eval")
        result = _eval_arith(tree)
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)
    except SyntaxError as e:
        return f"语法错误：{e.msg}"
    except (ValueError, ZeroDivisionError, TypeError) as e:
        return f"计算失败：{e}"


# 模拟法律知识库（非真实法律服务，仅供演示）
_LEGAL_FAQ: list[tuple[list[str], str]] = [
    (
        ["劳动合同", "书面", "订立"],
        "【模拟条文说明】建立劳动关系，应当订立书面劳动合同。已建立劳动关系但未同时订立书面合同的，"
        "应当自用工之日起一个月内订立书面劳动合同（依据《劳动合同法》第十条等规定的精神）。"
        "具体争议请咨询专业律师。",
    ),
    (
        ["试用期", "工资"],
        "【模拟条文说明】劳动者在试用期的工资不得低于本单位相同岗位最低档工资或者劳动合同约定工资的百分之八十，"
        "并不得低于用人单位所在地的最低工资标准（《劳动合同法》第二十条精神）。此为示意，以当地规定为准。",
    ),
    (
        ["民事", "诉讼时效", "三年"],
        "【模拟条文说明】向人民法院请求保护民事权利的诉讼时效期间一般为三年；法律另有规定的依照其规定。"
        "自权利人知道或应当知道权利受到损害以及义务人之日起算（《民法典》第一百八十八条精神）。",
    ),
    (
        ["离婚", "冷静期"],
        "【模拟条文说明】协议离婚存在冷静期制度：婚姻登记机关收到申请之日起三十日内，任何一方不愿离婚的，"
        "可撤回申请；期满后三十日内双方应亲自申请发给离婚证（《民法典》相关条款精神）。",
    ),
    (
        ["继承", "法定继承", "顺序"],
        "【模拟条文说明】法定继承第一顺序一般为配偶、子女、父母；第二顺序为兄弟姐妹、祖父母、外祖父母。"
        "继承开始后，由第一顺序继承人继承，第二顺序不继承（《民法典》继承编精神）。",
    ),
]


@tool
def legal_knowledge_query(query: str) -> str:
    """模拟法律知识库检索：根据用户问题返回与关键词匹配的示意性法律常识说明。

    参数 query：用户的法律相关问题或关键词（中文）。
    返回：匹配的模拟条文说明；若无匹配则返回通用提示。
    """
    q = (query or "").strip()
    if not q:
        return "请提供具体的法律问题或关键词。"

    hits: list[str] = []
    for keywords, text in _LEGAL_FAQ:
        if any(kw in q for kw in keywords):
            hits.append(text)

    if not hits:
        return (
            "【模拟库未命中】未在演示知识库中找到与您问题直接匹配的条目。"
            "本工具仅为演示，不构成法律意见；请咨询执业律师或查阅正式法规文本。"
        )

    return "\n\n---\n\n".join(hits)


_DB_ALIASES: dict[str, str] = {
    "ctr": YCYT_DATABASE_CTR_DATABASE,
    "pay": YCYT_DATABASE_PAY_DATABASE,
    "rds_ycyt_ctr": YCYT_DATABASE_CTR_DATABASE,
    "rds_ycyt_pay": YCYT_DATABASE_PAY_DATABASE,
}

_READ_ONLY_PREFIXES = (
    "select",
    "show",
    "describe",
    "desc",
    "explain",
    "with",  # CTE，常用于只读分析
)


def _normalize_sql(sql: str) -> str:
    return (sql or "").strip().rstrip(";")


def _first_sql_keyword(sql: str) -> str:
    for raw in (sql or "").splitlines():
        line = raw.strip()
        if not line or line.startswith("--"):
            continue
        if line.startswith("/*"):
            continue
        parts = line.split()
        if not parts:
            continue
        return parts[0].lower().rstrip(";")
    return ""


def _is_read_only_sql(sql: str) -> bool:
    s = _normalize_sql(sql)
    if not s:
        return False
    first = _first_sql_keyword(s)
    return first in _READ_ONLY_PREFIXES


@tool
def mysql_ycyt_query(database: str, sql: str) -> str:
    """在 YCYT 业务库执行只读 SQL（SELECT / SHOW / DESCRIBE / EXPLAIN / WITH…SELECT），返回文本化结果。

    参数 database：目标库标识，取值为 ctr、pay，或完整库名 rds_ycyt_ctr、rds_ycyt_pay。
    参数 sql：单条只读 SQL 语句。
    """
    try:
        import pymysql
        from pymysql.cursors import DictCursor
    except ImportError:
        return "错误：未安装 pymysql，请执行 pip install pymysql"

    key = (database or "").strip().lower()
    db_name = _DB_ALIASES.get(key)
    if not db_name:
        return (
            f"错误：未知 database={database!r}，请使用 ctr、pay、"
            f"{YCYT_DATABASE_CTR_DATABASE!r} 或 {YCYT_DATABASE_PAY_DATABASE!r}"
        )

    stmt = _normalize_sql(sql)
    if not stmt:
        return "错误：SQL 为空"
    if not _is_read_only_sql(stmt):
        return "错误：仅允许只读查询（SELECT、SHOW、DESCRIBE、EXPLAIN、WITH…）"

    conn = None
    try:
        conn = pymysql.connect(
            host=YCYT_DATABASE_HOST,
            port=YCYT_DATABASE_PORT,
            user=YCYT_DATABASE_NAME,
            password=YCYT_DATABASE_PASSWORD,
            database=db_name,
            charset="utf8mb4",
            cursorclass=DictCursor,
        )
        with conn.cursor() as cur:
            cur.execute(stmt)
            rows = cur.fetchall()
    except Exception as e:
        return f"查询失败：{e}"
    finally:
        if conn is not None:
            conn.close()

    if not rows:
        return "（无行）"
    # DictCursor：每行 dict；控制行数与宽度避免撑爆上下文
    max_rows = 200
    if len(rows) > max_rows:
        tail = f"\n… 共 {len(rows)} 行，仅显示前 {max_rows} 行"
        rows = rows[:max_rows]
    else:
        tail = f"\n（共 {len(rows)} 行）"
    lines: list[str] = []
    for i, row in enumerate(rows, 1):
        lines.append(f"{i}: {row}")
    return "\n".join(lines) + tail


SKILL_TOOLS = [arithmetic_calculate, legal_knowledge_query, mysql_ycyt_query]
