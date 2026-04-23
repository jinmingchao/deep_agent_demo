# 科学计算器

一个完整的科学计算器应用，包含前端HTML页面和后端Python API服务。

## 功能特性

- **基本运算**: 加(+)、减(-)、乘(×)、除(÷)
- **高级运算**: 取余(%)、平方(x²)、开方(√)
- **支持类型**: 整数和小数运算
- **表达式显示**: 实时显示输入表达式和计算结果
- **历史记录**: 保存最近10条计算记录
- **键盘支持**: 支持键盘输入
- **响应式设计**: 适配各种屏幕尺寸

## 项目结构

```
workspace/
├── index.html          # 前端HTML页面
├── styles.css          # 前端样式文件
├── app.js              # 前端JavaScript逻辑
├── server.py           # 后端Python Flask服务
├── requirements.txt    # Python依赖包
└── README.md           # 项目说明文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动后端服务

```bash
python server.py
```

后端服务将在 `http://localhost:5000` 启动。

### 3. 打开前端页面

直接在浏览器中打开 `index.html` 文件，或使用Python简单HTTP服务器：

```bash
# 在workspace目录下运行
python -m http.server 8000
```

然后在浏览器中访问 `http://localhost:8000`

## API接口

### 计算表达式
```
POST /calculate
Content-Type: application/json

{
    "expression": "1+2×3"
}
```

响应：
```json
{
    "expression": "1+2×3",
    "result": "7",
    "success": true
}
```

### 健康检查
```
GET /health
```

### 获取示例
```
GET /examples
```

## 使用说明

### 前端操作
1. 点击数字按钮输入数字
2. 点击运算符按钮进行运算
3. 特殊功能按钮：
   - **x²**: 平方运算
   - **√**: 开方运算
   - **%**: 取余运算
   - **C**: 清除所有
   - **CE**: 清除当前输入
   - **=**: 计算结果

### 键盘快捷键
- **数字 0-9**: 输入数字
- **+ - * /**: 基本运算
- **%**: 取余
- **.**: 小数点
- **( )**: 括号
- **Enter** 或 **=**: 计算
- **Escape**: 清除所有
- **Backspace**: 退格
- **^**: 平方
- **s**: 开方

## 技术栈

### 前端
- HTML5
- CSS3 (Flexbox, Grid, CSS Variables)
- JavaScript (ES6+)
- Font Awesome 图标
- Google Fonts 字体

### 后端
- Python 3
- Flask Web框架
- Flask-CORS 跨域支持
- Decimal 高精度计算

## 开发说明

### 后端计算逻辑
1. 表达式标准化（替换符号）
2. 分词处理
3. 中缀转后缀（逆波兰表示法）
4. 后缀表达式计算
5. 结果格式化

### 错误处理
- 除零错误
- 负数开方错误
- 表达式语法错误
- 网络连接错误

## 许可证

MIT License