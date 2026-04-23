#!/usr/bin/env python3
"""
测试乘除法修复
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import Calculator

def test_fixed_calculator():
    """测试修复后的计算器"""
    print("测试乘除法修复...")
    print("=" * 60)
    
    calculator = Calculator()
    
    test_cases = [
        ("2×3", "6", "乘法（使用×符号）"),
        ("10÷2", "5", "除法（使用÷符号）"),
        ("2*3", "6", "乘法（使用*符号）"),
        ("10/2", "5", "除法（使用/符号）"),
        ("2.5×4", "10", "小数乘法"),
        ("10÷3", "3.3333333333", "小数除法"),
        ("(2+3)×4", "20", "括号乘法"),
        ("12÷(2+2)", "3", "括号除法"),
        ("2×3×4", "24", "连续乘法"),
        ("24÷2÷3", "4", "连续除法"),
        ("5÷0", "无穷大", "除以零"),
        ("5%0", "无穷大", "取余零"),
    ]
    
    passed = 0
    failed = 0
    
    for expression, expected, description in test_cases:
        print(f"\n测试: {description}")
        print(f"表达式: {expression}")
        
        try:
            result = calculator.calculate(expression)
            print(f"结果: {result}")
            print(f"期望: {expected}")
            
            # 特殊处理无穷大
            if expected == "无穷大" and result == "无穷大":
                print("✓ 通过")
                passed += 1
            elif result == expected or abs(float(result) - float(expected)) < 0.0001:
                print("✓ 通过")
                passed += 1
            else:
                print("✗ 失败")
                failed += 1
                
        except Exception as e:
            print(f"错误: {e}")
            print("✗ 失败")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0

def test_expression_processing():
    """测试表达式处理流程"""
    print("\n测试表达式处理流程...")
    print("=" * 60)
    
    calculator = Calculator()
    
    # 测试标准化
    test_expressions = ["2×3", "10÷2", "3^2", "√16"]
    
    for expr in test_expressions:
        print(f"\n原始表达式: {expr}")
        normalized = calculator.normalize_expression(expr)
        print(f"标准化后: {normalized}")
        
        tokens = calculator.tokenize(normalized)
        print(f"分词结果: {tokens}")
        
        postfix = calculator.infix_to_postfix(tokens)
        print(f"后缀表达式: {postfix}")
        
        try:
            result = calculator.evaluate_postfix(postfix)
            print(f"计算结果: {result}")
        except Exception as e:
            print(f"计算错误: {e}")

if __name__ == '__main__':
    print("开始测试计算器修复...")
    
    # 测试修复后的计算器
    test_ok = test_fixed_calculator()
    
    # 测试表达式处理流程
    test_expression_processing()
    
    print("\n" + "=" * 60)
    print("测试完成!")
    
    if test_ok:
        print("✓ 所有测试通过!")
    else:
        print("✗ 有些测试失败，需要进一步调试")
    
    print("=" * 60)