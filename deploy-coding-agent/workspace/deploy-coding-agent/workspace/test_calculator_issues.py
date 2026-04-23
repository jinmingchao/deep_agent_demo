#!/usr/bin/env python3
"""
测试计算器问题
1. 开方运算：默认的0不会去掉
2. 取余运算：结果不正确
"""

import sys
sys.path.insert(0, '.')

# 导入计算器类
from server import Calculator

def test_sqrt_issue():
    """测试开方运算问题"""
    print("=" * 50)
    print("测试开方运算问题")
    print("=" * 50)
    
    calculator = Calculator()
    
    # 测试用例1: √9 应该等于 3
    test_cases = [
        ("√9", "3"),
        ("√16", "4"),
        ("√(9+16)", "5"),  # √(9+16) = √25 = 5
        ("√2", "1.4142135624"),  # 近似值
    ]
    
    for expr, expected in test_cases:
        try:
            result = calculator.calculate(expr)
            print(f"表达式: {expr}")
            print(f"期望结果: {expected}")
            print(f"实际结果: {result}")
            print(f"测试: {'通过' if abs(float(result) - float(expected)) < 0.0001 else '失败'}")
            print()
        except Exception as e:
            print(f"表达式: {expr} 出错: {e}")
            print()

def test_modulo_issue():
    """测试取余运算问题"""
    print("=" * 50)
    print("测试取余运算问题")
    print("=" * 50)
    
    calculator = Calculator()
    
    # 测试用例
    test_cases = [
        ("10%3", "1"),      # 10 mod 3 = 1
        ("15%4", "3"),      # 15 mod 4 = 3
        ("7%2", "1"),       # 7 mod 2 = 1
        ("8%3", "2"),       # 8 mod 3 = 2
        ("5%5", "0"),       # 5 mod 5 = 0
        ("3.5%2", "1.5"),   # 3.5 mod 2 = 1.5
    ]
    
    for expr, expected in test_cases:
        try:
            result = calculator.calculate(expr)
            print(f"表达式: {expr}")
            print(f"期望结果: {expected}")
            print(f"实际结果: {result}")
            
            # 浮点数比较
            if expected == "0":
                test_passed = float(result) == 0
            else:
                test_passed = abs(float(result) - float(expected)) < 0.0001
            
            print(f"测试: {'通过' if test_passed else '失败'}")
            print()
        except Exception as e:
            print(f"表达式: {expr} 出错: {e}")
            print()

def test_frontend_sqrt_behavior():
    """模拟前端开方按钮行为"""
    print("=" * 50)
    print("模拟前端开方按钮行为")
    print("=" * 50)
    
    # 模拟前端状态
    calculator_state = {
        'expression': '0',
        'result': '0',
        'isNewExpression': True
    }
    
    def appendOperation(operator):
        """模拟前端的appendOperation函数"""
        if calculator_state['isNewExpression'] and operator not in ['(', ')']:
            # 如果是一个新表达式，从结果开始
            calculator_state['expression'] = calculator_state['result'] + operator
            calculator_state['isNewExpression'] = False
        else:
            calculator_state['expression'] += operator
        
        print(f"点击 {operator} 按钮后，表达式: {calculator_state['expression']}")
    
    # 测试场景1: 初始状态点击开方按钮
    print("场景1: 初始状态点击开方按钮")
    calculator_state = {'expression': '0', 'result': '0', 'isNewExpression': True}
    appendOperation('√')
    print(f"问题: 表达式变成了 '{calculator_state['expression']}'，应该是 '√'")
    print()
    
    # 测试场景2: 输入数字后点击开方按钮
    print("场景2: 输入9后点击开方按钮")
    calculator_state = {'expression': '9', 'result': '0', 'isNewExpression': False}
    appendOperation('√')
    print(f"表达式: {calculator_state['expression']}")
    print()

def test_frontend_modulo_behavior():
    """模拟前端取余按钮行为"""
    print("=" * 50)
    print("模拟前端取余按钮行为")
    print("=" * 50)
    
    # 测试取余运算在前端的表现
    test_cases = [
        ("10%3", "10%3"),
        ("15%4", "15%4"),
    ]
    
    for input_expr, expected_display in test_cases:
        print(f"输入: {input_expr}")
        print(f"期望显示: {expected_display}")
        print()

if __name__ == "__main__":
    test_sqrt_issue()
    test_modulo_issue()
    test_frontend_sqrt_behavior()
    test_frontend_modulo_behavior()