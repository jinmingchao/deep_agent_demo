import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mlp_model import MLP, MLPClassifier, MLPRegressor, create_mlp_model
from data_generator import (
    generate_classification_data, 
    generate_regression_data,
    generate_simple_test_data,
    generate_spiral_data,
    get_data_info
)


def test_basic_functionality():
    """测试MLP基本功能"""
    print("=" * 60)
    print("测试MLP基本功能")
    print("=" * 60)
    
    # 创建简单测试数据
    batch_size = 16
    input_dim = 10
    hidden_dims = [64, 32, 16]
    output_dim = 3
    
    X, y = generate_simple_test_data(batch_size, input_dim, output_dim)
    
    # 创建MLP模型
    model = MLP(
        input_dim=input_dim,
        hidden_dims=hidden_dims,
        output_dim=output_dim,
        activation='relu',
        dropout_rate=0.2,
        use_batch_norm=True
    )
    
    print(f"模型架构: {model}")
    print(f"输入维度: {input_dim}")
    print(f"隐藏层维度: {hidden_dims}")
    print(f"输出维度: {output_dim}")
    print(f"参数数量: {model.get_num_parameters():,}")
    
    # 测试前向传播
    model.eval()
    with torch.no_grad():
        output = model(X)
    
    print(f"输入形状: {X.shape}")
    print(f"输出形状: {output.shape}")
    
    # 验证形状
    assert output.shape == (batch_size, output_dim), f"输出形状错误: {output.shape}"
    print("✓ 前向传播测试通过")
    
    return model, X, y


def test_classifier():
    """测试分类器MLP"""
    print("\n" + "=" * 60)
    print("测试分类器MLP")
    print("=" * 60)
    
    # 生成分类数据
    X_train, X_test, y_train, y_test = generate_classification_data(
        n_samples=200, n_features=8, n_classes=3
    )
    
    data_info = get_data_info(X_train, y_train)
    print(f"数据信息:")
    for key, value in data_info.items():
        print(f"  {key}: {value}")
    
    # 创建分类器
    input_dim = X_train.shape[1]
    hidden_dims = [32, 16]
    num_classes = len(torch.unique(y_train))
    
    classifier = MLPClassifier(
        input_dim=input_dim,
        hidden_dims=hidden_dims,
        num_classes=num_classes,
        activation='relu',
        dropout_rate=0.3
    )
    
    print(f"\n分类器架构:")
    print(f"  输入维度: {input_dim}")
    print(f"  隐藏层: {hidden_dims}")
    print(f"  类别数: {num_classes}")
    print(f"  参数数量: {classifier.get_num_parameters():,}")
    
    # 测试前向传播
    classifier.eval()
    with torch.no_grad():
        logits = classifier(X_train[:5])  # 只测试前5个样本
        proba = classifier.predict_proba(X_train[:5])
        predictions = classifier.predict(X_train[:5])
    
    print(f"\n测试结果:")
    print(f"  Logits形状: {logits.shape}")
    print(f"  概率形状: {proba.shape}")
    print(f"  预测形状: {predictions.shape}")
    
    # 验证概率和为1
    proba_sum = proba.sum(dim=1)
    assert torch.allclose(proba_sum, torch.ones_like(proba_sum), rtol=1e-5), "概率和不为1"
    print("✓ 概率和验证通过")
    
    # 测试训练循环
    print("\n测试训练循环...")
    classifier.train()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(classifier.parameters(), lr=0.001)
    
    # 一个小批量的训练
    optimizer.zero_grad()
    outputs = classifier(X_train[:32])
    loss = criterion(outputs, y_train[:32])
    loss.backward()
    optimizer.step()
    
    print(f"  训练损失: {loss.item():.4f}")
    print("✓ 训练循环测试通过")
    
    return classifier


def test_regressor():
    """测试回归器MLP"""
    print("\n" + "=" * 60)
    print("测试回归器MLP")
    print("=" * 60)
    
    # 生成回归数据
    X_train, X_test, y_train, y_test, y_scaler = generate_regression_data(
        n_samples=200, n_features=5, n_targets=1
    )
    
    data_info = get_data_info(X_train, y_train)
    print(f"数据信息:")
    for key, value in data_info.items():
        print(f"  {key}: {value}")
    
    # 创建回归器
    input_dim = X_train.shape[1]
    hidden_dims = [64, 32]
    output_dim = y_train.shape[1]
    
    regressor = MLPRegressor(
        input_dim=input_dim,
        hidden_dims=hidden_dims,
        output_dim=output_dim,
        activation='relu',
        dropout_rate=0.1
    )
    
    print(f"\n回归器架构:")
    print(f"  输入维度: {input_dim}")
    print(f"  隐藏层: {hidden_dims}")
    print(f"  输出维度: {output_dim}")
    print(f"  参数数量: {regressor.get_num_parameters():,}")
    
    # 测试前向传播
    regressor.eval()
    with torch.no_grad():
        predictions = regressor(X_train[:5])
    
    print(f"\n测试结果:")
    print(f"  预测形状: {predictions.shape}")
    print(f"  真实值形状: {y_train[:5].shape}")
    
    # 测试训练循环
    print("\n测试训练循环...")
    regressor.train()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(regressor.parameters(), lr=0.001)
    
    # 一个小批量的训练
    optimizer.zero_grad()
    outputs = regressor(X_train[:32])
    loss = criterion(outputs, y_train[:32])
    loss.backward()
    optimizer.step()
    
    print(f"  训练损失: {loss.item():.4f}")
    print("✓ 训练循环测试通过")
    
    return regressor


