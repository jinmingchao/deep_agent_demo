import torch
import numpy as np
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def generate_classification_data(n_samples=1000, n_features=20, n_classes=3, 
                                 n_informative=10, random_state=42):
    """
    生成分类任务的测试数据
    
    参数:
        n_samples: 样本数量
        n_features: 特征数量
        n_classes: 类别数量
        n_informative: 信息特征数量
        random_state: 随机种子
    
    返回:
        X_train, X_test, y_train, y_test: 训练和测试数据
    """
    # 生成分类数据
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,
        n_redundant=n_features - n_informative,
        n_classes=n_classes,
        n_clusters_per_class=1,
        random_state=random_state
    )
    
    # 转换为PyTorch张量
    X = torch.FloatTensor(X)
    y = torch.LongTensor(y)
    
    # 分割训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state
    )
    
    # 标准化特征
    scaler = StandardScaler()
    X_train = torch.FloatTensor(scaler.fit_transform(X_train))
    X_test = torch.FloatTensor(scaler.transform(X_test))
    
    return X_train, X_test, y_train, y_test


def generate_regression_data(n_samples=1000, n_features=10, n_targets=1, 
                             noise=0.1, random_state=42):
    """
    生成回归任务的测试数据
    
    参数:
        n_samples: 样本数量
        n_features: 特征数量
        n_targets: 目标数量
        noise: 噪声水平
        random_state: 随机种子
    
    返回:
        X_train, X_test, y_train, y_test: 训练和测试数据
    """
    # 生成回归数据
    X, y = make_regression(
        n_samples=n_samples,
        n_features=n_features,
        n_targets=n_targets,
        noise=noise,
        random_state=random_state
    )
    
    # 转换为PyTorch张量
    X = torch.FloatTensor(X)
    y = torch.FloatTensor(y)
    
    # 如果y是1D，转换为2D
    if y.dim() == 1:
        y = y.unsqueeze(1)
    
    # 分割训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state
    )
    
    # 标准化特征
    scaler = StandardScaler()
    X_train = torch.FloatTensor(scaler.fit_transform(X_train))
    X_test = torch.FloatTensor(scaler.transform(X_test))
    
    # 标准化目标（对于回归任务）
    y_scaler = StandardScaler()
    y_train = torch.FloatTensor(y_scaler.fit_transform(y_train))
    y_test = torch.FloatTensor(y_scaler.transform(y_test))
    
    return X_train, X_test, y_train, y_test, y_scaler


def generate_simple_test_data(batch_size=32, input_dim=10, output_dim=3):
    """
    生成简单的测试数据用于快速验证
    
    参数:
        batch_size: 批量大小
        input_dim: 输入维度
        output_dim: 输出维度
    
    返回:
        X: 输入数据
        y: 目标数据（随机生成）
    """
    # 生成随机输入数据
    X = torch.randn(batch_size, input_dim)
    
    # 生成随机目标数据
    if output_dim == 1:
        # 回归任务
        y = torch.randn(batch_size, 1)
    else:
        # 分类任务
        y = torch.randint(0, output_dim, (batch_size,))
    
    return X, y


def generate_spiral_data(n_samples=300, n_classes=3, noise=0.1, random_state=42):
    """
    生成螺旋数据集（可视化用）
    
    参数:
        n_samples: 每个类别的样本数量
        n_classes: 类别数量
        noise: 噪声水平
        random_state: 随机种子
    
    返回:
        X, y: 特征和标签
    """
    np.random.seed(random_state)
    
    X = []
    y = []
    
    for class_idx in range(n_classes):
        # 生成螺旋参数
        r = np.linspace(0.0, 1.0, n_samples)
        t = np.linspace(class_idx * 4, (class_idx + 1) * 4, n_samples) + \
            np.random.randn(n_samples) * noise
        
        # 转换为笛卡尔坐标
        x1 = r * np.sin(t)
        x2 = r * np.cos(t)
        
        # 组合特征
        class_X = np.column_stack([x1, x2])
        class_y = np.full(n_samples, class_idx)
        
        X.append(class_X)
        y.append(class_y)
    
    X = np.vstack(X)
    y = np.hstack(y)
    
    # 转换为PyTorch张量
    X = torch.FloatTensor(X)
    y = torch.LongTensor(y)
    
    # 打乱数据
    indices = np.random.permutation(len(X))
    X = X[indices]
    y = y[indices]
    
    return X, y


def get_data_info(X, y):
    """
    获取数据信息
    
    参数:
        X: 特征数据
        y: 标签数据
    
    返回:
        数据信息字典
    """
    info = {
        'num_samples': X.shape[0],
        'input_dim': X.shape[1],
        'output_dim': y.shape[1] if y.dim() > 1 else 1,
        'num_classes': len(torch.unique(y)) if y.dtype == torch.long else None,
        'X_shape': X.shape,
        'y_shape': y.shape,
        'X_dtype': X.dtype,
        'y_dtype': y.dtype,
        'X_range': (X.min().item(), X.max().item()),
        'y_range': (y.min().item(), y.max().item()),
    }
    
    return info


if __name__ == "__main__":
    # 测试数据生成函数
    print("测试数据生成函数...")
    
    # 生成分类数据
    X_train_cls, X_test_cls, y_train_cls, y_test_cls = generate_classification_data(
        n_samples=100, n_features=5, n_classes=3
    )
    print(f"分类数据: X_train shape={X_train_cls.shape}, y_train shape={y_train_cls.shape}")
    
    # 生成回归数据
    X_train_reg, X_test_reg, y_train_reg, y_test_reg, y_scaler = generate_regression_data(
        n_samples=100, n_features=5
    )
    print(f"回归数据: X_train shape={X_train_reg.shape}, y_train shape={y_train_reg.shape}")
    
    # 生成简单测试数据
    X_simple, y_simple = generate_simple_test_data(batch_size=10, input_dim=5, output_dim=2)
    print(f"简单数据: X shape={X_simple.shape}, y shape={y_simple.shape}")
    
    # 生成螺旋数据
    X_spiral, y_spiral = generate_spiral_data(n_samples=50, n_classes=3)
    print(f"螺旋数据: X shape={X_spiral.shape}, y shape={y_spiral.shape}")