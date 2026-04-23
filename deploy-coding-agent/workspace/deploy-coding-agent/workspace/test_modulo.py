#!/usr/bin/env python3
"""
测试取余运算
"""

# 测试Python的%运算符
test_cases = [
    ("10%3", 1),
    ("15%4", 3),
    ("7%2", 1),
    ("10.5%3", 1.5),
    ("5%2.5", 0.0),
    ("8%3", 2),
    ("12%5", 2),
    ("9%3", 0),
    ("7.5%2", 1.5),
    ("10%2.5", 0.0),
]

print("测试Python的%运算符:")
print("=" * 40)

for expr, expected in test_cases:
    try:
        result = eval(expr)
        status = "✓" if abs(result - expected) < 0.0001 else "✗"
        print(f"{status} {expr} = {result} (期望: {expected})")
    except Exception as e:
        print(f"✗ {expr} 错误: {e}")

print("\n测试计算器后端的取余运算:")
print("=" * 40)

# 测试计算器后端的逻辑
from decimal import Decimal

def test_calculator_modulo():
    """模拟计算器后端的取余运算"""
    test_cases = [
        (Decimal('10'), Decimal('3'), Decimal('1')),
        (Decimal('15'), Decimal('4'), Decimal('3')),
        (Decimal('7'), Decimal('2'), Decimal('1')),
        (Decimal('10.5'), Decimal('3'), Decimal('1.5')),
        (Decimal('5'), Decimal('2.5'), Decimal('0.0')),
    ]
    
    for x, y, expected in test_cases:
        try:
            if y == 0:
                result = float('inf')
            else:
                result = x % y
            
            status = "✓" if abs(result - expected) < Decimal('0.0001') else "✗"
            print(f"{status} {x} % {y} = {result} (期望: {expected})")
        except Exception as e:
            print(f"✗ {x} % {y} 错误: {e}")

test_calculator_modulo()

print("\n测试表达式解析:")
print("=" * 40)

# 测试表达式解析
expressions = [
    "10%3",
    "15%4+2",
    "3+7%2",
    "10%3*2",
    "(10+5)%3",
]

for expr in expressions:
    # 替换符号
    normalized = expr.replace('×', '*').replace('÷', '/')
    print(f"原始: {expr}")
    print(f"标准化: {normalized}")
    
    try:
        result = eval(normalized)
        print(f"结果: {result}")
    except Exception as e:
        print(f"错误: {e}")
    print()