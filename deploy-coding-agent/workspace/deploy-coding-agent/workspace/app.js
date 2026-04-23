// 计算器状态
let calculatorState = {
    expression: '0',
    result: '0',
    history: [],
    isNewExpression: true,
    backendUrl: 'http://localhost:5000/calculate'
};

// DOM元素
const expressionElement = document.getElementById('expression');
const resultElement = document.getElementById('result');
const historyElement = document.getElementById('history');
const connectionStatusElement = document.getElementById('connectionStatus');
const inputModeElement = document.getElementById('inputMode');

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    updateDisplay();
    checkBackendConnection();
    
    // 添加键盘支持
    document.addEventListener('keydown', handleKeyboardInput);
});

// 检查后端连接
async function checkBackendConnection() {
    try {
        const response = await fetch(calculatorState.backendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ expression: '1+1' })
        });
        
        if (response.ok) {
            connectionStatusElement.textContent = '已连接';
            connectionStatusElement.style.color = '#28a745';
        } else {
            connectionStatusElement.textContent = '连接失败';
            connectionStatusElement.style.color = '#dc3545';
        }
    } catch (error) {
        connectionStatusElement.textContent = '未连接';
        connectionStatusElement.style.color = '#dc3545';
        console.warn('后端服务未启动，请运行 python server.py');
    }
}

// 处理键盘输入
function handleKeyboardInput(event) {
    const key = event.key;
    
    // 阻止默认行为，避免页面滚动等
    if (/[\d+\-*/.=()%]|Enter|Backspace|Escape/.test(key)) {
        event.preventDefault();
    }
    
    if (key >= '0' && key <= '9') {
        appendNumber(key);
    } else if (key === '.') {
        appendNumber('.');
    } else if (key === '+') {
        appendOperation('+');
    } else if (key === '-') {
        appendOperation('-');
    } else if (key === '*') {
        appendOperation('×');
    } else if (key === '/') {
        appendOperation('÷');
    } else if (key === '%') {
        appendOperation('%');
    } else if (key === '(') {
        appendOperation('(');
    } else if (key === ')') {
        appendOperation(')');
    } else if (key === 'Enter' || key === '=') {
        calculate();
    } else if (key === 'Escape') {
        clearAll();
    } else if (key === 'Backspace') {
        backspace();
    } else if (key === '^') {
        appendOperation('^2');
    } else if (key === 's' || key === 'S') {
        appendOperation('√');
    }
}

// 添加数字
function appendNumber(number) {
    if (calculatorState.isNewExpression) {
        calculatorState.expression = number;
        calculatorState.isNewExpression = false;
    } else {
        // 避免多个小数点
        if (number === '.' && calculatorState.expression.includes('.')) {
            const lastNumber = calculatorState.expression.split(/[\+\-\×\÷\(\)\%\^√]/).pop();
            if (lastNumber.includes('.')) {
                return;
            }
        }
        
        // 如果当前是0，替换它（除非是0.）
        if (calculatorState.expression === '0' && number !== '.') {
            calculatorState.expression = number;
        } else {
            calculatorState.expression += number;
        }
    }
    
    updateDisplay();
}

