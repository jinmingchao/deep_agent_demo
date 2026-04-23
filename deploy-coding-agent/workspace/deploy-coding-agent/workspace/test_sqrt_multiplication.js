// 测试开方运算与乘法结合的问题
console.log("测试开方运算与乘法结合的问题");
console.log("=".repeat(50));

// 模拟计算器状态
let calculatorState = {
    expression: '0',
    result: '0',
    isNewExpression: true
};

// 模拟appendOperation函数（当前版本）
function appendOperationCurrent(operator) {
    // 特殊处理开方运算符：当表达式是"0"时，直接替换为"√"
    if (operator === '√' && calculatorState.expression === '0') {
        calculatorState.expression = '√';
        calculatorState.isNewExpression = false;
        return;
    }
    
    if (calculatorState.isNewExpression && operator !== '(' && operator !== ')') {
        // 如果是一个新表达式，从结果开始
        calculatorState.expression = calculatorState.result + operator;
        calculatorState.isNewExpression = false;
    } else {
        // 避免连续运算符（除了括号）
        const lastChar = calculatorState.expression.slice(-1);
        const lastTwoChars = calculatorState.expression.slice(-2);
        const operators = ['+', '-', '×', '÷', '%', '√'];
        const twoCharOperators = ['^2'];
        
        // 检查最后一个字符是否是运算符
        const isLastCharOperator = operators.includes(lastChar);
        // 检查最后两个字符是否是运算符（如^2）
        const isLastTwoCharsOperator = twoCharOperators.includes(lastTwoChars);
        
        if ((isLastCharOperator || isLastTwoCharsOperator) && 
            (operators.includes(operator) || twoCharOperators.includes(operator)) && 
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
}

// 模拟appendNumber函数
function appendNumber(number) {
    if (calculatorState.isNewExpression) {
        calculatorState.expression = number;
        calculatorState.isNewExpression = false;
    } else {
        if (calculatorState.expression === '0' && number !== '.') {
            calculatorState.expression = number;
        } else {
            calculatorState.expression += number;
        }
    }
}

// 测试用例：10*√25
console.log("测试用例: 10*√25");
console.log("期望表达式: 10×√25");
console.log();

// 重置状态
calculatorState.expression = '0';
calculatorState.isNewExpression = true;

console.log("步骤1: 输入10");
appendNumber('1');
appendNumber('0');
console.log(`  当前表达式: ${calculatorState.expression}`);

console.log("\n步骤2: 输入乘法运算符 ×");
appendOperationCurrent('×');
console.log(`  当前表达式: ${calculatorState.expression}`);

console.log("\n步骤3: 输入开方运算符 √");
appendOperationCurrent('√');
console.log(`  当前表达式: ${calculatorState.expression}`);
console.log(`  问题: *号消失了！应该是 10×√`);

console.log("\n步骤4: 输入25");
appendNumber('2');
appendNumber('5');
console.log(`  最终表达式: ${calculatorState.expression}`);
console.log(`  错误表达式: ${calculatorState.expression} (应该是 10×√25)`);

console.log("\n" + "=".repeat(50));
console.log("问题分析:");
console.log("当输入 10× 后点击 √ 按钮时:");
console.log("1. 最后一个字符是 '×'，它在 operators 数组中");
console.log("2. 当前操作符 '√' 也在 operators 数组中");
console.log("3. 因此执行替换逻辑: expression.slice(0, -1) + '√'");
console.log("4. 结果: '10×' 变成 '10√'，×号被替换了");
console.log("\n解决方案:");
console.log("开方运算符 √ 是一元运算符，应该可以跟在其他运算符后面");
console.log("需要修改逻辑，允许 √ 跟在其他运算符后面");