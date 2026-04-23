#!/usr/bin/env python3
"""
调试计算器乘除法问题
"""

import sys
import os

# 手动导入计算器模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 复制计算器核心逻辑进行调试
import math
from decimal import Decimal, getcontext

getcontext().prec = 28

class DebugCalculator:
    """调试用计算器"""
    
    def __init__(self):
        self.operators = {
            '+': (1, lambda x, y: x + y),
            '-': (1, lambda x, y: x - y),
            '×': (2, lambda x, y: x * y),
            '÷': (2, lambda x, y: x / y if y != 0 else float('inf')),
            '%': (3, lambda x, y: x % y if y != 0 else float('inf')),
            '^': (4, lambda x, y: x ** y),
        }
    
    def normalize_expression(self, expression):
        """标准化表达式"""
        print(f"原始表达式: {expression}")
        
        # 替换前端使用的符号为Python可识别的符号
        expression = expression.replace('×', '*').replace('÷', '/')
        print(f"替换符号后: {expression}")
        
        # 处理平方运算 x² -> x^2
        import re
        expression = re.sub(r'(\d+(?:\.\d+)?)\^2', r'(\1)^2', expression)
        
        # 处理开方运算 √x -> sqrt(x)
        expression = re.sub(r'√(\d+(?:\.\d+)?)', r'sqrt(\1)', expression)
        expression = re.sub(r'√\(([^)]+)\)', r'sqrt(\1)', expression)
        
        # 确保负号正确处理
        expression = expression.replace('--', '+')
        
        print(f"标准化后: {expression}")
        return expression
    
    def tokenize(self, expression):
        """将表达式转换为标记列表"""
        print(f"\n分词表达式: {expression}")
        tokens = []
        number = ''
        
        i = 0
        while i < len(expression):
            char = expression[i]
            
            if char.isdigit() or char == '.':
                number += char
            else:
                if number:
                    tokens.append(number)
                    print(f"  数字: {number}")
                    number = ''
                
                if char in '+-*/%^()':
                    tokens.append(char)
                    print(f"  运算符: {char}")
                elif char == 's' and expression[i:i+4] == 'sqrt':
                    tokens.append('sqrt')
                    print(f"  函数: sqrt")
                    i += 3  # 跳过'sqrt'的剩余字符
                elif not char.isspace():
                    # 忽略其他字符或抛出错误
                    pass
            
            i += 1
        
        if number:
            tokens.append(number)
            print(f"  数字: {number}")
        
        print(f"分词结果: {tokens}")
        return tokens
    
    def is_number(self, token):
        """检查是否为数字"""
        try:
            float(token)
            return True
        except ValueError:
            return False
    
    def get_precedence(self, operator):
        """获取运算符优先级"""
        if operator == 'sqrt':
            return 5
        return self.operators.get(operator, (0, None))[0]
    
    def infix_to_postfix(self, tokens):
        """中缀表达式转后缀表达式"""
        print(f"\n中缀转后缀:")
        print(f"输入tokens: {tokens}")
        
        output = []
        stack = []
        
        for token in tokens:
            print(f"\n处理token: {token}")
            print(f"  stack: {stack}")
            print(f"  output: {output}")
            
            if self.is_number(token):
                output.append(token)
                print(f"  数字 -> output")
            elif token == 'sqrt':
                stack.append(token)
                print(f"  sqrt -> stack")
            elif token == '(':
                stack.append(token)
                print(f"  ( -> stack")
            elif token == ')':
                print(f"  ) 开始弹出直到(")
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # 弹出 '('
                print(f"  弹出 '('")
                
                # 处理函数调用
                if stack and stack[-1] == 'sqrt':
                    output.append(stack.pop())
                    print(f"  弹出 sqrt -> output")
            else:
                print(f"  运算符 {token}, 优先级: {self.get_precedence(token)}")
                while (stack and stack[-1] != '(' and 
                       self.get_precedence(token) <= self.get_precedence(stack[-1])):
                    output.append(stack.pop())
                    print(f"  弹出 {output[-1]} -> output")
                stack.append(token)
                print(f"  {token} -> stack")
        
        while stack:
            output.append(stack.pop())
            print(f"  最后弹出 {output[-1]} -> output")
        
        print(f"后缀表达式: {output}")
        return output
    
    def evaluate_postfix(self, postfix):
        """计算后缀表达式"""
        print(f"\n计算后缀表达式: {postfix}")
        stack = []
        
        for token in postfix:
            print(f"\n处理token: {token}")
            print(f"  stack: {stack}")
            
            if self.is_number(token):
                stack.append(Decimal(token))
                print(f"  数字 {token} -> stack")
            elif token == 'sqrt':
                if not stack:
                    raise ValueError("sqrt函数缺少参数")
                x = stack.pop()
                print(f"  sqrt({x})")
                if x < 0:
                    raise ValueError("不能对负数开方")
                result = math.sqrt(float(x))
                stack.append(Decimal(str(result)))
                print(f"  结果 {result} -> stack")
            else:
                if len(stack) < 2:
                    raise ValueError("运算符缺少操作数")
                y = stack.pop()
                x = stack.pop()
                print(f"  运算: {x} {token} {y}")
                
                if token == '/' and y == 0:
                    raise ValueError("除数不能为零")
                elif token == '%' and y == 0:
                    raise ValueError("取余运算除数不能为零")
                
                result = self.operators[token][1](x, y)
                print(f"  结果: {result}")
                stack.append(Decimal(str(result)))
        
        if len(stack) != 1:
            raise ValueError("表达式不完整")
        
        print(f"最终结果: {stack[0]}")
        return stack[0]
    
    def calculate(self, expression):
        """计算表达式"""
        print("=" * 50)
        print(f"计算表达式: {expression}")
        print("=" * 50)
        
        try:
            # 标准化表达式
            normalized = self.normalize_expression(expression)
            
            # 分词
            tokens = self.tokenize(normalized)
            
            # 转换为后缀表达式
            postfix = self.infix_to_postfix(tokens)
            
            # 计算
            result = self.evaluate_postfix(postfix)
            
            # 格式化结果
            if result == float('inf'):
                return "无穷大"
            elif result == float('-inf'):
                return "负无穷大"
            
            # 如果是整数，显示为整数格式
            if result == int(result):
                return str(int(result))
            else:
                # 保留最多10位小数
                result_str = format(float(result), '.10f').rstrip('0').rstrip('.')
                return result_str
                
        except ValueError as e:
            print(f"计算错误: {e}")
            raise ValueError(str(e))
        except Exception as e:
            print(f"未知错误: {e}")
            raise Exception(f"计算失败: {str(e)}")

