from __future__ import annotations

from langchain_core.tools import tool


@tool
def add_numbers(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    s = a + b
    print(f"[tool add_numbers] a={a} b={b} sum={s}")
    return s

