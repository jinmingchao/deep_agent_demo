#!/usr/bin/env python3
"""
Calculator Backend Server (Flask)
Provides a REST API for the calculator frontend.

Usage:
  python server.py

Then open http://localhost:5000 in your browser.
"""

import re
import math
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)


def safe_eval(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.
    Supports: +, -, *, /, %, ^ (power), sqrt(), decimal numbers, parentheses.
    """
    # Clean the expression
    expr = expression.strip()

    if not expr:
        raise ValueError("表达式不能为空")

    # Replace display operators with Python operators
    expr = expr.replace('×', '*').replace('÷', '/').replace('−', '-')

    # Replace ^ with ** for power
    expr = expr.replace('^', '**')

    # Allow only safe characters: digits, operators, parentheses, dots, spaces, sqrt
    allowed_pattern = r'^[\d+\-*/().%^ sqrt**e]+$'
    # More precise: check character by character
    safe_chars = set('0123456789+-*/().% sqrt**e')
    for ch in expr:
        if ch not in safe_chars and not ch.isspace():
            raise ValueError(f"不支持的字符: '{ch}'")

    # Handle sqrt function: sqrt(x) -> math.sqrt(x)
    expr = re.sub(r'sqrt\(', 'math.sqrt(', expr)

    # Build a restricted namespace for eval
    namespace = {
        'math': math,
        '__builtins__': {},
    }

    try:
        result = eval(expr, namespace)
        # Format result
        if isinstance(result, (int, float)):
            if result == float('inf') or result == float('-inf'):
                raise ValueError("结果超出范围")
            if isinstance(result, float):
                # Round to avoid floating point artifacts
                result = round(result, 10)
                # If it's a whole number, show as integer
                if result == int(result):
                    result = int(result)
            return str(result)
        else:
            raise ValueError("计算结果无效")
    except ZeroDivisionError:
        raise ValueError("除数不能为零")
    except (SyntaxError, NameError, TypeError) as e:
        raise ValueError(f"表达式错误: {str(e)}")
    except Exception as e:
        raise ValueError(f"计算错误: {str(e)}")


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)


@app.route('/calculate', methods=['POST'])
def calculate():
    """API endpoint for calculation."""
    data = request.get_json()
    if not data or 'expression' not in data:
        return jsonify({'error': '缺少 expression 参数'}), 400

    expression = data['expression']
    try:
        result = safe_eval(expression)
        return jsonify({'expression': expression, 'result': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    print("=" * 50)
    print("  计算器后端服务已启动")
    print("  请打开浏览器访问: http://localhost:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