def test_multiplication_division():
    """测试乘除法"""
    print("\n" + "=" * 60)
    print("测试乘除法运算")
    print("=" * 60)
    
    calculator = DebugCalculator()
    
    test_cases = [
        ("2×3", "6", "简单乘法"),
        ("10÷2", "5", "简单除法"),
        ("2.5×4", "10", "小数乘法"),
        ("10÷3", "3.3333333333", "小数除法"),
        ("0×5", "0", "零乘法"),
        ("(2+3)×4", "20", "括号乘法"),
        ("12÷(2+2)", "3", "括号除法"),
        ("2×3×4", "24", "连续乘法"),
        ("24÷2÷3", "4", "连续除法"),
    ]
    
    for expression, expected, description in test_cases:
        print(f"\n{'='*40}")
        print(f"测试: {description}")
        print(f"表达式: {expression}")
        print(f"期望结果: {expected}")
        print(f"{'='*40}")
        
        try:
            result = calculator.calculate(expression)
            print(f"\n实际结果: {result}")
            
            if result == expected or abs(float(result) - float(expected)) < 0.0001:
                print(f"✓ 测试通过")
            else:
                print(f"✗ 测试失败: 期望 {expected}, 实际 {result}")
                
        except Exception as e:
            print(f"\n错误: {e}")
            print(f"✗ 测试失败")

if __name__ == '__main__':
    test_multiplication_division()