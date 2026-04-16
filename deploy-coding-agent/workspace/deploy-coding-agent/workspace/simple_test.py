import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# 简单的测试脚本，不依赖外部模块
print("=" * 60)
print("PyTorch MLP 简单测试")
print("=" * 60)

# 设置随机种子
torch.manual_seed(42)
np.random.seed(42)

# 1. 测试基本MLP类
print("\n1. 测试基本MLP类")

class SimpleMLP(nn.Module):
    """简单的MLP实现"""
    def __init__(self, input_dim, hidden_dims, output_dim, activation='relu'):
        super().__init__()
        
        layers = []
        prev_dim = input_dim
        
        # 构建隐藏层
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.ReLU() if activation == 'relu' else nn.Tanh())
            prev_dim = hidden_dim
        
        # 输出层
        layers.append(nn.Linear(prev_dim, output_dim))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)

# 创建测试数据
batch_size = 8
input_dim = 10
hidden_dims = [64, 32, 16]
output_dim = 3

X = torch.randn(batch_size, input_dim)
y = torch.randn(batch_size, output_dim)

# 创建模型
model = SimpleMLP(input_dim, hidden_dims, output_dim, activation='relu')

print(f"输入形状: {X.shape}")
print(f"目标形状: {y.shape}")
print(f"模型架构: {model}")

# 测试前向传播
model.eval()
with torch.no_grad():
    output = model(X)

print(f"输出形状: {output.shape}")
assert output.shape == (batch_size, output_dim), f"输出形状错误: {output.shape}"
print("✓ 前向传播测试通过")

# 2. 测试训练循环
print("\n2. 测试训练循环")

model.train()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练一个epoch
for epoch in range(5):
    optimizer.zero_grad()
    predictions = model(X)
    loss = criterion(predictions, y)
    loss.backward()
    optimizer.step()
    
    if epoch % 2 == 0:
        print(f"  Epoch {epoch}: loss = {loss.item():.6f}")

print("✓ 训练循环测试通过")

# 3. 测试不同配置
print("\n3. 测试不同网络配置")

configs = [
    {"hidden_dims": [32], "activation": "relu"},
    {"hidden_dims": [64, 32], "activation": "relu"},
    {"hidden_dims": [128, 64, 32], "activation": "tanh"},
]

for i, config in enumerate(configs, 1):
    test_model = SimpleMLP(
        input_dim=input_dim,
        hidden_dims=config["hidden_dims"],
        output_dim=output_dim,
        activation=config["activation"]
    )
    
    with torch.no_grad():
        test_output = test_model(X)
    
    num_params = sum(p.numel() for p in test_model.parameters())
    print(f"  配置{i}: 隐藏层={config['hidden_dims']}, "
          f"激活函数={config['activation']}, "
          f"参数数量={num_params:,}, "
          f"输出形状={test_output.shape}")

print("✓ 配置测试通过")

# 4. 测试分类任务
print("\n4. 测试分类任务")

# 生成分类数据
num_classes = 4
y_class = torch.randint(0, num_classes, (batch_size,))

class ClassifierMLP(nn.Module):
    """分类MLP"""
    def __init__(self, input_dim, hidden_dims, num_classes):
        super().__init__()
        
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.ReLU())
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, num_classes))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)

classifier = ClassifierMLP(input_dim, [32, 16], num_classes)
criterion_cls = nn.CrossEntropyLoss()
optimizer_cls = optim.Adam(classifier.parameters(), lr=0.001)

# 训练分类器
classifier.train()
for epoch in range(3):
    optimizer_cls.zero_grad()
    logits = classifier(X)
    loss = criterion_cls(logits, y_class)
    loss.backward()
    optimizer_cls.step()

print(f"分类损失: {loss.item():.6f}")

# 测试预测
classifier.eval()
with torch.no_grad():
    logits = classifier(X)
    predictions = torch.argmax(logits, dim=1)
    accuracy = (predictions == y_class).float().mean()

print(f"准确率: {accuracy.item():.2%}")
print("✓ 分类任务测试通过")

print("\n" + "=" * 60)
print("所有测试完成！✓")
print("=" * 60)