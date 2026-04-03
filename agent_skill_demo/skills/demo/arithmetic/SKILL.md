---
name: arithmetic
description: 处理四则运算与括号表达式求值。当用户要求计算、加减乘除、数值表达式、算式结果时使用本技能；关键词如「计算」「等于多少」「加」「减」「乘」「除」。
license: MIT
allowed-tools: arithmetic_calculate
---

# 四则运算 Skill

## When to Use

- 用户给出数学表达式或自然语言描述的计算需求（先整理成标准表达式再调用工具）。
- 涉及 `+`、`-`、`*`、`/`、括号与数字的求值。

## Instructions

1. 将用户意图转化为**单一**数学表达式字符串（半角运算符），例如 `3 + 5 * 2`。
2. 调用工具 **`arithmetic_calculate`**，传入参数 `expression`。
3. 用自然语言向用户复述结果；若工具返回错误信息，向用户说明并请求修正表达式。

## Limitations

- 本技能仅通过 `arithmetic_calculate` 完成数值计算，不负责法律咨询或其它领域。
