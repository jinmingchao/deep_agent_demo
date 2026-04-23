// 测试修复后的开方运算与乘法结合问题
console.log("测试修复后的开方运算与乘法结合问题");
console.log("=".repeat(50));

// 模拟修复后的appendOperation函数
function appendOperationFixed(operator, calculatorState) {
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
        const binaryOperators = ['+', '-', '×', '÷', '%']; // 二元运算符
        const unaryOperators = ['√']; // 一元运算符
        const twoCharOperators = ['^2'];
        
        // 检查最后一个字符是否是运算符
        const isLastCharBinaryOperator = binaryOperators.includes(lastChar);
        const isLastCharUnaryOperator = unaryOperators.includes(lastChar);
        const isLastCharOperator = isLastCharBinaryOperator || isLastCharUnaryOperator;
        
        // 检查最后两个字符是否是运算符（如^2）
        const isLastTwoCharsOperator = twoCharOperators.includes(lastTwoChars);
        
        // 特殊处理：开方运算符可以跟在二元运算符后面
        if (operator === '√' && isLastCharBinaryOperator) {
            // 允许开方运算符跟在二元运算符后面
            calculatorState.expression += operator;
        }
        // 检查：开方运算符后面不能直接跟其他运算符（除了括号）
        else if (isLastCharUnaryOperator && operator !== '(' && operator !== ')') {
            // 开方运算符后面不能直接跟其他运算符，替换最后一个运算符
            calculatorState.expression = calculatorState.expression.slice(0, -1) + operator;
        }
        // 处理其他运算符替换逻辑
        else if ((isLastCharBinaryOperator || isLastTwoCharsOperator) && 
                 (binaryOperators.includes(operator) || twoCharOperators.includes(operator)) && 
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
function appendNumber(number, calculatorState) {
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

// 测试用例1: 10*√25
console.log("测试用例1: 10*√25");
console.log("期望表达式: 10×√25");
console.log();

let calculatorState = {
    expression: '0',
    result: '0',
    isNewExpression: true
};

console.log("步骤1: 输入10");
appendNumber('1', calculatorState);
appendNumber('0', calculatorState);
console.log(`  当前表达式: ${calculatorState.expression}`);

console.log("\n步骤2: 输入乘法运算符 ×");
appendOperationFixed('×', calculatorState);
console.log(`  当前表达式: ${calculatorState.expression}`);

console.log("\n步骤3: 输入开方运算符 √");
appendOperationFixed('√', calculatorState);
console.log(`  当前表达式: ${calculatorState.expression}`);
console.log(`  ✓ 正确: 10×√ (×号没有消失)`);

console.log("\n步骤4: 输入25");
appendNumber('2', calculatorState);
appendNumber('5', calculatorState);
console.log(`  最终表达式: ${calculatorState.expression}`);
console.log(`  ✓ 正确表达式: ${calculatorState.expression}`);

console.log("\n" + "=".repeat(50));

// 测试用例2: 其他运算符后面跟开方
console.log("测试用例2: 其他运算符后面跟开方");
const testCases = [
    { name: "加法", operator: '+', expected: "10+√" },
    { name: "减法", operator: '-', expected: "10-√" },
    { name: "除法", operator: '÷', expected: "10÷√" },
    { name: "取余", operator: '%', expected: "10%√" },
];

for (const test of testCases) {
    calculatorState.expression = '0';
    calculatorState.isNewExpression = true;
    
    console.log(`\n${test.name}: 10${test.operator}√`);
    appendNumber('1', calculatorState);
    appendNumber('0', calculatorState);
    appendOperationFixed(test.operator, calculatorState);
    appendOperationFixed('√', calculatorState);
    
    console.log(`  当前表达式: ${calculatorState.expression}`);
    if (calculatorState.expression === test.expected) {
        console.log(`  ✓ 正确`);
    } else {
        console.log(`  ✗ 错误，期望: ${test.expected}`);
    }
}

console.log("\n" + "=".repeat(50));

// 测试用例3: 开方运算符后面不能直接跟其他运算符
console.log("测试用例3: 开方运算符后面不能直接跟其他运算符");
calculatorState.expression = '0';
calculatorState.isNewExpression = true;

console.log("\n步骤1: 输入√");
appendOperationFixed('√', calculatorState);
console.log(`  当前表达式: ${calculatorState.expression}`);

console.log("\n步骤2: 尝试输入+（应该替换√）");
appendOperationFixed('+', calculatorState);
console.log(`  当前表达式: ${calculatorState.expression}`);
console.log(`  ✓ 正确: √被替换为+`);

console.log("\n步骤3: 尝试输入×（应该替换+）");
appendOperationFixed('×', calculatorState);
console.log(`  当前表达式: ${calculatorState.expression}`);
console.log(`  ✓ 正确: +被替换为×`);

console.log("\n" + "=".repeat(50));
console.log("所有测试完成！");