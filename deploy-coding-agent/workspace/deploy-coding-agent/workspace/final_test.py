#!/usr/bin/env python3
"""
最终测试计算器修复
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import Calculator

def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("计算器乘除法修复测试")
    print("=" * 60)
    
    calculator = Calculator()
    
    test_cases = [
        # 基本乘除法
        ("2×3", "6", "乘法"),
        ("10÷2", "5", "除法"),
        ("2*3", "6", "乘法（*符号）"),
        ("10/2", "5", "除法（/符号）"),
        
        # 小数乘除法
        ("2.5×4", "10", "小数乘法"),
        ("10÷3", "3.3333333333", "小数除法"),
        
        # 优先级测试
        ("1+2×3", "7", "乘除优先于加减"),
        ("2×3+1", "7", "乘除优先于加减（反向）"),
        ("10÷2+3", "8", "除法优先于加法"),
        
        # 括号测试
        ("(2+3)×4", "20", "括号乘法"),
        ("12÷(2+2)", "3", "括号除法"),
        
        # 零处理
        ("0×5", "0", "乘以零"),
        ("5×0", "0", "零乘以"),
        
        # 错误情况
        ("5÷0", "错误", "除以零"),
        ("5/0", "错误", "除以零（/符号）"),
        
        # 混合运算
        ("2×3÷2", "3", "乘除混合"),
        ("1+2×3÷2", "4", "加减乘除混合"),
        
        # 其他运算符
        ("3^2", "9", "平方"),
        ("√16", "4", "开方"),
        ("√(9+16)", "5", "括号开方"),
        ("10%3", "1", "取余"),
    ]
    
    passed = 0
    failed = 0
    
    for expression, expected, description in test_cases:
        print(f"\n测试: {description}")
        print(f"  表达式: {expression}")
        print(f"  期望: {expected}")
        
        try:
            result = calculator.calculate(expression)
            print(f"  结果: {result}")
            
            if expected == "错误":
                print(f"  ✗ 应该报错但没有")
                failed += 1
            elif result == expected or abs(float(result) - float(expected)) < 0.0001:
                print(f"  ✓ 通过")
                passed += 1
            else:
                print(f"  ✗ 失败")
                failed += 1
                
        except ValueError as e:
            print(f"  错误: {e}")
            if expected == "错误":
                print(f"  ✓ 正确报错")
                passed += 1
            else:
                print(f"  ✗ 不应该报错")
                failed += 1
        except Exception as e:
            print(f"  未知错误: {e}")
            print(f"  ✗ 失败")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    if failed == 0:
        print("\n✅ 所有测试通过！乘除法问题已修复。")
    else:
        print(f"\n❌ 有 {failed} 个测试失败，需要进一步调试。")
    
    return failed == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)