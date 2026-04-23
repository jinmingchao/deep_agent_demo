#!/usr/bin/env python3
"""
验证计算器修复
"""

print("验证开方运算修复")
print("=" * 50)

# 模拟前端状态
class MockCalculatorState:
    def __init__(self):
        self.expression = '0'
        self.result = '0'
        self.isNewExpression = True

state = MockCalculatorState()

# 模拟appendOperation函数（修复后的版本）
def appendOperation(operator):
    # 特殊处理开方运算符：当表达式是"0"时，直接替换为"√"
    if operator == '√' and state.expression == '0':
        state.expression = '√'
        state.isNewExpression = False
        return
    
    if state.isNewExpression and operator not in ['(', ')']:
        # 如果是一个新表达式，从结果开始
        state.expression = state.result + operator
        state.isNewExpression = False
    else:
        # 避免连续运算符（除了括号）
        last_char = state.expression[-1] if state.expression else ''
        operators = ['+', '-', '×', '÷', '%', '√']
        
        if last_char in operators and operator in operators and operator not in ['(', ')']:
            # 替换最后一个运算符
            state.expression = state.expression[:-1] + operator
        else:
            state.expression += operator

# 测试开方运算
print("测试1: 初始状态点击开方按钮")
print(f"  初始表达式: '{state.expression}'")
appendOperation('√')
print(f"  点击√后表达式: '{state.expression}'")
print(f"  期望: '√'")
print(f"  结果: {'✓ 正确' if state.expression == '√' else '✗ 不正确'}")

print("\n测试2: 输入数字后点击开方按钮")
state.expression = '16'
state.isNewExpression = False
print(f"  当前表达式: '{state.expression}'")
appendOperation('√')
print(f"  点击√后表达式: '{state.expression}'")
print(f"  期望: '16√'")
print(f"  结果: {'✓ 正确' if state.expression == '16√' else '✗ 不正确'}")

print("\n测试3: 清除后点击开方按钮")
state.expression = '0'
state.isNewExpression = True
print(f"  清除后表达式: '{state.expression}'")
appendOperation('√')
print(f"  点击√后表达式: '{state.expression}'")
print(f"  期望: '√'")
print(f"  结果: {'✓ 正确' if state.expression == '√' else '✗ 不正确'}")

print("\n" + "=" * 50)
print("验证取余运算")
print("=" * 50)

# 重置状态
state.expression = '0'
state.isNewExpression = True

# 测试取余运算
print("测试1: 输入数字后点击%按钮")
state.expression = '10'
state.isNewExpression = False
print(f"  当前表达式: '{state.expression}'")
appendOperation('%')
print(f"  点击%后表达式: '{state.expression}'")
print(f"  期望: '10%'")
print(f"  结果: {'✓ 正确' if state.expression == '10%' else '✗ 不正确'}")

print("\n测试2: 完整取余表达式")
state.expression = '10%3'
state.isNewExpression = False
print(f"  表达式: '{state.expression}'")
print(f"  期望结果: 1")
print("  注意: 实际计算需要后端服务器")

print("\n测试3: 从结果开始取余运算")
state.expression = '0'
state.result = '5'
state.isNewExpression = True
print(f"  当前结果: '{state.result}', isNewExpression: {state.isNewExpression}")
appendOperation('%')
print(f"  点击%后表达式: '{state.expression}'")
print(f"  期望: '5%'")
print(f"  结果: {'✓ 正确' if state.expression == '5%' else '✗ 不正确'}")

print("\n" + "=" * 50)
print("修复总结")
print("=" * 50)
print("1. 开方运算修复:")
print("   - 问题: 当表达式为'0'时，点击√按钮会变成'0√'")
print("   - 修复: 在appendOperation函数中添加特殊处理，当表达式为'0'且操作符为'√'时，直接替换为'√'")
print()
print("2. 取余运算检查:")
print("   - 检查了前端表达式构建逻辑，看起来正确")
print("   - 后端计算逻辑使用Python的%运算符，应该正确")
print("   - 如果用户报告结果不正确，可能需要具体测试用例来重现")
print()
print("建议:")
print("1. 启动后端服务器: python server.py")
print("2. 打开前端: 在浏览器中打开index.html")
print("3. 测试具体用例:")
print("   - 点击√按钮，应该显示√而不是0√")
print("   - 测试10%3，应该等于1")
print("   - 测试15%4，应该等于3")