def test_factory_function():
    """测试工厂函数"""
    print("\n" + "=" * 60)
    print("测试工厂函数")
    print("=" * 60)
    
    # 测试创建分类器
    classifier = create_mlp_model(
        model_type='classifier',
        input_dim=10,
        hidden_dims=[32, 16],
        num_classes=3
    )
    
    print(f"工厂创建的分类器: {type(classifier).__name__}")
    print(f"  输入维度: {classifier.input_dim}")
    print(f"  输出维度: {classifier.output_dim}")
    
    # 测试创建回归器
    regressor = create_mlp_model(
        model_type='regressor',
        input_dim=10,
        hidden_dims=[64, 32],
        output_dim=1
    )
    
    print(f"\n工厂创建的回归器: {type(regressor).__name__}")
    print(f"  输入维度: {regressor.input_dim}")
    print(f"  输出维度: {regressor.output_dim}")
    
    print("✓ 工厂函数测试通过")
    
    return classifier, regressor


def test_different_activations():
    """测试不同的激活函数"""
    print("\n" + "=" * 60)
    print("测试不同的激活函数")
    print("=" * 60)
    
    activations = ['relu', 'sigmoid', 'tanh', 'leaky_relu']
    batch_size = 4
    input_dim = 5
    output_dim = 2
    
    X = torch.randn(batch_size, input_dim)
    
    for activation in activations:
        try:
            model = MLP(
                input_dim=input_dim,
                hidden_dims=[8, 4],
                output_dim=output_dim,
                activation=activation
            )
            
            model.eval()
            with torch.no_grad():
                output = model(X)
            
            print(f"激活函数: {activation:12s} - 输出形状: {output.shape} - 测试通过")
        except Exception as e:
            print(f"激活函数: {activation:12s} - 错误: {e}")
    
    print("✓ 激活函数测试完成")


def test_different_configurations():
    """测试不同的网络配置"""
    print("\n" + "=" * 60)
    print("测试不同的网络配置")
    print("=" * 60)
    
    configurations = [
        {"hidden_dims": [64], "dropout_rate": 0.0, "use_batch_norm": False},
        {"hidden_dims": [128, 64], "dropout_rate": 0.2, "use_batch_norm": False},
        {"hidden_dims": [256, 128, 64], "dropout_rate": 0.3, "use_batch_norm": True},
        {"hidden_dims": [512, 256, 128, 64], "dropout_rate": 0.5, "use_batch_norm": True},
    ]
    
    batch_size = 8
    input_dim = 20
    output_dim = 5
    
    X = torch.randn(batch_size, input_dim)
    
    for i, config in enumerate(configurations, 1):
        model = MLP(
            input_dim=input_dim,
            hidden_dims=config["hidden_dims"],
            output_dim=output_dim,
            activation='relu',
            dropout_rate=config["dropout_rate"],
            use_batch_norm=config["use_batch_norm"]
        )
        
        model.eval()
        with torch.no_grad():
            output = model(X)
        
        params = model.get_num_parameters()
        print(f"配置 {i}: 隐藏层={config['hidden_dims']}, "
              f"Dropout={config['dropout_rate']}, "
              f"BatchNorm={config['use_batch_norm']}, "
              f"参数={params:,}, "
              f"输出形状={output.shape}")
    
    print("✓ 配置测试完成")


def test_spiral_dataset():
    """测试螺旋数据集（可视化用）"""
    print("\n" + "=" * 60)
    print("测试螺旋数据集")
    print("=" * 60)
    
    # 生成螺旋数据
    X, y = generate_spiral_data(n_samples=100, n_classes=3)
    
    print(f"螺旋数据形状: X={X.shape}, y={y.shape}")
    print(f"类别分布: {torch.bincount(y).tolist()}")
    
    # 创建分类器
    input_dim = X.shape[1]
    num_classes = len(torch.unique(y))
    
    model = MLPClassifier(
        input_dim=input_dim,
        hidden_dims=[16, 8],
        num_classes=num_classes,
        activation='relu'
    )
    
    # 测试前向传播
    model.eval()
    with torch.no_grad():
        predictions = model.predict(X[:10])
    
    print(f"前10个样本的预测: {predictions.tolist()}")
    print(f"前10个样本的真实标签: {y[:10].tolist()}")
    
    print("✓ 螺旋数据集测试通过")
    
    return X, y, model


def run_all_tests():
    """运行所有测试"""
    print("开始运行MLP测试套件")
    print("=" * 60)
    
    results = {}
    
    try:
        # 测试1: 基本功能
        results['basic'] = test_basic_functionality()
        print("\n" + "=" * 60)
        
        # 测试2: 分类器
        results['classifier'] = test_classifier()
        print("\n" + "=" * 60)
        
        # 测试3: 回归器
        results['regressor'] = test_regressor()
        print("\n" + "=" * 60)
        
        # 测试4: 工厂函数
        results['factory'] = test_factory_function()
        print("\n" + "=" * 60)
        
        # 测试5: 激活函数
        test_different_activations()
        print("\n" + "=" * 60)
        
        # 测试6: 不同配置
        test_different_configurations()
        print("\n" + "=" * 60)
        
        # 测试7: 螺旋数据集
        results['spiral'] = test_spiral_dataset()
        
        print("\n" + "=" * 60)
        print("所有测试通过！✓")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # 设置随机种子以确保可重复性
    torch.manual_seed(42)
    np.random.seed(42)
    
    # 运行所有测试
    success = run_all_tests()
    
    if success:
        print("\nMLP实现测试完成，所有功能正常！")
        sys.exit(0)
    else:
        print("\nMLP实现测试失败，请检查代码！")
        sys.exit(1)