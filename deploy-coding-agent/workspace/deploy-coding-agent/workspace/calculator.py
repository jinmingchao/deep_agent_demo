#!/usr/bin/env python3
"""
Calculator Backend - supports +, -, *, /, %, ^ (power), sqrt
Accepts integer and decimal numbers.
Usage:
  python calculator.py <expression>
  python calculator.py "3 + 5 * 2"
  python calculator.py "sqrt(16)"
  python calculator.py "10 % 3"
"""

import sys
import math
import re


def calculate(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    expr = expression.strip()

    # Handle sqrt specially: sqrt(x)
    sqrt_pattern = r"sqrt\(([^)]+)\)"
    while re.search(sqrt_pattern, expr):
        match = re.search(sqrt_pattern, expr)
        inner = match.group(1)
        try:
            val = float(inner)
            if val < 0:
                return "Error: sqrt of negative number"
            result = math.sqrt(val)
            # Remove decimal if whole number
            result_str = str(int(result)) if result == int(result) else str(result)
            expr = expr[:match.start()] + result_str + expr[match.end():]
        except ValueError:
            return f"Error: invalid sqrt argument '{inner}'"

    # Replace ^ with ** for power
    expr = expr.replace("^", "**")

    # Validate characters: only digits, operators, spaces, decimal points, parentheses
    allowed = re.compile(r"^[\d\s+\-*/().%]+$")
    if not allowed.match(expr):
        return "Error: invalid characters in expression"

    try:
        # Use Python's eval with limited scope for safety
        result = eval(expr, {"__builtins__": {}}, {"abs": abs, "round": round})
        if isinstance(result, float):
            # If it's a whole number, return as int
            if result == int(result):
                return str(int(result))
            # Round to avoid floating point artifacts
            return str(round(result, 10))
        return str(result)
    except ZeroDivisionError:
        return "Error: division by zero"
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    if len(sys.argv) < 2:
        print("Usage: python calculator.py <expression>")
        print("Example: python calculator.py \"3 + 5 * 2\"")
        sys.exit(1)

    expression = " ".join(sys.argv[1:])
    result = calculate(expression)
    print(result)


if __name__ == "__main__":
    main()
