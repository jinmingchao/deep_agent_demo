// 测试场景：先算9/3得到3，然后输入×√9
console.log("测试场景：先算9/3得到3，然后输入×√9");
console.log("=" .repeat(50));

// 模拟计算器状态
let calculatorState = {
    expression: '9÷3',
    result: '3',
    history: [],
    isNewExpression: true
};

// 模拟DOM更新函数
function updateDisplay() {
    console.log(`表达式: ${calculatorState.expression}, isNewExpression: ${calculatorState.isNewExpression}`);
}

// 模拟appendOperation函数（简化版）
function appendOperation(operator) {
    console.log(`\n点击操作符: ${operator}`);
    
    // 特殊处理一元运算符：当表达式是单个数字时，用一元运算符替换它
    if ((operator === '√' || operator === '^2') && /^\d+(\.\d+)?$/.test(calculatorState.expression)) {
        console.log("  特殊处理：表达式是单个数字，用一元运算符替换");
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
            console.log("  一元运算符开始新的表达式");
            calculatorState.expression = operator;
            calculatorState.isNewExpression = false;
        } else {
            // 二元运算符从结果开始
            console.log(`  二元运算符从结果开始: ${calculatorState.result} + ${operator}`);
            calculatorState.expression = calculatorState.result + operator;
            calculatorState.isNewExpression = false;
        }
    } else {
        // 避免连续运算符（除了括号）
        const lastChar = calculatorState.expression.slice(-1);
        const lastTwoChars = calculatorState.expression.slice(-2);
        const binaryOperators = ['+', '-', '×', '÷', '%'];
        const unaryOperators = ['√'];
        const twoCharUnaryOperators = ['^2'];
        
        const isLastCharBinaryOperator = binaryOperators.includes(lastChar);
        const isLastCharUnaryOperator = unaryOperators.includes(lastChar);
        const isLastTwoCharsUnaryOperator = twoCharUnaryOperators.includes(lastTwoChars);
        
        // 特殊处理：一元运算符可以跟在二元运算符后面
        if ((operator === '√' || operator === '^2') && isLastCharBinaryOperator) {
            console.log("  一元运算符跟在二元运算符后面");
            calculatorState.expression += operator;
        }
        // 检查：一元运算符后面不能直接跟其他运算符（除了括号）
        else if ((isLastCharUnaryOperator || isLastTwoCharsUnaryOperator) && operator !== '(' && operator !== ')') {
            console.log("  一元运算符后面不能直接跟其他运算符，替换最后一个运算符");
            if (isLastTwoCharsUnaryOperator) {
                calculatorState.expression = calculatorState.expression.slice(0, -2) + operator;
            } else {
                calculatorState.expression = calculatorState.expression.slice(0, -1) + operator;
            }
        }
        // 处理其他运算符替换逻辑
        else if ((isLastCharBinaryOperator || isLastTwoCharsUnaryOperator) && 
                 (binaryOperators.includes(operator) || twoCharUnaryOperators.includes(operator)) && 
                 operator !== '(' && operator !== ')') {
            console.log("  替换最后一个运算符");
            if (isLastTwoCharsUnaryOperator) {
                calculatorState.expression = calculatorState.expression.slice(0, -2) + operator;
            } else {
                calculatorState.expression = calculatorState.expression.slice(0, -1) + operator;
            }
        } else {
            console.log("  添加操作符到表达式");
            calculatorState.expression += operator;
        }
    }
    
    updateDisplay();
}

// 模拟appendNumber函数
function appendNumber(number) {
    console.log(`\n输入数字: ${number}`);
    
    if (calculatorState.isNewExpression) {
        calculatorState.expression = number;
        calculatorState.isNewExpression = false;
    } else {
        calculatorState.expression += number;
    }
    
    updateDisplay();
}

// 模拟calculate函数
function calculate() {
    console.log(`\n计算表达式: ${calculatorState.expression}`);
    // 这里简化，实际应该调用后端
    console.log("  调用后端计算...");
    calculatorState.result = "9"; // 假设结果是9
    calculatorState.isNewExpression = true;
    console.log(`  结果: ${calculatorState.result}`);
}

// 测试场景1：正确的操作顺序
console.log("\n测试场景1：正确的操作顺序 (9/3 → × → √ → 9 → =)");
console.log("-".repeat(40));

// 初始状态：刚计算完9/3
calculatorState.expression = '9÷3';
calculatorState.result = '3';
calculatorState.isNewExpression = true;
updateDisplay();

// 点击×
appendOperation('×');

// 点击√
appendOperation('√');

// 输入9
appendNumber('9');

// 计算
calculate();

console.log("\n" + "=".repeat(50));
console.log("测试场景2：错误操作顺序 (9/3 → √ → 9 → =)");
console.log("-".repeat(40));

// 重置状态
calculatorState.expression = '9÷3';
calculatorState.result = '3';
calculatorState.isNewExpression = true;
updateDisplay();

// 直接点击√（错误操作）
appendOperation('√');

// 输入9
appendNumber('9');

// 计算
calculate();

console.log("\n" + "=".repeat(50));
console.log("测试场景3：表达式是单个数字时点击√");
console.log("-".repeat(40));

// 重置状态：表达式是单个数字3
calculatorState.expression = '3';
calculatorState.result = '3';
calculatorState.isNewExpression = false;
updateDisplay();

// 点击√
appendOperation('√');

// 输入9
appendNumber('9');

// 计算
calculate();