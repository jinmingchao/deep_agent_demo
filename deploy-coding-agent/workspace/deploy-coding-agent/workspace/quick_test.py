# 快速测试计算器修复
import sys
import os

# 模拟server.py中的Calculator类
class Calculator:
    def __init__(self):
        self.operators = {
            '+': (1, lambda x, y: x + y),
            '-': (1, lambda x, y: x - y),
            '×': (2, lambda x, y: x * y),
            '÷': (2, lambda x, y: x / y if y != 0 else float('inf')),
            '*': (2, lambda x, y: x * y),  # 添加*作为乘法运算符
            '/': (2, lambda x, y: x / y if y != 0 else float('inf')),  # 添加/作为除法运算符
            '%': (3, lambda x, y: x % y if y != 0 else float('inf')),
            '^': (4, lambda x, y: x ** y),
        }
    
    def normalize_expression(self, expression):
        """标准化表达式"""
        import re
        # 替换前端使用的符号为Python可识别的符号
        expression = expression.replace('×', '*').replace('÷', '/')
        
        # 处理平方运算 x² -> x^2
        expression = re.sub(r'(\d+(?:\.\d+)?)\^2', r'(\1)^2', expression)
        
        # 处理开方运算 √x -> sqrt(x)
        expression = re.sub(r'√(\d+(?:\.\d+)?)', r'sqrt(\1)', expression)
        expression = re.sub(r'√\(([^)]+)\)', r'sqrt(\1)', expression)
        
        # 确保负号正确处理
        expression = expression.replace('--', '+')
        
        return expression
    
    def tokenize(self, expression):
        """将表达式转换为标记列表"""
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
                    number = ''
                
                if char in '+-*/%^()':
                    tokens.append(char)
                elif char == 's' and expression[i:i+4] == 'sqrt':
                    tokens.append('sqrt')
                    i += 3  # 跳过'sqrt'的剩余字符
                elif not char.isspace():
                    # 忽略其他字符或抛出错误
                    pass
            
            i += 1
        
        if number:
            tokens.append(number)
        
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
        """中缀表达式转后缀表达式（逆波兰表示法）"""
        output = []
        stack = []
        
        for token in tokens:
            if self.is_number(token):
                output.append(token)
            elif token == 'sqrt':
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # 弹出 '('
                
                # 处理函数调用
                if stack and stack[-1] == 'sqrt':
                    output.append(stack.pop())
            else:
                while (stack and stack[-1] != '(' and 
                       self.get_precedence(token) <= self.get_precedence(stack[-1])):
                    output.append(stack.pop())
                stack.append(token)
        
        while stack:
            output.append(stack.pop())
        
        return output
    
    def evaluate_postfix(self, postfix):
        """计算后缀表达式"""
        from decimal import Decimal
        import math
        
        stack = []
        
        for token in postfix:
            if self.is_number(token):
                stack.append(Decimal(token))
            elif token == 'sqrt':
                if not stack:
                    raise ValueError("sqrt函数缺少参数")
                x = stack.pop()
                if x < 0:
                    raise ValueError("不能对负数开方")
                stack.append(math.sqrt(float(x)))
            else:
                if len(stack) < 2:
                    raise ValueError("运算符缺少操作数")
                y = stack.pop()
                x = stack.pop()
                
                if (token == '/' or token == '÷') and y == 0:
                    raise ValueError("除数不能为零")
                elif token == '%' and y == 0:
                    raise ValueError("取余运算除数不能为零")
                
                result = self.operators[token][1](x, y)
                stack.append(Decimal(str(result)))
        
        if len(stack) != 1:
            raise ValueError("表达式不完整")
        
        return stack[0]
    
    def calculate(self, expression):
        """计算表达式"""
        try:
            # 标准化表达式
            normalized = self.normalize_expression(expression)
            print(f"标准化后的表达式: {normalized}")
            
            # 分词
            tokens = self.tokenize(normalized)
            print(f"分词结果: {tokens}")
            
            # 转换为后缀表达式
            postfix = self.infix_to_postfix(tokens)
            print(f"后缀表达式: {postfix}")
            
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
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"计算失败: {str(e)}")

# 测试
print("测试计算器乘除法修复")
print("=" * 50)

calc = Calculator()

test_cases = [
    ("2×3", "6"),
    ("10÷2", "5"),
    ("2*3", "6"),
    ("10/2", "5"),
    ("2.5×4", "10"),
    ("10÷3", "3.3333333333"),
    ("(2+3)×4", "20"),
]

for expr, expected in test_cases:
    print(f"\n测试表达式: {expr}")
    try:
        result = calc.calculate(expr)
        print(f"计算结果: {result}")
        print(f"期望结果: {expected}")
        
        if result == expected or abs(float(result) - float(expected)) < 0.0001:
            print("✓ 通过")
        else:
            print("✗ 失败")
    except Exception as e:
        print(f"错误: {e}")
        print("✗ 失败")

print("\n" + "=" * 50)
print("测试完成!")