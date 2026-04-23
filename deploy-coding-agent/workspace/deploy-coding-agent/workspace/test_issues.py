#!/usr/bin/env python3
"""
测试计算器问题
"""

def test_sqrt_issue():
    """测试开方运算问题"""
    print("=== 测试开方运算问题 ===")
    
    # 模拟前端状态
    expression = "0"
    result = "0"
    isNewExpression = True
    
    print(f"初始状态: 表达式='{expression}', isNewExpression={isNewExpression}")
    
    # 模拟点击开方按钮 - 当前逻辑
    operator = '√'
    if isNewExpression and operator not in ['(', ')']:
        expression = result + operator
        isNewExpression = False
    else:
        expression += operator
    
    print(f"当前逻辑点击√按钮后: 表达式='{expression}'")
    print(f"问题: 应该是'√'而不是'{expression}'")
    
    # 重置状态
    expression = "0"
    isNewExpression = True
    
    # 正确的逻辑
    if expression == "0":
        expression = "√"
        isNewExpression = False
    else:
        expression += operator
    
    print(f"正确逻辑点击√按钮后: 表达式='{expression}'")
    print()

def test_modulo_issue():
    """测试取余运算问题"""
    print("=== 测试取余运算问题 ===")
    
    # 测试一些取余运算
    test_cases = [
        ("10%3", 1),
        ("15%4", 3),
        ("7%2", 1),
        ("10.5%3", 1.5),  # 10.5 % 3 = 1.5
        ("5%2.5", 0.0),   # 5 % 2.5 = 0.0
    ]
    
    for expr, expected in test_cases:
        print(f"测试: {expr}")
        print(f"期望结果: {expected}")
        
        try:
            result = eval(expr)
            print(f"Python计算结果: {result}")
            
            # 检查是否匹配
            if abs(result - expected) < 0.0001:
                print("✓ 结果正确")
            else:
                print(f"✗ 结果不正确，差值: {abs(result - expected)}")
        except Exception as e:
            print(f"✗ 计算错误: {e}")
        print()

def test_backend_logic():
    """测试后端逻辑"""
    print("=== 测试后端逻辑 ===")
    
    # 从server.py中提取关键逻辑
    import re
    
    def normalize_expression(expression):
        """标准化表达式"""
        expression = expression.replace('×', '*').replace('÷', '/')
        
        # 处理平方运算 x² -> x^2
        expression = re.sub(r'(\d+(?:\.\d+)?)\^2', r'(\1)^2', expression)
        
        # 处理开方运算 √x -> sqrt(x)
        expression = re.sub(r'√(\d+(?:\.\d+)?)', r'sqrt(\1)', expression)
        expression = expression.replace('√(', 'sqrt(')
        
        return expression
    
    # 测试表达式
    test_expressions = [
        "√9",
        "0√9",  # 问题表达式
        "10%3",
        "√(4+5)",
    ]
    
    for expr in test_expressions:
        print(f"原始表达式: {expr}")
        normalized = normalize_expression(expr)
        print(f"标准化后: {normalized}")
        
        # 尝试计算
        try:
            # 注意：需要导入math模块
            import math
            result = eval(normalized)
            print(f"计算结果: {result}")
        except Exception as e:
            print(f"计算错误: {e}")
        print()

if __name__ == "__main__":
    test_sqrt_issue()
    test_modulo_issue()
    test_backend_logic()