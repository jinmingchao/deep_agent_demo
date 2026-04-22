/**
 * Calculator Frontend - app.js
 * Sends expressions to the Python backend and displays results.
 */

const BACKEND_URL = 'http://localhost:5000/calculate';

// DOM references
const expressionEl = document.getElementById('expression');
const resultEl = document.getElementById('result');
const historyList = document.getElementById('historyList');
const buttons = document.querySelectorAll('.btn');

// State
let currentInput = '';
let history = [];

// ===== Core Functions =====

function updateDisplay() {
  expressionEl.textContent = currentInput || '0';
}

function updateResult(value) {
  resultEl.textContent = value;
}

function addToHistory(expression, result) {
  history.unshift({ expression, result });
  if (history.length > 20) history.pop();
  renderHistory();
}

function renderHistory() {
  historyList.innerHTML = '';
  if (history.length === 0) {
    historyList.innerHTML = '<div class="history-item" style="opacity:0.4;font-size:12px;">暂无记录</div>';
    return;
  }
  history.forEach(item => {
    const div = document.createElement('div');
    div.className = 'history-item';
    div.innerHTML = `
      <span class="h-expr">${escapeHtml(item.expression)}</span>
      <span class="h-result">= ${escapeHtml(item.result)}</span>
    `;
    historyList.appendChild(div);
  });
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// ===== Backend Communication =====

async function calculate(expression) {
  try {
    const response = await fetch(BACKEND_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ expression }),
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error || '计算错误');
    }

    const data = await response.json();
    return data.result;
  } catch (err) {
    if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
      throw new Error('无法连接到后端服务，请确保 Python 后端正在运行');
    }
    throw err;
  }
}

// ===== Input Handling =====

function appendToInput(value) {
  currentInput += value;
  updateDisplay();
}

function handleOperator(op) {
  // Don't start with an operator (except minus for negative numbers)
  if (currentInput === '' && op !== '-') return;
  // Replace trailing operator
  if (/[+\-*/%^]$/.test(currentInput)) {
    currentInput = currentInput.slice(0, -1);
  }
  currentInput += op;
  updateDisplay();
}

function handleSqrt() {
  // sqrt( expression )
  if (currentInput === '') {
    currentInput = 'sqrt(';
  } else if (/[\d)]$/.test(currentInput)) {
    // Multiply: 3 sqrt(4) -> 3*sqrt(4)
    currentInput += '*sqrt(';
  } else {
    currentInput += 'sqrt(';
  }
  updateDisplay();
}

function handleDecimal() {
  // Find the current number being typed
  const parts = currentInput.split(/[+\-*/%^()]/);
  const lastPart = parts[parts.length - 1];
  if (lastPart.includes('.')) return; // Already has decimal
  if (lastPart === '') {
    currentInput += '0.';
  } else {
    currentInput += '.';
  }
  updateDisplay();
}

function handleEquals() {
  if (currentInput === '') return;

  const expression = currentInput;

  // Auto-close parentheses
  let expr = expression;
  const openCount = (expr.match(/\(/g) || []).length;
  const closeCount = (expr.match(/\)/g) || []).length;
  if (openCount > closeCount) {
    expr += ')'.repeat(openCount - closeCount);
    currentInput = expr;
    updateDisplay();
  }

  calculate(expr)
    .then(result => {
      updateResult(result);
      addToHistory(expr, result);
    })
    .catch(err => {
      updateResult('错误');
      setTimeout(() => {
        if (currentInput === expr) updateResult('');
      }, 2000);
      console.error(err.message);
    });
}

function handleClear() {
  currentInput = '';
  updateDisplay();
  updateResult('');
}

function handleBackspace() {
  currentInput = currentInput.slice(0, -1);
  updateDisplay();
}

// ===== Keyboard Support =====

document.addEventListener('keydown', (e) => {
  const key = e.key;

  if (/^[\d]$/.test(key)) {
    appendToInput(key);
  } else if (key === '.') {
    handleDecimal();
  } else if (['+', '-', '*', '/', '%'].includes(key)) {
    handleOperator(key);
  } else if (key === '^') {
    handleOperator('^');
  } else if (key === 'Enter' || key === '=') {
    e.preventDefault();
    handleEquals();
  } else if (key === 'Backspace') {
    handleBackspace();
  } else if (key === 'Escape' || key === 'c' || key === 'C') {
    handleClear();
  } else if (key === '(' || key === ')') {
    appendToInput(key);
  }
});

// ===== Button Event Binding =====

buttons.forEach(btn => {
  btn.addEventListener('click', () => {
    const action = btn.dataset.action;
    const value = btn.dataset.value;

    if (action === 'number') {
      appendToInput(value);
    } else if (action === 'operator') {
      handleOperator(value);
    } else if (action === 'decimal') {
      handleDecimal();
    } else if (action === 'sqrt') {
      handleSqrt();
    } else if (action === 'equals') {
      handleEquals();
    } else if (action === 'clear') {
      handleClear();
    } else if (action === 'backspace') {
      handleBackspace();
    }
  });
});

// ===== Init =====
updateDisplay();
updateResult('');
renderHistory();
