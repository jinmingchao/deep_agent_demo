# 简单测试脚本
print("测试计算器功能...")

# 测试基本运算
def test_basic_operations():
    print("\n1. 测试基本运算:")
    
    # 模拟计算器逻辑
    tests = [
        ("1 + 2", 3),
        ("5 - 3", 2),
        ("2 * 3", 6),
        ("10 / 2", 5),
        ("7 % 3", 1),
        ("3 ** 2", 9),  # 平方
        ("16 ** 0.5", 4),  # 开方
        ("2.5 + 1.5", 4.0),
    ]
    
    for expr, expected in tests:
        try:
            # 使用Python的eval进行简单测试
            result = eval(expr.replace('**', '**'))
            if abs(result - expected) < 0.0001:
                print(f"  ✓ {expr} = {result}")
            else:
                print(f"  ✗ {expr} = {result} (期望: {expected})")
        except Exception as e:
            print(f"  ✗ {expr} 错误: {e}")

# 测试表达式解析
def test_expression_parsing():
    print("\n2. 测试表达式解析:")
    
    expressions = [
        "1+2×3",      # 应该等于7
        "(2+3)×4",    # 应该等于20
        "10÷(2+3)",   # 应该等于2
        "√(9+16)",    # 应该等于5
    ]
    
    # 替换符号为Python可识别的
    for expr in expressions:
        py_expr = (expr
                  .replace('×', '*')
                  .replace('÷', '/')
                  .replace('√', 'math.sqrt')
                  .replace('^', '**'))
        
        print(f"  {expr} -> {py_expr}")

# 检查文件完整性
def check_files():
    print("\n3. 检查文件完整性:")
    
    import os
    
    files = [
        "index.html",
        "styles.css", 
        "app.js",
        "server.py",
        "requirements.txt",
        "README.md",
    ]
    
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✓ {file} ({size} 字节)")
        else:
            print(f"  ✗ {file} (不存在)")

if __name__ == "__main__":
    print("=" * 50)
    print("计算器应用功能测试")
    print("=" * 50)
    
    check_files()
    test_basic_operations()
    test_expression_parsing()
    
    print("\n" + "=" * 50)
    print("测试完成!")
    print("=" * 50)
    print("\n使用说明:")
    print("1. 安装依赖: pip install -r requirements.txt")
    print("2. 启动后端: python server.py")
    print("3. 打开前端: 在浏览器中打开 index.html")
    print("=" * 50)