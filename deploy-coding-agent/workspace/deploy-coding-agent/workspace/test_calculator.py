#!/usr/bin/env python3
"""
计算器功能测试脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import Calculator

def test_calculator():
    """测试计算器核心功能"""
    print("=" * 50)
    print("计算器功能测试")
    print("=" * 50)
    
    calculator = Calculator()
    
    test_cases = [
        # (表达式, 期望结果, 描述)
        ("1+2", "3", "简单加法"),
        ("5-3", "2", "简单减法"),
        ("2×3", "6", "乘法"),
        ("10÷2", "5", "除法"),
        ("7%3", "1", "取余"),
        ("3^2", "9", "平方"),
        ("√16", "4", "开方"),
        ("2.5+1.5", "4", "小数加法"),
        ("(2+3)×4", "20", "括号运算"),
        ("√(9+16)", "5", "复杂开方"),
        ("10÷3", "3.3333333333", "小数除法"),
    ]
    
    passed = 0
    failed = 0
    
    for expression, expected, description in test_cases:
        try:
            result = calculator.calculate(expression)
            if result == expected or abs(float(result) - float(expected)) < 0.0001:
                print(f"✓ {description}: {expression} = {result}")
                passed += 1
            else:
                print(f"✗ {description}: {expression}")
                print(f"  期望: {expected}, 实际: {result}")
                failed += 1
        except Exception as e:
            print(f"✗ {description}: {expression}")
            print(f"  错误: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0

def test_api_endpoints():
    """测试API端点（不启动服务器）"""
    print("\n" + "=" * 50)
    print("API端点测试")
    print("=" * 50)
    
    from flask import Flask
    from server import app
    
    # 创建测试客户端
    test_client = app.test_client()
    
    # 测试健康检查
    response = test_client.get('/health')
    print(f"GET /health: {response.status_code}")
    if response.status_code == 200:
        print("  ✓ 健康检查通过")
    else:
        print("  ✗ 健康检查失败")
    
    # 测试示例端点
    response = test_client.get('/examples')
    print(f"GET /examples: {response.status_code}")
    if response.status_code == 200:
        data = response.get_json()
        print(f"  ✓ 获取到 {data.get('count', 0)} 个示例")
    else:
        print("  ✗ 示例端点失败")
    
    # 测试计算端点
    test_data = [
        {"expression": "1+2×3", "expected": "7"},
        {"expression": "10÷2", "expected": "5"},
        {"expression": "√16", "expected": "4"},
    ]
    
    for data in test_data:
        response = test_client.post('/calculate', 
                                   json={"expression": data["expression"]},
                                   content_type='application/json')
        
        print(f"POST /calculate: {data['expression']}")
        if response.status_code == 200:
            result = response.get_json()
            if result.get('success') and result.get('result') == data['expected']:
                print(f"  ✓ 计算正确: {result['result']}")
            else:
                print(f"  ✗ 计算错误: {result}")
        else:
            print(f"  ✗ 请求失败: {response.status_code}")
    
    print("=" * 50)

if __name__ == '__main__':
    print("开始测试计算器应用...")
    
    # 测试核心计算功能
    core_ok = test_calculator()
    
    # 测试API端点
    test_api_endpoints()
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    
    if core_ok:
        print("✓ 核心计算功能测试通过")
    else:
        print("✗ 核心计算功能测试失败")
    
    print("\n要启动完整服务器，请运行:")
    print("  python server.py")
    print("\n要查看前端页面，请打开:")
    print("  index.html (在浏览器中直接打开)")
    print("=" * 50)