// 添加运算符
function appendOperation(operator) {
    // 特殊处理一元运算符：当表达式是单个数字时，用一元运算符替换它
    if ((operator === '√' || operator === '^2') && /^\d+(\.\d+)?$/.test(calculatorState.expression)) {
        // 如果表达式是单个数字（如"3"或"3.14"），用一元运算符替换它
        calculatorState.expression = operator;
        calculatorState.isNewExpression = false;
        updateDisplay();
        return;
    }
    
    if (calculatorState.isNewExpression && operator !== '(' && operator !== ')') {
        // 如果是一个新表达式，从结果开始
        // 但一元运算符（√和^2）应该开始新的表达式，而不是跟在结果后面
        if (operator === '√' || operator === '^2') {
            // 一元运算符开始新的表达式
            calculatorState.expression = operator;
            calculatorState.isNewExpression = false;
        } else {
            // 二元运算符从结果开始
            calculatorState.expression = calculatorState.result + operator;
            calculatorState.isNewExpression = false;
        }
    } else {
        // 避免连续运算符（除了括号）
        const lastChar = calculatorState.expression.slice(-1);
        const lastTwoChars = calculatorState.expression.slice(-2);
        const binaryOperators = ['+', '-', '×', '÷', '%']; // 二元运算符
        const unaryOperators = ['√']; // 一元运算符
        const twoCharUnaryOperators = ['^2']; // 两个字符的一元运算符
        
        // 检查最后一个字符是否是运算符
        const isLastCharBinaryOperator = binaryOperators.includes(lastChar);
        const isLastCharUnaryOperator = unaryOperators.includes(lastChar);
        const isLastCharOperator = isLastCharBinaryOperator || isLastCharUnaryOperator;
        
        // 检查最后两个字符是否是运算符（如^2）
        const isLastTwoCharsUnaryOperator = twoCharUnaryOperators.includes(lastTwoChars);
        
        // 特殊处理：一元运算符可以跟在二元运算符后面
        if ((operator === '√' || operator === '^2') && isLastCharBinaryOperator) {
            // 允许一元运算符（√和^2）跟在二元运算符后面
            calculatorState.expression += operator;
        }
        // 检查：一元运算符后面不能直接跟其他运算符（除了括号）
        else if ((isLastCharUnaryOperator || isLastTwoCharsUnaryOperator) && operator !== '(' && operator !== ')') {
            // 一元运算符后面不能直接跟其他运算符，替换最后一个运算符
            if (isLastTwoCharsUnaryOperator) {
                // 如果是两个字符的一元运算符（如^2），删除最后两个字符
                calculatorState.expression = calculatorState.expression.slice(0, -2) + operator;
            } else {
                // 如果是单个字符的一元运算符
                calculatorState.expression = calculatorState.expression.slice(0, -1) + operator;
            }
        }
        // 处理其他运算符替换逻辑
        else if ((isLastCharBinaryOperator || isLastTwoCharsUnaryOperator) && 
                 (binaryOperators.includes(operator) || twoCharUnaryOperators.includes(operator)) && 
                 operator !== '(' && operator !== ')') {
            // 替换最后一个运算符
            if (isLastTwoCharsOperator) {
                // 如果是两个字符的运算符（如^2），删除最后两个字符
                calculatorState.expression = calculatorState.expression.slice(0, -2) + operator;
            } else {
                // 如果是单个字符的运算符
                calculatorState.expression = calculatorState.expression.slice(0, -1) + operator;
            }
        } else {
            calculatorState.expression += operator;
        }
    }
    
    updateDisplay();
}

// 计算
async function calculate() {
    if (calculatorState.expression === '0' || calculatorState.expression === '') {
        return;
    }
    
    try {
        // 发送到后端计算
        const response = await fetch(calculatorState.backendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                expression: calculatorState.expression 
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.error) {
            calculatorState.result = '错误: ' + data.error;
        } else {
            calculatorState.result = data.result.toString();
            
            // 添加到历史记录
            const historyItem = {
                expression: calculatorState.expression,
                result: calculatorState.result,
                timestamp: new Date().toLocaleTimeString()
            };
            
            calculatorState.history.unshift(historyItem);
            
            // 保持最多10条历史记录
            if (calculatorState.history.length > 10) {
                calculatorState.history.pop();
            }
            
            // 准备下一个表达式
            calculatorState.isNewExpression = true;
        }
        
        updateDisplay();
        checkBackendConnection();
        
    } catch (error) {
        console.error('计算错误:', error);
        calculatorState.result = '错误: 无法连接到后端';
        updateDisplay();
    }
}

// 清除所有
function clearAll() {
    calculatorState.expression = '0';
    calculatorState.result = '0';
    calculatorState.isNewExpression = true;
    updateDisplay();
}

// 清除当前输入
function clearEntry() {
    calculatorState.expression = '0';
    calculatorState.isNewExpression = true;
    updateDisplay();
}

// 退格
function backspace() {
    if (calculatorState.expression.length > 1) {
        calculatorState.expression = calculatorState.expression.slice(0, -1);
    } else {
        calculatorState.expression = '0';
        calculatorState.isNewExpression = true;
    }
    updateDisplay();
}

// 更新显示
function updateDisplay() {
    // 更新表达式显示
    expressionElement.textContent = calculatorState.expression;
    
    // 更新结果显示
    resultElement.textContent = calculatorState.result;
    
    // 更新历史记录
    historyElement.innerHTML = '';
    calculatorState.history.forEach(item => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.innerHTML = `
            <span style="color: #6c757d">${item.timestamp}</span><br>
            <span style="color: #4361ee">${item.expression}</span> = 
            <span style="color: #7209b7; font-weight: bold">${item.result}</span>
        `;
        historyElement.appendChild(historyItem);
    });
    
    // 更新输入模式
    const hasAdvancedOps = calculatorState.expression.includes('^2') || 
                          calculatorState.expression.includes('√') || 
                          calculatorState.expression.includes('%');
    inputModeElement.textContent = hasAdvancedOps ? '科学' : '标准';
    inputModeElement.style.color = hasAdvancedOps ? '#7209b7' : '#4361ee';
}

// 导出函数供HTML调用
window.appendNumber = appendNumber;
window.appendOperation = appendOperation;
window.calculate = calculate;
window.clearAll = clearAll;
window.clearEntry = clearEntry;
window.backspace = backspace;