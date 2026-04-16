"""
最小化MLP测试
直接在代码中定义和测试MLP
"""

import torch
import torch.nn as nn
import torch.optim as optim

print("=" * 60)
print("PyTorch MLP 最小测试")
print("=" * 60)

# 设置随机种子
torch.manual_seed(42)

# 1. 定义简单的MLP
class SimpleMLP(nn.Module):
    def __init__(self, input_dim, hidden_dims, output_dim):
        super().__init__()
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.ReLU())
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, output_dim))
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)

# 2. 创建测试数据
batch_size = 8
input_dim = 5
hidden_dims = [10, 8, 6]
output_dim = 2

X = torch.randn(batch_size, input_dim)
y = torch.randn(batch_size, output_dim)

print(f"测试数据:")
print(f"  X形状: {X.shape}")
print(f"  y形状: {y.shape}")

# 3. 创建和测试模型
model = SimpleMLP(input_dim, hidden_dims, output_dim)

print(f"\nMLP模型:")
print(f"  输入维度: {input_dim}")
print(f"  隐藏层: {hidden_dims}")
print(f"  输出维度: {output_dim}")

# 测试前向传播
model.eval()
with torch.no_grad():
    output = model(X)

print(f"\n前向传播测试:")
print(f"  输出形状: {output.shape}")
assert output.shape == (batch_size, output_dim)
print("  ✓ 形状正确")

# 4. 测试训练
model.train()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

print(f"\n训练测试:")
for epoch in range(3):
    optimizer.zero_grad()
    pred = model(X)
    loss = criterion(pred, y)
    loss.backward()
    optimizer.step()
    print(f"  Epoch {epoch}: loss = {loss.item():.6f}")

print("  ✓ 训练完成")

# 5. 测试不同配置
print(f"\n不同配置测试:")
configs = [
    ([4], "小型网络"),
    ([16, 8], "中型网络"),
    ([32, 16, 8, 4], "大型网络"),
]

for hidden_dims, desc in configs:
    test_model = SimpleMLP(input_dim, hidden_dims, output_dim)
    params = sum(p.numel() for p in test_model.parameters())
    
    with torch.no_grad():
        test_output = test_model(X)
    
    print(f"  {desc}: 隐藏层={hidden_dims}, 参数={params}, 输出形状={test_output.shape}")

print("\n" + "=" * 60)
print("MLP实现测试完成！")
print("=" * 60)

# 6. 生成示例代码
print("\n示例使用代码:")
example = '''
# 创建MLP
model = SimpleMLP(
    input_dim=10,           # 输入特征数
    hidden_dims=[64, 32],   # 两个隐藏层
    output_dim=1            # 输出维度
)

# 训练MLP
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(100):
    optimizer.zero_grad()
    predictions = model(X_train)
    loss = criterion(predictions, y_train)
    loss.backward()
    optimizer.step()
'''

print(example)