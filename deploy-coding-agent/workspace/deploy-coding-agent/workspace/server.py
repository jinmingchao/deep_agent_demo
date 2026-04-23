#!/usr/bin/env python3
"""
科学计算器后端服务
支持加减乘除、取余、平方、开方运算
支持整数和小数运算
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import re
import logging
from decimal import Decimal, getcontext

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 设置Decimal精度
getcontext().prec = 28

class Calculator:
    """计算器核心类"""
    
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
        logger.info(f"标准化表达式输入: {expression}")
        
        # 替换前端使用的符号为Python可识别的符号
        expression = expression.replace('×', '*').replace('÷', '/')
        logger.info(f"替换符号后: {expression}")
        
        # 处理平方运算 x² -> x^2
        if '^2' in expression:
            # 使用正则表达式模块
            import re as regex_module
            expression = regex_module.sub(r'(\d+(?:\.\d+)?)\^2', r'(\1)^2', expression)
            logger.info(f"处理^2后: {expression}")
        
        # 处理开方运算 √x -> sqrt(x)
        # 简单处理：√数字 -> sqrt(数字)
        if '√' in expression:
            # 先处理 √( 的情况
            expression = expression.replace('√(', 'sqrt(')
            logger.info(f"处理√(后: {expression}")
            
            # 处理 √数字 的情况
            # 使用正则表达式替换所有 √数字
            import re as regex_module
            original = expression
            expression = regex_module.sub(r'√(\d+(?:\.\d+)?)', r'sqrt(\1)', expression)
            logger.info(f"处理√数字后: {expression}")
            
            # 检查是否还有未处理的 √
            if '√' in expression:
                logger.error(f"还有未处理的 √: {expression}")
                raise ValueError("开方运算符 √ 必须后跟数字或括号表达式")
        
        # 确保负号正确处理
        if '--' in expression:
            expression = expression.replace('--', '+')
            logger.info(f"处理--后: {expression}")
        
        logger.info(f"标准化表达式输出: {expression}")
        return expression
    
    def tokenize(self, expression):
        """将表达式转换为标记列表"""
        logger.info(f"开始分词: {expression}")
        tokens = []
        number = ''
        
        i = 0
        while i < len(expression):
            char = expression[i]
            logger.debug(f"处理字符 {i}: '{char}'")
            
            if char.isdigit() or char == '.':
                number += char
            else:
                if number:
                    tokens.append(number)
                    logger.debug(f"  添加数字: {number}")
                    number = ''
                
                if char in '+-*/%^()':
                    tokens.append(char)
                    logger.debug(f"  添加运算符: {char}")
                elif char == 's' and i + 3 < len(expression) and expression[i:i+4] == 'sqrt':
                    tokens.append('sqrt')
                    logger.debug(f"  添加函数: sqrt")
                    i += 3  # 跳过'sqrt'的剩余字符
                elif not char.isspace():
                    # 忽略其他字符或抛出错误
                    # 但如果是字母，可能是未知函数
                    if char.isalpha():
                        logger.error(f"未知字符: {char}")
                        raise ValueError(f"未知函数或操作符: {char}")
                    logger.debug(f"  忽略字符: {char}")
                    pass
            
            i += 1
        
        if number:
            tokens.append(number)
            logger.debug(f"  添加最后数字: {number}")
        
        logger.info(f"分词结果: {tokens}")
        return tokens
    
    def infix_to_postfix(self, tokens):
        """中缀表达式转后缀表达式（逆波兰表示法）"""
        output = []
        stack = []
        
        logger.info(f"开始转换后缀表达式，标记: {tokens}")
        
        for i, token in enumerate(tokens):
            logger.info(f"处理标记 {i}: {token}, 输出: {output}, 栈: {stack}")
            
            if self.is_number(token):
                output.append(token)
            elif token == 'sqrt':
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise ValueError("括号不匹配: 缺少左括号")
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
        
        logger.info(f"后缀表达式结果: {output}")
        return output
    
    def evaluate_postfix(self, postfix):
        """计算后缀表达式"""
        stack = []
        
        logger.info(f"开始计算后缀表达式: {postfix}")
        
        for i, token in enumerate(postfix):
            logger.info(f"计算标记 {i}: {token}, 栈: {stack}")
            
            if self.is_number(token):
                stack.append(Decimal(token))
            elif token == 'sqrt':
                if not stack:
                    raise ValueError("sqrt函数缺少参数")
                x = stack.pop()
                logger.info(f"  sqrt参数: {x}, 类型: {type(x)}")
                
                # 确保x是Decimal类型
                x = self.ensure_decimal(x)
                
                if x < 0:
                    raise ValueError("不能对负数开方")
                
                try:
                    # Decimal类型有sqrt方法
                    result = x.sqrt()
                    logger.info(f"  sqrt结果: {result}, 类型: {type(result)}")
                except Exception as e:
                    logger.error(f"sqrt计算错误: x={x}, 错误={e}")
                    raise ValueError(f"开方计算失败: {e}")
                
                # 确保结果是Decimal类型
                result = self.ensure_decimal(result)
                stack.append(result)
            else:
                if len(stack) < 2:
                    raise ValueError(f"运算符 {token} 缺少操作数，栈: {stack}")
                
                # 检查运算符是否在字典中
                if token not in self.operators:
                    raise ValueError(f"未知运算符: {token}")
                
                y = stack.pop()
                x = stack.pop()
                logger.info(f"  运算符 {token}: {x} {token} {y}, x类型: {type(x)}, y类型: {type(y)}")
                
                # 确保操作数都是Decimal类型
                x = self.ensure_decimal(x)
                y = self.ensure_decimal(y)
                
                logger.info(f"  运算符 {token}: {x} {token} {y}")
                
                if (token == '/' or token == '÷') and y == 0:
                    raise ValueError("除数不能为零")
                elif token == '%' and y == 0:
                    raise ValueError("取余运算除数不能为零")
                
                try:
                    result = self.operators[token][1](x, y)
                    logger.info(f"  运算结果: {result}, 类型: {type(result)}")
                    # 确保结果是Decimal类型
                    result = self.ensure_decimal(result)
                    stack.append(result)
                except Exception as e:
                    logger.error(f"运算符 {token} 计算错误: x={x}, y={y}, 错误={e}")
                    raise ValueError(f"运算失败: {e}")
        
        logger.info(f"计算完成，最终栈: {stack}")
        
        if len(stack) != 1:
            raise ValueError(f"表达式不完整，栈大小: {len(stack)}, 栈: {stack}")
        
        return stack[0]
    
    def is_number(self, token):
        """检查是否为数字"""
        try:
            float(token)
            return True
        except ValueError:
            return False
    
    def ensure_decimal(self, value):
        """确保值是Decimal类型"""
        if isinstance(value, Decimal):
            return value
        try:
            return Decimal(str(value))
        except Exception as e:
            logger.error(f"无法将值转换为Decimal: {value}, 类型: {type(value)}, 错误: {e}")
            raise ValueError(f"无法转换为Decimal: {type(value)}")
    
    def get_precedence(self, operator):
        """获取运算符优先级"""
        if operator == 'sqrt':
            return 5
        return self.operators.get(operator, (0, None))[0]
    
    def calculate(self, expression):
        """计算表达式"""
        try:
            logger.info(f"开始计算表达式: {expression}")
            
            # 标准化表达式
            normalized = self.normalize_expression(expression)
            logger.info(f"标准化后的表达式: {normalized}")
            
            # 分词
            tokens = self.tokenize(normalized)
            logger.info(f"分词结果: {tokens}")
            
            if not tokens:
                raise ValueError("表达式为空或无法分词")
            
            # 转换为后缀表达式
            postfix = self.infix_to_postfix(tokens)
            logger.info(f"后缀表达式: {postfix}")
            
            # 计算
            logger.info(f"开始计算后缀表达式")
            result = self.evaluate_postfix(postfix)
            logger.info(f"计算结果: {result}")
            
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
            logger.error(f"计算错误: {e}")
            raise ValueError(str(e))
        except Exception as e:
            logger.error(f"未知错误: {e}")
            raise Exception(f"计算失败: {str(e)}")

# 创建计算器实例
calculator = Calculator()

@app.route('/')
def index():
    """主页"""
    return jsonify({
        'name': '科学计算器API',
        'version': '1.0.0',
        'endpoints': {
            '/calculate': 'POST - 计算表达式',
            '/health': 'GET - 健康检查'
        },
        'supported_operations': ['+', '-', '×', '÷', '%', '^2', '√']
    })

@app.route('/health')
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'service': 'calculator-api'
    })

@app.route('/calculate', methods=['POST'])
def calculate():
    """计算表达式"""
    try:
        data = request.get_json()
        
        if not data or 'expression' not in data:
            return jsonify({
                'error': '缺少表达式参数',
                'example': {'expression': '1+2×3'}
            }), 400
        
        expression = data['expression']
        
        if not expression or expression.strip() == '':
            return jsonify({
                'error': '表达式不能为空'
            }), 400
        
        logger.info(f"收到计算请求: {expression}")
        
        # 计算
        result = calculator.calculate(expression)
        
        logger.info(f"计算结果: {result}")
        
        return jsonify({
            'expression': expression,
            'result': result,
            'success': True
        })
        
    except ValueError as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 400
    except Exception as e:
        logger.error(f"服务器错误: {e}")
        return jsonify({
            'error': '服务器内部错误',
            'success': False
        }), 500

@app.route('/examples', methods=['GET'])
def get_examples():
    """获取示例表达式"""
    examples = [
        {'expression': '1+2×3', 'description': '基本运算'},
        {'expression': '10÷3', 'description': '除法运算'},
        {'expression': '15%4', 'description': '取余运算'},
        {'expression': '3^2', 'description': '平方运算'},
        {'expression': '√16', 'description': '开方运算'},
        {'expression': '(2+3)×4', 'description': '括号运算'},
        {'expression': '2.5+3.7', 'description': '小数运算'},
        {'expression': '√(9+16)', 'description': '复杂开方'},
    ]
    
    return jsonify({
        'examples': examples,
        'count': len(examples)
    })

if __name__ == '__main__':
    print("=" * 50)
    print("科学计算器后端服务")
    print("=" * 50)
    print("端点:")
    print("  GET  /           - API信息")
    print("  GET  /health     - 健康检查")
    print("  GET  /examples   - 示例表达式")
    print("  POST /calculate  - 计算表达式")
    print("=" * 50)
    print("支持的运算: +, -, ×, ÷, %, ^2, √")
    print("=" * 50)
    print("启动服务器...")
    
    app.run(host='0.0.0.0', port=5000, debug=True)